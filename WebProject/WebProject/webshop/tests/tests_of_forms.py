from django.test import TestCase
from django.urls import resolve

from django.contrib.auth.views import login
from django.contrib.auth.models import User

import webshop.views

"""
class RegistrationFormTest(TestCase):

	def test_root_url_resolves_to_registration_view(self):
		#преобразование url в представление
		found = resolve('/registration/')
		self.assertEqual(found.func, webshop.views.registration_view)
	

	def test_can_register_new_user_from_POST_request(self):
		#Проверка создания юзера
		data={
			'username': 'test_user', 'password': 'test', 
			'password_check': 'test', 'first_name': 'test_first_name',
			'last_name': 'test_last_name', 'email': 'test@mail.ru'
			}
		response = self.client.post('/registration/', data)
		users = User.objects.all()
		self.assertEqual(User.objects.count(), 1)
				
	def test_redirects_after_registration_new_user(self):
		#проверка перенаправления
		data={
			'username': 'test_user', 'password': 'test', 
			'password_check': 'test', 'first_name': 'test_first_name',
			'last_name': 'test_last_name', 'email': 'test@mail.ru'
			}
		response = self.client.post('/registration/', data)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')
		#дописать проверку аутентификации
"""