import json
from django.core.exceptions import ViewDoesNotExist
from django.test import SimpleTestCase, TestCase
from django.urls import get_callable, reverse
from rest_framework.authtoken.models import Token

from .models import (Shop, Category, User, Product,
                           ProductInfo, Parameter, ProductParameter)


class ShopsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создать 10 Shops
        number_of_shops = 10
        for shop_num in range(number_of_shops):
            Shop.objects.create(name='Shop %s' % shop_num)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('http://127.0.0.1:8000/api/v1/shops')
        self.assertNotEqual(resp.status_code, 404)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:shops'))
        self.assertNotEqual(resp.status_code, 404)

    def test_lists_all_shops(self):
        count = Shop.objects.all().count()
        resp = self.client.get(reverse('api:shops'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['count'] == count)


class CategoriesViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создать 5 Categories
        number_of_categories = 5
        for category_num in range(number_of_categories):
            Category.objects.create(name='Category %s' % category_num)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('http://127.0.0.1:8000/api/v1/categories')
        self.assertNotEqual(resp.status_code, 404)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:categories'))
        self.assertNotEqual(resp.status_code, 404)

    def test_lists_all_categories(self):
        count = Category.objects.all().count()
        resp = self.client.get(reverse('api:categories'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['count'] == count)

class ProductViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # создать Shops
        cls.shop_1 = Shop.objects.create(name='Shop 1')
        cls.shop_2 = Shop.objects.create(name='Shop2')
        # Создать 2 Categories
        cls.category_1 = Category.objects.create(name='Category 1')
        cls.category_1.shops.add(cls.shop_1)
        cls.category_2 = Category.objects.create(name='Category 1')
        cls.category_2.shops.add(cls.shop_2)
        # Создать 2 Product
        cls.product = Product.objects.create(name='Product 1',
                                             category=cls.category_1)

        cls.product_info = ProductInfo.objects.create(model='New',
                                                      external_id=1111,
                                                      product=cls.product,
                                                      shop=cls.shop_1,
                                                      quantity=1,
                                                      price=100,
                                                      price_rrc=110)
        cls.parameter = Parameter.objects.create(name='First')
        ProductParameter.objects.create(product_info=cls.product_info,
                                        parameter=cls.parameter,
                                        value='Value')
        cls.product_2 = Product.objects.create(name='Product 2',
                                               category=cls.category_2)

        cls.product_info_2 = ProductInfo.objects.create(model='New2',
                                                        external_id=1122,
                                                        product=cls.product_2,
                                                        shop=cls.shop_2,
                                                        quantity=2,
                                                        price=102,
                                                        price_rrc=112)
        ProductParameter.objects.create(product_info=cls.product_info_2,
                                        parameter=cls.parameter,
                                        value='Value')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('http://127.0.0.1:8000/api/v1/products')
        self.assertNotEqual(resp.status_code, 404)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('api:products'))
        self.assertNotEqual(resp.status_code, 404)

    def test_shop_state(self):
        resp = self.client.get(reverse('api:products'))
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.content)
        self.assertEqual(len(resp_json), 2)