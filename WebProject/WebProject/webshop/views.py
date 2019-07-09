"""
Definition of views.
"""
from datetime import datetime

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth.views import login
from django.core.mail import send_mail

from webshop.models import Category, Product, CartItem, Cart, Brand
from webshop.forms import RegistrationForm, OrderForm
from webshop.functions import get_cart, get_or_create_cart



#Названия переменных переписать, проверяя как они используется в шаблонах

def home_view(request):
	products = Product.objects.all()
	brands = Brand.objects.all()
	context = {
		'products': products,
		'brands': brands
		}
	return render(request, 'index.html', context)

def registration_view(request):
	form = RegistrationForm(request.POST or None)
	if form.is_valid():

		new_user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']

		#Перенести в методы формы
		#Сохранение нового юзера
		new_user.username = username
		new_user.set_password(password)
		new_user.email = email
		new_user.first_name = first_name
		new_user.last_name = last_name
		new_user.save()
		#переименовать
		#вынести в отдельную функцию
		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('home'))
	#Добавил чтобы получать сообщение об ошибке при тестировании, надо бы переписать
#	else:
#		form.clean()

	context = {
		'form': form
		}
	return render(request, 'registration.html', context)

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
	products_of_category = Product.objects.filter(category=category)
	#рабоатет неправильно, разобраться
	#products_of_category = category.product_set.all()
	context = {
		'category': category,
		'products_of_category': products_of_category
		}
	return render(request, 'category.html', context)

def brand_view(request, brand_slug):
	brand = Brand.objects.get(slug=brand_slug)
	products_of_brand = brand.product_set.all()
	context = {
		'brand': brand,
		'products_of_brand': products_of_brand
		}
	return render(request, 'brand.html', context)

def cart_view(request):
	return render(request, 'cart.html')


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

def checkout_view(request):
	return render(request, 'checkout.html', {})

def order_create_view(request):
	form = OrderForm(request.POST or None)
	context = {
		'form': form,
		}
	return render(request, 'order.html', context)

def make_order_view(request):

	form = OrderForm(request.POST or None)
	if form.is_valid():
		cart, created = get_or_create_cart(request)
		name = form.cleaned_data['name']
		last_name = form.cleaned_data['last_name']
		patronymic = form.cleaned_data['patronymic']
		email = form.cleaned_data['email']
		phone = form.cleaned_data['phone']
		city = form.cleaned_data['city']
		address = form.cleaned_data['address']
		postcode = form.cleaned_data['postcode']
		comments = form.cleaned_data['comments']
		new_order = Order()
		new_order.user = request.user
		new_order.save()
		new_order.items.add(cart)
		new_order.first_name = name
		new_order.last_name = last_name
		new_order.patronymic = patronymic
		new_order.email = email
		new_order.phone = phone
		new_order.city = city
		new_order.address = address
		new_order.postcode = postcode
		new_order.comments = comments
		new_order.total = cart.total_price
		new_order.save()
		del request.session['cart_id']
		del request.session['total_quantity_items_in_cart']
		return HttpResponseRedirect(reverse('home'))
	return render(request, 'order.html', {})

#Пишу тест отправки письма
#send_mail('Subject here', 'Here is the message.', 'from@example.com',
#    ['to@example.com'], fail_silently=False)
	
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

def return_page(request, template):
	return render(request, template, {})
