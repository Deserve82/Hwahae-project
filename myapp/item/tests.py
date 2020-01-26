from django.test import TestCase
from .models import Item, Ingredient
# Create your tests here.

class ItemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        ingredient1 = Ingredient.objects.create(name='한글도', oily=1, dry=-1, sensitivity=0)
        ingredient2 = Ingredient.objects.create(name='시험해', oily=-1, dry=1, sensitivity=1)
        ingredient3 = Ingredient.objects.create(name='보자', oily=0, dry=-1, sensitivity=0)
        ingredient1.save()
        ingredient2.save()
        ingredient3.save()
        item1 = Item.objects.create(name='코리아나더숨딸기엠플마스크팩! Reboot Ver.[100]', category='maskpack', 
                    imageId='dsfkajdlfijlkf12903123', gender='all', price=1000000, 
                    ingredient_string = ingredient1.name+','+ingredient2.name+','+ingredient3.name,
                    monthly_sales=10000
                    )
        item2 = Item.objects.create(name='item2', category='skincare', 
                    imageId='ddddddddddddddddddddd23', gender='all', price=10, 
                    ingredient_string = ingredient1.name+','+ingredient2.name ,
                    monthly_sales=100001
                    )
        item1 = item1.ingredients.add(ingredient1, ingredient2, ingredient3)
        item2 = item1.ingredients.add(ingredient1, ingredient2)

    def test_ingredient_oily_field(self):
        ingredient = Ingredient.objects.get(id=1)
        name = ingredient._meta.get_field('oily').verbose_name
        self.assertEquals(name, 'oily')
    
    def test_ingredient_dry_field(self):
        ingredient = Ingredient.objects.get(id=1)
        name = ingredient._meta.get_field('dry').verbose_name
        self.assertEquals(name, 'dry')
    
    def test_ingredient_sensitivity_field(self):
        ingredient = Ingredient.objects.get(id=1)
        name = ingredient._meta.get_field('sensitivity').verbose_name
        self.assertEquals(name, 'sensitivity')

    def test_ingredient_name_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('name').max_length
        self.assertEquals(max_length, 32)

    def test_item_name_field(self):
        item = Item.objects.get(id=1)
        name = item._meta.get_field('name').verbose_name
        self.assertEquals(name, 'name')

    def test_item_name_length(self):
        item = Item.objects.get(id=1)
        max_length = item._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)
    
    def test_item_category_field(self):
        item = Item.objects.get(id=1)
        name = item._meta.get_field('category').verbose_name
        self.assertEquals(name, 'category')

    def test_item_category_length(self):
        item = Item.objects.get(id=1)
        max_length = item._meta.get_field('category').max_length
        self.assertEquals(max_length, 32)

    def test_item_gender_field(self):
        item = Item.objects.get(id=1)
        gender = item._meta.get_field('gender').verbose_name
        self.assertEquals(gender, 'gender')

    def test_item_gender_length(self):
        item = Item.objects.get(id=1)
        max_length = item._meta.get_field('gender').max_length
        self.assertEquals(max_length, 10)

    def test_ingredient_string(self):
        item = Item.objects.get(id=1)
        ingredient_string = item.ingredient_string
        self.assertEquals(ingredient_string, '한글도,시험해,보자')