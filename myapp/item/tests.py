from django.test import TestCase
from .models import Item, Ingredient, filt_by_types, input_skin_type
# Create your tests here.

class ItemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        ingredient1 = Ingredient.objects.create(name='한글도', oily=1, dry=-1, sensitivity=1)
        ingredient2 = Ingredient.objects.create(name='시험해', oily=-1, dry=1, sensitivity=1)
        ingredient3 = Ingredient.objects.create(name='보자', oily=1, dry=-1, sensitivity=-1)
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
        item3 = Item.objects.create(name='item3', category='suncare', 
                    imageId='d23', gender='male', price=1, 
                    ingredient_string = ingredient3.name,
                    )

        item1 = item1.ingredients.add(ingredient1, ingredient2, ingredient3)
        item2 = item2.ingredients.add(ingredient1, ingredient2)
        item3 = item3.ingredients.add(ingredient3)
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

    def test_item_price_field(self):
        item = Item.objects.get(id=1)
        price = item._meta.get_field('price').verbose_name
        self.assertEquals(price, 'price')
    
    def test_item_monthly_sales_field(self):
        item = Item.objects.get(id=1)
        monthly_sales = item._meta.get_field('monthly_sales').verbose_name
        self.assertEquals(monthly_sales, 'monthly sales')

    def test_ingredient_string_field(self):
        item = Item.objects.get(id=1)
        ingredient_string = item._meta.get_field('ingredient_string').verbose_name
        self.assertEquals(ingredient_string, 'ingredient string')

    def test_ingredient_string(self):
        item = Item.objects.get(id=1)
        ingredient_string = item.ingredient_string
        self.assertEquals(ingredient_string, '한글도,시험해,보자')
    
    def test_input_skin_type(self):
        # oily order test
        items = input_skin_type(Item, 'oily', recommend=False)

        item1 = Item.objects.get(id=1)
        # oily point = 1 , price = 1000000
        item2 = Item.objects.get(id=2)
        # oily point = 0
        item3 = Item.objects.get(id=3)
        # oily point = 1, price = 1

        self.assertEquals(items[0], item3)
        self.assertEquals(items[1], item1)
        self.assertEquals(items[2], item2)

        # dry order test
        items = input_skin_type(Item, 'dry', recommend=False)

        item1 = Item.objects.get(id=1)
        # dry point = -1 , price = 100000
        item2 = Item.objects.get(id=2)
        # dry point = 0
        item3 = Item.objects.get(id=3)
        # dry point = -1, price = 1

        self.assertEquals(items[0], item2)
        self.assertEquals(items[1], item3)
        self.assertEquals(items[2], item1)

        # sensitivity order test
        items = input_skin_type(Item, 'sensitivity', recommend=False)

        item1 = Item.objects.get(id=1)
        # sensitivity point = 1
        item2 = Item.objects.get(id=2)
        # sensitivity point = 2
        item3 = Item.objects.get(id=3)
        # sensitivity point = -1

        self.assertEquals(items[0], item2)
        self.assertEquals(items[1], item1)
        self.assertEquals(items[2], item3)
    
    def test_filt_by_types(self):
        items = Item.objects.all()
        ingredients = Ingredient.objects.all()
        category = None
        page = 1
        include_ingredient = ['한글도' , '시험해']
        exclude_ingredient = ['보자']
        item = filt_by_types(items, ingredients, category, page, include_ingredient, exclude_ingredient)
        filtered_item = Item.objects.get(id=2)
        self.assertEquals(item[0], filtered_item)

        category = 'suncare'
        page = None
        include_ingredient = []
        exclude_ingredient = []
        item = filt_by_types(items, ingredients, category, page, include_ingredient, exclude_ingredient)
        filtered_item = Item.objects.get(id=3)
        self.assertEqual(item[0], filtered_item)

        category = None
        page = None
        items = input_skin_type(Item, 'sensitivity', False)
        include_ingredient = ['한글도']
        exclude_ingredient = []
        item = filt_by_types(items, ingredients, category, page, include_ingredient, exclude_ingredient)
        filtered_item1 = Item.objects.get(id=2)
        filtered_item2 = Item.objects.get(id=1)
        self.assertEqual(item[0], filtered_item1)
        self.assertEqual(item[1], filtered_item2)
