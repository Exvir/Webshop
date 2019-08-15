"""
Definition of views.
"""
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from django.views.generic import View, ListView

from webshop.models import Category, Product, CartItem, Cart, Brand, Order
from webshop.forms import OrderForm, ContactUsForm
from webshop.functions import get_cart, get_or_create_cart

#Названия переменных переписать, проверяя как они используется в шаблонах

class HomeView(ListView):

	template_name = 'index.html'
	context_object_name = 'products'
	model = Product

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['brands'] = Brand.objects.all()
		return context

class ProductView(ListView):

	template_name = 'product.html'
	context_object_name = 'product'

	def get_queryset(self):
		self.product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
		return self.product

class CategoryView(ListView):

	template_name = 'category.html'
	context_object_name = 'category'

	def get_queryset(self):
		self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
		return self.category

	def get_context_data(self, **kwargs):
		context = super(CategoryView, self).get_context_data(**kwargs)
		context['brands'] = self.category.brands.all()
		context['products_of_category'] = Product.objects.filter(category=self.category)
		return context	

class BrandView(ListView):

	template_name = 'brand.html'
	context_object_name = 'brand'

	def get_queryset(self):
		self.brand = get_object_or_404(Brand, slug=self.kwargs['brand_slug'])
		return self.brand

	def get_context_data(self, **kwargs):
		context = super(BrandView, self).get_context_data(**kwargs)
		context['products_of_brand'] = Product.objects.filter(brand=self.brand)
		return context	

class OrderView(View):

	form_class = OrderForm
	template_name = 'order.html'
	
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			new_order = form.save()
			cart = get_cart(request)
			new_order.items.add(cart)
			new_order.save()
		#дописать отправку письма в отдельном методе
			values = new_order.get_values_local_fields()	
			message = 'Данные заказа \n'
			message += ','.join(map(str, values))
			message += 'Посмотреть заказ №{} в базе данных можно по ссылке: https://clock.conwert.ru/admin/webshop/order/'.format(new_order.id)
			send_mail('Поступил Заказ №{}'.format(new_order.id), message,
					'tiktakclock24@gmail.com', ['tiktakclock24@gmail.com'], fail_silently=False)

			del request.session['cart_id']
			del request.session['total_quantity_items_in_cart']
			return HttpResponseRedirect(reverse('home'))
        else:
            pass # дописать возврат формы с ошибками, смотри конспект лекций по формам
		return render(request, self.template_name)

class ContactUsView(View):

	form_class = ContactUsForm
	template_name = 'contact_us.html'
	
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

	def post(self, request, *args, **kwargs):
		contact_form = self.form_class(request.POST) # A form bound to the POST data
		if contact_form.is_valid(): # All validation rules pass
			subject = "(Обратная связь от клиента) "
			subject += contact_form.cleaned_data['subject']
			sender = contact_form.cleaned_data['sender']
			message = 'Письмо было отправлено от {} \r\n \r\n'.format(sender)
			message += contact_form.cleaned_data['message']
			recipient = ['tiktakclock24@gmail.com']
			try:
				send_mail(subject, message, sender, recipient, fail_silently=False)
			except:
				# TODO: дописать сообщение о том, что отправка провалилась
				pass
			return HttpResponseRedirect(reverse('home'))
	#		return render_to_response(reverse('home'), {'path_back': path_back}, context_instance=RequestContext(request))

		return HttpResponseRedirect(reverse('home'))
	#	return render_to_response(reverse('home'), context_instance=RequestContext(request))

#Добавление в корзину
def add_to_cart_view(request):
	cart, created = get_or_create_cart(request)
	product_slug = request.GET.get('product_slug')		#значение передаётся с запросом с помощью JS
	quantity = request.GET.get('quantity')
	product = Product.objects.get(slug=product_slug)
	cart.add_item(product_slug=product.slug, quantity=quantity)
	cart.recount_total_price()
	return JsonResponse(
		{'cart_total': cart.items.count(),
		'cart_total_price': cart.total_price
		})

#Удаление из корзины
def remove_from_cart_view(request):
	cart = get_cart(request)
	product_slug = request.GET.get('product_slug')		#значение передаётся методом GET
	product = Product.objects.get(slug=product_slug)
	cart.remove_from_cart(product_slug=product.slug)
	cart.recount_total_price()

	return JsonResponse(
		{"cart_total": cart.items.count(),
		'cart_total_price': cart.total_price
		})

def change_item_quantity_and_recount_total_price_view(request):
	cart = get_cart(request)
	item_id = request.GET.get('item_id')
	new_quantity = request.GET.get('new_quantity')
	cart_item = CartItem.objects.get(id=item_id)
	cart_item.change_quantity(new_quantity=new_quantity)
	cart_item.recount_total_price(new_quantity=new_quantity)
	cart.recount_total_price()
	return JsonResponse(
		{"cart_total": cart.items.count(),
		'item_total': cart_item.total_price,
		'cart_total_price': cart.total_price
		})

#Переписать с использованием _set c 227 книга по джанго
#Чистим мусор
def clean_view(request):
	for itemcart in CartItem.objects.all():
		itemcart.associated_with_cart = False
	for cart in Cart.objects.all():
		for cartitem in cart.items.all():
			cartitem.associated_with_cart = True
			cartitem.save()
	for itemcart in CartItem.objects.filter(associated_with_cart=False):
		itemcart.delete()
	return HttpResponseRedirect(reverse('home'))


'''
def home_view(request):
	products = Product.objects.all()
	brands = Brand.objects.all()
	context = {
		'products': products,
		'brands': brands
		}
	return render(request, 'index.html', context)

TODO: Удалить после того как класс будет протестирован
#Для отображения url в шаблоне
def product_view(request, product_slug):
	product = Product.objects.get(slug=product_slug)
	context = {
		'product': product
		}
	return render(request, 'product.html', context)

#Для отображения url в шаблоне
def category_view(request, category_slug):
	category = Category.objects.get(slug=category_slug)
	brands = category.brands.all()
	products_of_category = Product.objects.filter(category=category)
	context = {
		'category': category,
		'brands': brands,
		'products_of_category': products_of_category
		}
	return render(request, 'category.html', context)

def brand_view(request, brand_slug):
	brand = Brand.objects.get(slug=brand_slug)
	products_of_brand = Product.objects.filter(brand=brand)
	context = {
		'brand': brand,
		'products_of_brand': products_of_brand
		}
	return render(request, 'brand.html', context)

TODO: удалить после проверки работоспособности класса
def make_order_view(request):

	form = OrderForm(request.POST)
	if form.is_valid():
		new_order = form.save()
		cart = get_cart(request)
		new_order.items.add(cart)
		new_order.save()
		
		values = new_order.get_values_local_fields()		
		message = 'Данные заказа \n'
		message += ','.join(map(str, values))
		message += 'Посмотреть заказ №{} в базе данных можно по ссылке: https://clock.conwert.ru/admin/webshop/order/'.format(new_order.id)
		send_mail('Поступил Заказ №{}'.format(new_order.id), message,
				'tiktakclock24@gmail.com', ['tiktakclock24@gmail.com'], fail_silently=False)

		del request.session['cart_id']
		del request.session['total_quantity_items_in_cart']
		return HttpResponseRedirect(reverse('home'))
	return render(request, 'order.html', {})

def make_contact_us_view(request):

	if request.method == 'POST': # If the form has been submitted...
		contact_form = ContactUsForm(request.POST) # A form bound to the POST data
		if contact_form.is_valid(): # All validation rules pass
			subject = "(Обратная связь от клиента) "
			subject += contact_form.cleaned_data['subject']
			sender = contact_form.cleaned_data['sender']
			message = 'Письмо было отправлено от {} \r\n \r\n'.format(sender)
			message += contact_form.cleaned_data['message']
			recipient = ['tiktakclock24@gmail.com']

		# и отправим его
		try:
			send_mail(subject, message, sender, recipient, fail_silently=False)
		except:
			# TODO: дописать сообщение о том, что отправка провалилась
			pass
		
		return HttpResponseRedirect(reverse('home'))
#		return render_to_response(reverse('home'), {'path_back': path_back}, context_instance=RequestContext(request))

	return HttpResponseRedirect(reverse('home'))
#	return render_to_response(reverse('home'), context_instance=RequestContext(request))
'''	