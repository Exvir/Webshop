from django.test import TestCase
from django.urls import resolve
from django.core.management import call_command

import webshop.views
from webshop.models import Category, Brand, Product

class HomeViewTest(TestCase):

    def test_200_code_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class ProductViewTest(TestCase):

    fixtures = ['db']

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.get(slug='emporio-test1')

    def test_200_code_response(self):
        response = self.client.get('/product/emporio-test1/')
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        response = self.client.get('/product/emporio-test1/')
        self.assertIsNotNone(response.context)        
        self.assertEqual(response.context.get('product'), self.product)

class CategoryViewTest(TestCase):

    fixtures = ['db']

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.get(slug='watchs-of-man')

    def test_200_code_response(self):
        response = self.client.get('/category/watchs-of-man/')
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        response = self.client.get('/category/watchs-of-man/')
        self.assertIsNotNone(response.context)        
        self.assertEqual(response.context.get('category'), self.category)
        #QuerySet нельзя сравнивать, по этому ограничиваюсь сравнением первого элемента, возможно следует перебрать в цикле for
        self.assertEqual(response.context.get('brands').first(), self.category.brands.all().first())
        self.assertEqual(response.context.get('products_of_category').first(), Product.objects.filter(category=self.category).first())

class BrandPageTest(TestCase):

    fixtures = ['db']

    def test_200_code_response(self):
        response = self.client.get('/brand/emporio-armani/')
        self.assertEqual(response.status_code, 200)

    def test_context_of_response(self):		
		
        response = self.client.get('/brand/emporio-armani/')
        self.assertIsNotNone(response.context)
        self.assertEqual(response.context.get('brand'), Brand.objects.get(slug='emporio-armani'))

class CartPageTest(TestCase):

    fixtures = ['db']

    def test_200_code_response(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)