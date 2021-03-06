from datetime import datetime

import django.contrib.auth.views
from django.conf.urls import url, include
from django.views.generic import TemplateView

import webshop.forms
import webshop.views

urlpatterns = [
    # Examples:
    url(r'^$', webshop.views.HomeView.as_view(), name='home'),
    url(r'^test1/$', TemplateView.as_view(template_name='1.html'), name='1'),
    url(r'^test2/$', TemplateView.as_view(template_name='2.html'), name='2'),
    url(r'^test3/$', TemplateView.as_view(template_name='3.html'), name='3'),
    url(r'^test4/$', TemplateView.as_view(template_name='4.html'), name='4'),
    url(r'^test5/$', TemplateView.as_view(template_name='5.html'), name='5'),
    url(r'^accounts/', include('registration.backends.default.urls'), name='accounts'),
    url(r'^logout$', django.contrib.auth.views.logout, {'next_page': '/',}, name='logout'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', webshop.views.ProductView.as_view(), name='product_detail'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', webshop.views.CategoryView.as_view(), name='category_detail'),
    url(r'^brand/(?P<brand_slug>[-\w]+)/$', webshop.views.BrandView.as_view(), name='brand_detail'),
    url(r'^cart/$', TemplateView.as_view(template_name="cart.html"), name='cart'),
    url(r'^cart/add_to_cart/$', webshop.views.add_to_cart_view, name='add_to_card'),
    url(r'^cart/remove_from_cart/$', webshop.views.remove_from_cart_view, name='remove_from_cart'),
    url(r'^cart/change_item_quantity_and_recount_total_price/$',
        webshop.views.change_item_quantity_and_recount_total_price_view,
        name="change_item_quantity_and_recount_total_price"),
    url(r'^cart/checkout/$', TemplateView.as_view(template_name="checkout.html"), name="checkout"),
    url(r'^order$', webshop.views.OrderView.as_view(), name='order'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^discounts/$', TemplateView.as_view(template_name="discounts.html"), name='discounts'),
    url(r'^payment/$', TemplateView.as_view(template_name="payment.html"), name='payment'),
    url(r'^delivery/$', TemplateView.as_view(template_name="delivery.html"), name='delivery'),
    url(r'^contact_us/$', webshop.views.ContactUsView.as_view(), name='contact_us'),
    ]
