from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from store import models
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time


class TestStorePage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.login_url = self.live_server_url + reverse('login')
        self.name = 'test name'
        self.email = 'test@test.test'

    def tearDown(self):
        self.browser.close()

    def make_product(self, name, price, digital):
        product = models.Product.objects.create(name=name, price=price, digital=digital)
        return product

    def wait_func(self, click_submit_button):
        """
        This is function that works with giving redirect submit buttons, it solves the problem of premature closing the
        browser tab.
        :param click_submit_button:
        :return:
        """
        current_url = self.browser.current_url
        click_submit_button()
        WebDriverWait(self.browser, 15).until(EC.url_changes(current_url))

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

    def test_buy_item_whole_cycle(self):
        product = self.make_product('Test product', 5000, False)
        print('product.id', product.id)
        self.browser.get(self.live_server_url)

        # find our item
        add_element_to_cart = self.browser.find_element_by_class_name('add-btn')

        # add it to our cart twice
        add_element_to_cart.click()
        add_element_to_cart.click()

        # give some time to server to handle our ajax queries
        time.sleep(1)

        # visit checkout page
        self.browser.get(self.live_server_url + reverse('checkout'))
        time.sleep(1)

        # fill the form
        name_field = self.browser.find_element_by_name('name')
        email_field = self.browser.find_element_by_name('email')
        address_field = self.browser.find_element_by_name('address')
        city_field = self.browser.find_element_by_name('city')
        phone_field = self.browser.find_element_by_name('phone')
        submit_button = self.browser.find_element_by_class_name('btn-success')
        stripe_button = self.browser.find_element_by_id('checkout-button')

        name_field.send_keys(self.name)
        email_field.send_keys(self.email)
        address_field.send_keys('test address')
        city_field.send_keys('test city')
        phone_field.send_keys('test phone')
        submit_button.click()
        time.sleep(1)
        self.wait_func(stripe_button.click)

        # fill the payments form
        email_field = self.browser.find_element_by_name('email')
        card_field = self.browser.find_element_by_id('cardNumber')
        card_expiry = self.browser.find_element_by_id('cardExpiry')
        card_cvc = self.browser.find_element_by_id('cardCvc')
        card_name = self.browser.find_element_by_id('billingName')
        submit_button = self.browser.find_element_by_class_name('SubmitButton-IconContainer')

        email_field.send_keys(self.email)
        card_field.send_keys('4242424242424242')  # special dummy Stripe test card
        card_expiry.send_keys('555')
        card_cvc.send_keys('555')
        card_name.send_keys(self.name)
        self.wait_func(submit_button.click)

        # check db params
        order = models.Order.objects.all().first()

        # after all we are on success page
        self.assertTrue('/order_paid/' in self.browser.current_url)
        # order exists
        self.assertTrue(order)
        # order paid
        self.assertTrue(order.paid)
        # order complete
        self.assertTrue(order.complete)
        # there is transaction id from Stripe
        self.assertTrue(order.transaction_id)
        # we were as guest
        self.assertTrue(order.customer.as_guest)
        # name corresponds
        self.assertEqual(self.name, order.customer.name)
        # email corresponds
        self.assertEqual(self.email, order.customer.email)





