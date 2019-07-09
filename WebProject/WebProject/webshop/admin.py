from django.contrib import admin

from webshop.models import Category, Brand, CartItem, Cart, TypeOfMechanism, Product, Test, Order


# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(TypeOfMechanism)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Test)
admin.site.register(Order)
