from django.test import TestCase

from webshop.models import Brand, Category, Product, Cart, CartItem, TypeOfMechanism

class CartItemModelTest(TestCase):
	
	fixtures = ['db']
	
	@classmethod
	def setUpTestData(cls):
		cls.test_product = Product.objects.get(title='Emporio test1')
		cls.test_cart_item = CartItem.objects.create(product=cls.test_product)

	def test_change_quantity_in_cart_item(self):
		self.test_cart_item.change_quantity(new_quantity=2)
		self.assertEqual(self.test_cart_item.quantity, 2)

	def test_recount_total_price(self):
		test_quantity = 2
		control_price = self.test_cart_item.product.price
		control_total_price = control_price * test_quantity
		self.test_cart_item.recount_total_price(new_quantity=test_quantity)		
		self.assertEqual(self.test_cart_item.total_price, control_total_price)

class CartModelTest(TestCase):

	fixtures = ['db']

	@classmethod
	def setUpTestData(cls):
		cls.test_cart = Cart.objects.create()

	def test_add_item_to_cart(self):
		self.assertEqual(self.test_cart.items.all().count(), 0)
		self.test_cart.add_item(product_slug='emporio-test1', quantity=1)
		self.assertEqual(self.test_cart.items.all().count(), 1)

	def test_recount_total_price(self):		
		self.test_cart.add_item(product_slug='emporio-test1', quantity=1)
		self.assertEqual(self.test_cart.total_price, 0.0)
		self.test_cart.recount_total_price()
		self.assertEqual(self.test_cart.total_price, 9999.0)
		
	def test_remove_from_cart(self):
		self.assertEqual(self.test_cart.items.all().count(), 0)
		self.test_cart.add_item(product_slug='emporio-test1', quantity=1)
		self.assertEqual(self.test_cart.items.all().count(), 1)
		self.test_cart.remove_from_cart(product_slug='emporio-test1')
		self.assertEqual(self.test_cart.items.all().count(), 0)