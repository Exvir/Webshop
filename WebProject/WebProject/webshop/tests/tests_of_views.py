from django.test import TestCase
from django.urls import resolve

import webshop.views
from webshop.models import Category, Brand

class HomePageTest(TestCase):

	def test_url_resolves(self):
		#преобразование url в представление
		found = resolve('/')
		self.assertEqual(found.func, webshop.views.home_view)
	
	def test_home_view_returns_correct_title(self):

		response = self.client.get('/')
		html = response.content.decode('utf8') 
		self.assertIn('<title>Интернет магазин</title>', html)
		
	def test_context_of_response(self):
		
		Category.objects.create(name='The first test category', slug='test-slug')
		
		response = self.client.get('/')
		self.assertIsNotNone(response.context.get('cart'))
		self.assertEqual(response.context.get('categories').count(), Category.objects.all().count())
		
class ProductPageTest(TestCase):

	def test_url_resolves(self):
		#преобразование url в представление
		found = resolve('/product/test-slug/')
		self.assertEqual(found.func, webshop.views.product_view)

class СategoryPageTest(TestCase):

	def test_url_resolves(self):
		#преобразование url в представление
		found = resolve('/category/test-slug/')
		self.assertEqual(found.func, webshop.views.category_view)
#Одинаковые QuerySet не равны друг другу, а если распаковать, то нормально, надо разобраться
	def test_context_of_response(self):
		
		Category.objects.create(name='The first test category', slug='test-slug')
		
		response = self.client.get('/category/test-slug/')
		self.assertIsNotNone(response.context)
		self.assertEqual(response.context.get('category'), Category.objects.get(slug='test-slug'))

class BrandPageTest(TestCase):

	def test_url_resolves(self):
		#преобразование url в представление
		found = resolve('/brand/test-slug/')
		self.assertEqual(found.func, webshop.views.brand_view)

	def test_context_of_response(self):
		
		Brand.objects.create(name='The first test brand', slug='test-slug')
		
		response = self.client.get('/brand/test-slug/')
		self.assertIsNotNone(response.context)
		self.assertEqual(response.context.get('brand'), Brand.objects.get(slug='test-slug'))

#написать тесты для вьшек корзины
class CartPageTest(TestCase):

	def test_cart_page_url_resolves(self):
		#преобразование url в представление
		found = resolve('/cart/')
		self.assertEqual(found.func, webshop.views.cart_view)

	def test_add_to_cart_url_resolves(self):
		#преобразование url в представление
		found = resolve('/add_to_cart/')
		self.assertEqual(found.func, webshop.views.add_to_cart_view)

	def test_remove_from_cart_url_resolves(self):
		#преобразование url в представление
		found = resolve('/remove_from_cart/')
		self.assertEqual(found.func, webshop.views.remove_from_cart_view)

