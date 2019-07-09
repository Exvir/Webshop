from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase
#узнать что за библиотека
from importlib import import_module

import webshop.functions
from webshop.models import Cart

class GetOrCreateCartTest(TestCase):

	def test_create_object_cart(self):
		request = HttpRequest()
		session_key = None
		engine = import_module(settings.SESSION_ENGINE)
		request.session = engine.SessionStore(session_key)
		webshop.functions.create_cart(request)
		self.assertEqual(Cart.objects.count(), 1)

	def test_return_created_cart(self):
		request = HttpRequest()
		session_key = None
		engine = import_module(settings.SESSION_ENGINE)
		request.session = engine.SessionStore(session_key)
		cart = webshop.functions.create_cart(request)
		cart_id = request.session['cart_id']
		self.assertEqual(cart, Cart.objects.get(id=cart_id))

	def test_get_cart(self):
		request = HttpRequest()
		session_key = None
		engine = import_module(settings.SESSION_ENGINE)
		request.session = engine.SessionStore(session_key)
		request.session['cart_id'] = 1

		Cart.objects.create(id=1)

		cart = webshop.functions.get_cart(request)
		self.assertEqual(cart, Cart.objects.get(id=1))

	def test_get_or_create_cart(self):

		request = HttpRequest()
		session_key = None
		engine = import_module(settings.SESSION_ENGINE)
		request.session = engine.SessionStore(session_key)

		cart, created = webshop.functions.get_or_create_cart(request)
		self.assertTrue(created)

		request.session['cart_id'] = 1
		Cart.objects.create(id=1)

		cart, created = webshop.functions.get_or_create_cart(request)
		self.assertFalse(created)
