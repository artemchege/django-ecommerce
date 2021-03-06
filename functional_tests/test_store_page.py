from selenium import webdriver
from store import models
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time


class TestStorePage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.login_url = self.live_server_url + reverse('login')

    def tearDown(self):
        self.browser.close()

    def make_product(self, name, price, digital):
        product = models.Product.objects.create(name=name, price=price, digital=digital)
        return product

    def test_empty_store_page(self):
        self.browser.get(self.live_server_url)

        alert = self.browser.find_element_by_class_name('row')
        self.assertEqual(alert.find_element_by_tag_name('h4').text, 'Sorry, we do not have items yet.')

    def test_store_page_click_login_button(self):
        self.browser.get(self.live_server_url)

        # user loads main page and clicks login btn
        self.browser.find_element_by_class_name('btn-warning').click()
        self.assertEqual(self.browser.current_url, self.login_url)

    def test_not_empty_store_page(self):
        # user loads main page and sees our product
        self.make_product('Test product', 5000, False)
        self.browser.get(self.live_server_url)
        price_element = self.browser.find_element_by_tag_name('h4').text
        self.assertEqual(price_element, '5000.00')





