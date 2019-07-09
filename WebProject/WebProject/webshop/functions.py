from webshop.models import Cart

#Используется в views для получения корзины
#Используется в процессоре контекста

def get_cart(request):
    cart_id = request.session['cart_id']				#Присваиваем переменной значение имеющиеся в сессии по ключу 'cart_id'
    cart = Cart.objects.get(id=cart_id)					
    request.session['total_quantity_items_in_cart'] = cart.items.count()		#Присваиваем ключу 'item_total_quantity' новое значение количества товаров в корзине
    return cart

def create_cart(request):
    cart = Cart.objects.create()
    cart_id = cart.id									
    request.session['cart_id'] = cart_id				#Присваиваем значение id корзины ключу 'cart_id' в сессии
    cart = Cart.objects.get(id=cart_id)					
    return cart

def get_or_create_cart(request):
    try:
        cart = get_cart(request)
        return cart, False
    except (KeyError, Cart.DoesNotExist):													
        cart =	create_cart(request)
        return cart, True
