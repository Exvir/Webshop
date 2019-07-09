from django.test import TestCase

from webshop.models import Brand, Category, Product, Cart, CartItem, TypeOfMechanism

#ПЕРЕПИСАТЬ ВСЕ ТЕСТЫ!!!

#Тесты моделей
class BrandModelTest(TestCase):
	
	def test_saving_brands(self):

		Brand.objects.create(name='The first test brand')
		Brand.objects.create(name='The second test brand')

		saved_brands = Brand.objects.all()
		self.assertEqual(saved_brands.count(), 2)

		first_saved_brand = saved_brands[0]
		second_saved_brand = saved_brands[1]
		self.assertEqual(first_saved_brand.name, 'The first test brand')
		self.assertEqual(second_saved_brand.name, 'The second test brand')

class CategoryModelTest(TestCase):
	
	def test_saving_categories(self):

		Category.objects.create(name='The first test category', slug='the-first-test-category')
		Category.objects.create(name='The second test category', slug='the-second-test-category')

		saved_categories = Category.objects.all()
		self.assertEqual(saved_categories.count(), 2)

		first_saved_category = saved_categories[0]
		second_saved_category = saved_categories[1]
		self.assertEqual(first_saved_category.name, 'The first test category')
		self.assertEqual(first_saved_category.slug, 'the-first-test-category')
		self.assertEqual(second_saved_category.name, 'The second test category')
		self.assertEqual(second_saved_category.slug, 'the-second-test-category')

class ProductModelTest(TestCase):

	def test_saving_product(self):

		test_category = Category.objects.create(name='The first test category', 
									slug='the-first-test-category')
		test_brand = Brand.objects.create(name='The first test brand')

		Product.objects.create(category=test_category, brand=test_brand,
								title='test1', slug='test1', description='test_description',
								price=9999
								)
		saved_products = Product.objects.all()
		self.assertEqual(saved_products.count(), 1)

		test_type_of_mechanism = TypeOfMechanism.objects.create(name='The first test mechanism' 
									)
		Product.objects.create(category=test_category, type_of_mechanism=test_type_of_mechanism, brand=test_brand,
								title='test2', slug='test2', description='test_description',
								price=9999
								)
		self.assertEqual(saved_products.count(), 2)

class CartItemModelTest(TestCase):

	def create_test_object(self):

		test_category = Category.objects.create(name='The first test category', 
									slug='the-first-test-category')
		test_brand = Brand.objects.create(name='The first test brand')
		
		test_product = Product.objects.create(category=test_category, brand=test_brand,
								title='test', slug='test', description='test_description',
								price=9999
								)
		return CartItem.objects.create(product=test_product)
	
	@create_test_objects
	def test_saving_cart_item(self):
		
	#	saved_cart_items = self.create_test_object()
		self.assertEqual(CartItem.objects.count(), 1)

	def test_change_quantity_in_cart_item(self):

		saved_cart_item = self.create_test_object()
		saved_cart_item.change_quantity(new_quantity=2)
		self.assertEqual(saved_cart_item.quantity, 2)

	def test_recount_total_price(self):
		
		saved_cart_item = self.create_test_object()

		test_quantity = 2
		control_price = saved_cart_item.product.price
		control_total_price = control_price * test_quantity

		saved_cart_item.recount_total_price(new_quantity=test_quantity)
		
		self.assertEqual(saved_cart_item.total_price, control_total_price)

class CartModelTest(TestCase):
	
	def create_test_objects(self):

		self.test_category = Category.objects.create(name='The first test category', 
									slug='the-first-test-category')
		self.test_brand = Brand.objects.create(name='The first test brand')
		
		self.test_product = Product.objects.create(category=self.test_category, brand=self.test_brand,
								title='test', slug='test', description='test_description',
								price=9999
								)
		self.test_cart_item = CartItem.objects.create(product=self.test_product, quantity=1, total_price=9999)
		self.test_cart = Cart.objects.create()
		return self.test_cart

	def test_saving_cart(self):

		new_cart = self.create_test_objects()
		self.assertEqual(Cart.objects.all().count(), 1)

	def test_add_item_to_cart(self):

		new_cart = self.create_test_objects()
		self.assertEqual(new_cart.items.all().count(), 0)
		new_cart.add_item(product_slug='test', quantity=1)
		self.assertEqual(new_cart.items.all().count(), 1)

	def test_recount_total_price(self):
		
		new_cart = self.create_test_objects()
		cart_items = new_cart.items.all()
		new_cart.items.add(self.test_cart_item)

		self.assertEqual(new_cart.total_price, 0.0)
		new_cart.recount_total_price()
		self.assertEqual(new_cart.total_price, 9999.0)
		
	def test_remove_from_cart(self):

		new_cart = self.create_test_objects()
		self.assertEqual(new_cart.items.all().count(), 0)
		new_cart.add_item(product_slug='test', quantity=1)
		self.assertEqual(new_cart.items.all().count(), 1)
		new_cart.remove_from_cart(product_slug='test')
		self.assertEqual(new_cart.items.all().count(), 0)

	
