# -*- coding: utf-8 -*-
"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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

class RegistrationForm(forms.ModelForm):

	password = forms.CharField(label='password', widget=forms.PasswordInput)
	password_check = forms.CharField(label='password_check', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'password_check',
			'first_name',
			'last_name',
			'email'
			]

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'
		self.fields['password'].help_text = 'Придумайте пароль'
		self.fields['password_check'].label = 'Повторите пароль'
		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'
		self.fields['email'].label = 'Ваша почта'
		self.fields['email'].help_text = 'Укажите правильный e-mail'
	#Валидация
	#Добавить поле емэйла как обязательное
	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		first_name = self.cleaned_data['first_name']
		last_name =  self.cleaned_data['last_name']
		email = self.cleaned_data['email']

		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('Пользователь с данным логином уже зарегистрирован')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Пользователь с данным email уже зарегистрирован')
		if password != password_check:
			raise forms.ValidationError('Ваши пароли не совпадают')
		if len(password) < 4:
			raise forms.ValidationError('Ваш пароль короче 4 символов')

		if email is None:
			raise forms.ValidationError('Укажите e-mail')

	

class OrderForm(forms.Form):

	name = forms.CharField(label="Имя")
	last_name  = forms.CharField(label='Фамилия')
	patronymic = forms.CharField(label='Отчество')
	email = forms.EmailField()
	phone = forms.CharField(label = 'Контактный телефон', 
						 help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться!')
	postcode = forms.IntegerField(label = 'Почтовый индекс')
	city = forms.CharField(label='Город')
	#buying_type = forms.ChoiceField(label = 'Способ получения', widget=forms.Select(), 
	#							 choices=([('self', 'Самовывоз'), ('delivery', 'Доставка')])) 
	#date = forms.DateField(label = 'Дата доставки', 
	#					help_text = 'Доставка производится на следующий день после оформления заказа. Менеджер свяжется с Вами предварительно', 
	#					widget=forms.SelectDateWidget(), initial=timezone.now()
	#					)
	address = forms.CharField(label = 'Адресс доставки', required=False)
	comments = forms.CharField(label = 'Комментарии к заказу', widget=forms.Textarea, required=False)
	