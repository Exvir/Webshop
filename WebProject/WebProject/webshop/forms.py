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
		labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
			"patronymic": "Отчество",
			"phone": "Контактный телефон",
			"postcode": "Почтовый индекс",
			"city": "Город",
			"address": "Адресс доставки",
			"comments": "Комментарии к заказу"
        }
		widgets = {
                'comments': forms.Textarea(),
                }
		help_texts = {
            'phone': 'Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться!',
        }

class ContactUsForm(forms.Form):

	subject = forms.CharField(label="Тема")
	message  = forms.CharField(label='Сообщение', widget=forms.Textarea())
	sender = forms.EmailField(label='Ваш E-mail')