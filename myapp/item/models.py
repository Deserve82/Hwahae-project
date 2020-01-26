from django.db import models
from django.db.models import Sum, Q
from functools import reduce
from operator import and_
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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

    imageId = models.CharField(max_length=60, null=True)
    name = models.CharField(max_length=100)

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
        default=ALL,
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
        max_length=12,
        choices=CATEGORY_CHOICES,
        default=None,
    )

    price = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient)
    ingredient_string = models.CharField(max_length=200, null=True)
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

    def __str__(self):
        return self.name


def input_skin_type(Item, skin_type, recommend):
    """
    skin_type에 따른 추천 순위를 적용한 Item들을 반환하는 함수입니다. 
    recommend=True 일 경우 3개만 따로 반환 합니다.
    """
    if skin_type == "oily":
        if recommend:
            oily_items = Item.objects.annotate(oily_point=Sum('ingredients__oily'))\
                                                    .order_by('-oily_point', 'price')[:3]
        else:
            oily_items = Item.objects.annotate(oily_point=Sum('ingredients__oily'))\
                                                    .order_by('-oily_point', 'price')
        return oily_items

    elif skin_type == "dry":
        if recommend:
            dry_items = Item.objects.annotate(dry_point=Sum('ingredients__dry'))\
                                                    .order_by('-dry_point', 'price')[:3]
        else:
            dry_items = Item.objects.annotate(dry_point=Sum('ingredients__dry'))\
                                                    .order_by('-dry_point', 'price')
        return dry_items

    elif skin_type == "sensitive":
        if recommend:
            sensitivity_items = Item.objects.annotate(sensitivity_point=Sum('ingredients__sensitivity'))\
                                                    .order_by('-sensitivity_point', 'price')[:3]
        else:
            sensitivity_items = Item.objects.annotate(sensitivity_point=Sum('ingredients__sensitivity'))\
                                                    .order_by('-sensitivity_point', 'price')
        return sensitivity_items

def filt_by_types(items, ingredients, category, page, include_ingredient, exclude_ingredient):
    """
     형태로 받은 include_ingredient를 filter를 통해 걸러주기 위해 받은 ingredients, 카테고리, 
     페이지, 포함 성분, 제외 성분을 통해 위 skin_type에 따라 걸렀던 items를 한 번 더 자료에 맞게 걸러줍니다.
    """
    # 만약 인자가 없다면 실행이 안되게 if 문을 사용했습니다.
    if category:
        items = items.filter(category=category)
    
    # 포함 성분은 AND형식으로 모두 포함되어야 하기 때문에 reduce와 Q를 통해 필터가 여러번 작동하게 했습니다.
    if include_ingredient:
        try:
            include_list = ingredients.filter(name__in=include_ingredient)
            items = items.filter(ingredients__in=include_list).distinct()
            items = items.filter(reduce(and_, (Q(ingredient_string__contains=ingredient.name) \
                                                for ingredient in include_list)))
        except:
            non_match_item = []
            return non_match_item
    
    # 제외 성분은 OR 형식이기 때문에 __in을 통해 한 번만 걸렀습니다.
    if exclude_ingredient:
        exclude_list = ingredients.filter(name__in=exclude_ingredient)
        items = items.exclude(ingredients__in=exclude_list).distinct()

    # paginator로 불러지는 query문을 최소화 하기 위해 리스트 형에 담는 것으로 자료형을 바꾸었습니다.
    items=list(items)
    paginator = Paginator(items, 50)
    try:
        items = paginator.get_page(page)
    except PageNotAnInteger:
        items = paginator.get_page(1)
    except EmptyPage:
        items = Paginator.get_page(paginator.num_pages)
    
    return items