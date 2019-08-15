from datetime import datetime

from webshop.models import Category
from webshop.functions import get_or_create_cart

#создать функции для работы с ключами сессии при работе с корзиной
def menu(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
		'year': datetime.now().year,
        }
    return context

def cart_in_session(request):
    cart, created = get_or_create_cart(request)
    context = {
        'cart': cart
        }
    return context
