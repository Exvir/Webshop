from decimal import Decimal

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


# Create your models here.

#Переопределение менеджера модели, чтобы отключённые товары не отображались в шаблоне
class AvailableProductManager(models.Manager):								
																	
	def all(self, *args, **kwargs):
		return super(AvailableProductManager, self).get_queryset().filter(available=True)

class Brand(models.Model):
	'''Бренд товара'''
	name = models.CharField(max_length = 30, unique = True)
	slug = models.SlugField(blank=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('brand_detail', kwargs={'brand_slug': self.slug})


class Category(models.Model):
	'''Категория товара'''
	name = models.CharField(max_length=30, unique=True)
	slug = models.SlugField(blank=True)
	brands = models.ManyToManyField(Brand, blank=True)

	def __str__(self):
		return self.name
	
	#Создание url категории, используется в шаблоне
	def get_absolute_url(self):
		return reverse('category_detail', kwargs={'category_slug': self.slug})


#Автоматическое создание имени файла изображения
def image_folder(instance, filename):
	
	filename = instance.slug + '.' + filename.split('.')[1]
	return "{0}/{1}".format(instance.slug, filename)

class TypeOfMechanism(models.Model):
	'''Тип механизма'''
	name = models.CharField(max_length=30, unique=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	'''Модель продукта'''
	category = models.ForeignKey(Category)
	type_of_mechanism = models.ForeignKey(TypeOfMechanism, null=True)
	brand = models.ForeignKey(Brand)
	title = models.CharField(max_length = 120)
	slug = models.SlugField()
	description = models.TextField()
	main_image = models.ImageField(upload_to=image_folder)
	first_additional_image = models.ImageField(upload_to=image_folder)
	second_additional_image = models.ImageField(upload_to=image_folder)
	third_additional_image = models.ImageField(upload_to=image_folder)
	price = models.DecimalField(max_digits = 9, decimal_places = 2)
	available = models.BooleanField(default=True)
	objects = AvailableProductManager()											

	def __str__(self):
		return self.title

	#Создание url продукта, используется в шаблоне
	def get_absolute_url(self):											
		return reverse('product_detail', kwargs={'product_slug': self.slug})
		
class CartItem(models.Model):
	'''Хранит информацию о количестве и полной стоимости однотипного товара'''

	product = models.ForeignKey(Product)
	quantity = models.PositiveIntegerField(default=1)
	total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

	def __str__(self):
		return "Cart item for product {0}".format(self.product.title)

	def change_quantity(self, new_quantity):

		cart_item = self
		cart_item.quantity = int(new_quantity)		
		cart_item.save()

	def recount_total_price(self, new_quantity):

		cart_item = self
		product_price = cart_item.product.price
		cart_item.total_price = int(new_quantity) * Decimal(product_price)
		cart_item.save()

class Cart(models.Model):											
	'''Корзина, в нее добавляются CartItem и хранится их общая стоимость'''

	items = models.ManyToManyField(CartItem, blank=True)
	total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

	def __str__(self):
		return str(self.id)

	def recount_total_price(self):

		cart = self
		new_total_price = 0.00
		for item in cart.items.all():
			new_total_price += float(item.total_price)
		cart.total_price = new_total_price
		cart.save()
			
	#Добавить в корзину товар по slug и с количеством полученным из формы
	def add_item(self, product_slug, quantity):
		
		cart = self
		product = Product.objects.get(slug=product_slug)
		total_price_of_item = Decimal(product.price) * int(quantity)
		new_item, created = CartItem.objects.get_or_create(product=product, quantity=quantity, total_price=total_price_of_item)		#created - булевое значение
		'''
		Необходимо избежать прикрепления к корзине экземпляров CartItem
		с одним и тем же товаром, но различным количеством.
		'''
		#Если список пустой, то просто добавляем в него товар
		if not bool(cart.items.all()):
			cart.items.add(new_item)
			cart.save()
		#Итерируем не пустой список, проверяем не возникнет ли дублирования CartItem
		else:
			for cart_item in cart.items.all():
				if new_item.product != cart_item.product:
					cart.items.add(new_item)
					cart.save()

	

	def remove_from_cart(self, product_slug):

		cart = self
		product = Product.objects.get(slug=product_slug)
		for cart_item in cart.items.all():
			if cart_item.product == product:
				cart.items.remove(cart_item)
				cart.save()

class Order(models.Model):
	'''Модель заказа'''
	#Дописать логику для различного поведения модели при заказе аутентифицирвоанным пользователем и нет, пользователь должен хранить историю заказов в личном кабинете
	#user = models.ForeignKey(settings.AUTH_USER_MODEL)
	items = models.ManyToManyField(Cart)
	total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
	first_name = models.CharField(max_length = 200)
	last_name = models.CharField(max_length = 200)
	patronymic = models.CharField(max_length = 200)
	email = models.EmailField()
	phone = models.CharField(max_length = 20)
	city = models.CharField(max_length = 100)
	address = models.CharField(max_length = 255)
	postcode = models.IntegerField(null=True)
	date = models.DateTimeField(auto_now_add=True)
	comments = models.TextField(blank=True)

	def __str__(self):
		return 'Заказ №{0}'.format(str(self.id))

	def get_values_local_fields(self):
		field_names = [field.name for field in Order._meta.local_fields]
		values = []
		for field_name in field_names:
			values.append(getattr(self, field_name))
		return values