from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    oily = models.IntegerField(default=0)
    dry = models.IntegerField(default=0)
    sensitivity = models.IntegerField(default=0)

class Item(models.Model):
    imageId = models.CharField(max_length=37, null=True)
    name = models.CharField(max_length=32)

    GENDER_CHOICES = [
        ('M', 'male'),
        ('F', 'female'),
        ('A', 'all')
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='A',
    )

    BASE_MAKE_UP = 'basemakeup'
    SUN_CARE = 'suncare'
    MASK_PACK = 'maskpack'
    SKIN_CARE = 'skincare'
    CATEGORY_CHOICES = [
        (BASE_MAKE_UP, 'basemakeup'),
        (SUN_CARE, 'suncare'),
        (MASK_PACK, 'maskpack'),
        (SKIN_CARE, 'skincare'),
    ]
    category = models.CharField(
        max_length=32,
        choices=CATEGORY_CHOICES,
        default=None,
    )

    price = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient)
    ingredient_string = models.CharField(max_length=150, null=True)
    monthlySales = models.IntegerField(default=0)

    @property
    def get_oily_point(self):
        oily_point = 0
        for ingredient in self.ingredients.all():
            oily_point += ingredient.oily
        return oily_point