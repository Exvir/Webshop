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
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy

from webshop.models import Category, Product, CartItem, Cart, Brand, Order
from webshop.forms import OrderForm, ContactUsForm
from webshop.functions import get_cart, get_or_create_cart



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

class OrderView(FormView):

	success_url = reverse_lazy('home')
	form_class = OrderForm
	template_name = 'order.html'	

	def form_valid(self, form):
		new_order = form.save()
		cart = get_cart(self.request)
		new_order.items.add(cart)
		new_order.save()

		values = new_order.get_values_local_fields()	
		message = 'Данные заказа \n'
		message += ','.join(map(str, values))
		message += f'Посмотреть заказ №{new_order.id} в базе данных можно по ссылке: https://clock.conwert.ru/admin/webshop/order/'
		send_mail(f'Поступил Заказ №{new_order.id}', message,
				'tiktakclock24@gmail.com', ['tiktakclock24@gmail.com'], fail_silently=False)

		del self.request.session['cart_id']
		del self.request.session['total_quantity_items_in_cart']
		
		return super(OrderView, self).form_valid(form)

class ContactUsView(View):

	success_url = reverse_lazy('home')
	form_class = ContactUsForm
	template_name = 'contact_us.html'	

	def form_valid(self, form):
		subject = "(Обратная связь от клиента) "
		subject += form.cleaned_data['subject']
		sender = form.cleaned_data['sender']
		message = f'Письмо было отправлено от {sender} \r\n \r\n'
		message += form.cleaned_data['message']
		recipient = ['tiktakclock24@gmail.com']
		send_mail(subject, message, sender, recipient, fail_silently=False)
		return super(ContactUsView, self).form_valid(form)


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