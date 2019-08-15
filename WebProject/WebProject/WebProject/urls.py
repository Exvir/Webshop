"""
Definition of urls for WebProject.
"""

from datetime import datetime

import django.contrib.auth.views
from django.conf.urls import url

#Импорт библиотек для медиа файлов
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

from registration.forms import RegistrationFormTermsOfService


import webshop.forms
import webshop.views

urlpatterns = [
    # Examples:
    
	url(r'^$', webshop.views.HomeView.as_view(), name='home'),
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

    url(r'^clean/$', webshop.views.clean_view, name='clean'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)		#url для медиа файлов
