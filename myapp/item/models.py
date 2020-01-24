from django.db import models

# Create your models here.
class Ingredient(models.Model):
    """
    성분 하나에 대한 정보 입니다. json을 가공해서 바로 Integer형식으로 입력 받게 끔 바꾸어 계산이 빠르고 쉽게 변했습니다.
    """
    name = models.CharField(max_length=32)
    oily = models.IntegerField(default=0)
    dry = models.IntegerField(default=0)
    sensitivity = models.IntegerField(default=0)

class Item(models.Model):
    """
    각 상품 하나에 대한 정보 입니다.
    name, imageId, gender, category, price, ingredients, ingredient_string, monthly_sales로 구성되어 있으며
    ingredients 는 m2m 필드로 포함되어 있는 성분들이 Ingredient 형태로 담겨 있습니다.
    ingredient_string은 filter를 좀 더 깔끔하게 사용하고 싶어 ingredients들의 name을 String 형태로 저장한 것입니다.
    또한 response할 때에도 빠르게 찾아 올 수 있어 포함 되어 있는 성분 자료를 두 개로 나누었습니다.
    """

    imageId = models.CharField(max_length=37, null=True)
    name = models.CharField(max_length=32)

    MALE = 'male'
    FEMALE = 'female'
    ALL = 'all'
    GENDER_CHOICES = [
        (MALE, 'male'),
        (FEMALE, 'female'),
        (ALL, 'all')
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
    monthly_sales = models.IntegerField(default=0)

    # 각 Item의 포함되어 있는 점수를 확인 할 수 있는 함수를 선언했습니다.
    @property
    def get_oily_point(self):
        oily_point = 0
        for ingredient in self.ingredients.all():
            oily_point += ingredient.oily
        return oily_point
    
    @property
    def get_dry_point(self):
        dry_point = 0
        for ingredient in self.ingredients.all():
            dry_point += ingredient.dry
        return dry_point
    
    @property
    def get_sensitivity_point(self):
        sensitivity_point = 0
        for ingredient in self.ingredients.all():
            sensitivity_point += ingredient.sensitivity
        return sensitivity_point