"""
Definition of urls for WebProject.
"""

from datetime import datetime

import django.contrib.auth.views
from django.conf.urls import url

#Импорт библиотек для медиа файлов
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

from registration.forms import RegistrationFormTermsOfService


import webshop.forms
import webshop.views



urlpatterns = [
    # Examples:
    url(r'^$', webshop.views.home_view, name='home'),
    url(r'^registration/$', webshop.views.registration_view, name='registration'),
	url(r'^accounts/', include('registration.backends.default.urls'), name='accounts'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'login.html',
            'authentication_form': webshop.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', webshop.views.product_view, name = 'product_detail'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', webshop.views.category_view, name = 'category_detail'),
	url(r'^brand/(?P<brand_slug>[-\w]+)/$', webshop.views.brand_view, name = 'brand_detail'),
    url(r'^cart/$', webshop.views.cart_view, name='cart'),
    url(r'^add_to_cart/$', webshop.views.add_to_cart_view, name='add_to_card'),
    url(r'^remove_from_cart/$', webshop.views.remove_from_cart_view, name='remove_from_cart'),
    url(r'^change_item_quantity_and_recount_total_price/$',
        webshop.views.change_item_quantity_and_recount_total_price_view,
        name="change_item_quantity_and_recount_total_price"),
	url(r'^checkout/$', webshop.views.checkout_view, name="checkout"),
    url(r'^order/$', webshop.views.order_create_view, name='order_create'),
	url(r'^make_order/$', webshop.views.make_order_view, name='make_order'),
	url(r'^about/$', webshop.views.return_page, {'template': 'about.html'}, name='about'),
	url(r'^discounts/$', webshop.views.return_page, {'template': 'discounts.html'}, name='discounts'),
	url(r'^payment/$', webshop.views.return_page, {'template': 'payment.html'}, name='payment'),
	url(r'^delivery/$', webshop.views.return_page, {'template': 'delivery.html'}, name='delivery'),
	url(r'^contacts/$', webshop.views.return_page, {'template': 'contacts.html'}, name='contacts'),

    url(r'^clean/$', webshop.views.clean_view, name='clean'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)		#url для медиа файлов
