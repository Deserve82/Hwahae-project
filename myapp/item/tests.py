from django.test import TestCase
from .models import Item, Ingredient
# Create your tests here.

class ItemTestCase(TestCase):
    def setUpTestData(self):
        g = Item(name= , imageId=, gender=, category=, price=, \
            ingredients=, ingredient_string=, monthly_sales=)

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

