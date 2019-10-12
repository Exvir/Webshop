from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase
#узнать что за библиотека
from importlib import import_module

import webshop.functions
from webshop.models import Cart
class GetOrCreateCartTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.session_key = None
		cls.engine = import_module(settings.SESSION_ENGINE)
		cls.request = HttpRequest()
		cls.request.session = cls.engine.SessionStore(cls.session_key)

	def test_create_object_cart(self):
		webshop.functions.create_cart(self.request)
		self.assertEqual(Cart.objects.count(), 1)

	def test_return_created_cart(self):
		cart = webshop.functions.create_cart(self.request)
		cart_id = self.request.session['cart_id']
		self.assertEqual(cart, Cart.objects.get(id=cart_id))

	def test_get_cart(self):
		self.request.session = self.engine.SessionStore(self.session_key)
		self.request.session['cart_id'] = 1
		Cart.objects.create(id=1)
		self.cart = webshop.functions.get_cart(self.request)
		self.assertEqual(self.cart, Cart.objects.get(id=1))

	def test_get_or_create_cart(self):
		cart, created = webshop.functions.get_or_create_cart(self.request)
		self.assertTrue(created)
		cart, created = webshop.functions.get_or_create_cart(self.request)
		self.assertFalse(created)