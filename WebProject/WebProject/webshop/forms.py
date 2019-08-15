# -*- coding: utf-8 -*-
"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm

from webshop.models import Order


class BootstrapAuthenticationForm(AuthenticationForm):
	"""Authentication form which uses boostrap CSS."""
	username = forms.CharField(max_length=254,
							   widget=forms.TextInput({
								   'class': 'form-control',
								   'placeholder': 'User name'}))
	password = forms.CharField(label=_("Password"),
							   widget=forms.PasswordInput({
								   'class': 'form-control',
								   'placeholder':'Password'}))

class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['first_name', 'last_name', 'patronymic', 'email', 'phone', 'postcode', 'city', 'address', 'comments']


# Старая форма записи
'''
class OrderForm(forms.Form):

	name = forms.CharField(label="Имя")
	last_name  = forms.CharField(label='Фамилия')
	patronymic = forms.CharField(label='Отчество')
	email = forms.EmailField()
	phone = forms.CharField(label = 'Контактный телефон', 
						 help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться!')
	postcode = forms.IntegerField(label = 'Почтовый индекс')
	city = forms.CharField(label='Город')
	address = forms.CharField(label = 'Адресс доставки', required=False)
	comments = forms.CharField(label = 'Комментарии к заказу', widget=forms.Textarea, required=False)
'''
class ContactUsForm(forms.Form):

	subject = forms.CharField(label="subject")
	message  = forms.CharField(label='message')
	sender = forms.EmailField(label='sender')