import time
import unittest

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		#Установка
		self.browser = webdriver.Chrome()

	def tearDown(self):
		#Демонтаж
		self.browser.quit()

	#Тело теста, нужно переименовать
	def test_body(self):

		self.browser.get(self.live_server_url)
		self.assertIn('Интернет магазин', self.browser.title)
		#проверка наличия меню
		navbar = self.browser.find_element_by_tag_name('nav')

		#проверка наличия товара если он вообще есть и он активирован

