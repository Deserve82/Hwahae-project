import json
from django.shortcuts import render
from django.db.models import Sum, Q
from operator import and_
from functools import reduce
from .models import Item, Ingredient
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request):
    """
    상품 목록을 반환하는 함수, Model은 Item, Ingredient 둘 다 사용했습니다.
    GET으로 받는 Parameter 들은 스킨타입, 카테고리, 페이지, 포함 성분, 제외 성분이 있습니다.
    """
    ingredients = Ingredient.objects.all()
    skin_type = request.GET.get("skin_type")
    category = request.GET.get("category")
    page = request.GET.get("page")

    # 포함 성분을 분류하기 쉽게 list형식으로 받습니다.
    try:
        include_ingredient = request.GET.get("include_ingredient").split(',')
    # 만약 성분이 없다면 빈 list를 넣습니다.
    except:
        include_ingredient = []
    
    # 제외 성분 역시 분류하기 쉽게 list형식으로 받습니다.
    try:
        exclude_ingredient = request.GET.get("exclude_ingredient").split(',')
    # 마찬가지로 성분이 없다면 빈 list를 통해 아무것도 거르지 않습니다.
    except:
        exclude_ingredient = []
    
    # items는 먼저 위에서 받은 스킨타입에 따른 우선순위 정렬을 위한 함수입니다.
    items = input_skin_type(skin_type)
    # item_list는 위 items에서 받은 것들을 카테고리, 페이지, 포함성분, 제외성분을 통해 걸러주는 작업을 합니다.
    item_list = filt_by_types(items, ingredients, category, page, include_ingredient, exclude_ingredient)

    # 빈 list에 반환 값들을 넣어주는 작업을 합니다.
    response_values = []
    for item in item_list:
        response_values.append({"id" : item.id,
                            "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"\
                                        +item.imageId+".jpg",
                            "name" : item.name,
                            "price" : item.price,
                            "ingredients" : item.ingredient_string ,
                            "monthlySales": item.monthlySales,
                            })
    
    return HttpResponse(json.dumps(response_values, indent=4, ensure_ascii=False),
         content_type="application/json")

def product_detail(request, item_id):
    """
    특정 상품 Id를 받고 그 상품 detail을 반환하는 함수입니다. 
    또한 스킨타입에 따라 추천 상품 3가지도 같이 반환합니다. GET으로 받는 Parameter 들은 스킨타입이 있습니다.
    """
    # 특정 id를 통해 쉽게 상품 정보를 받아 옵니다.
    item = Item.objects.get(id=item_id)
    skin_type = request.GET.get("skin_type")

    # 위 'product_list' 함수와 마찬가지로 빈 리스트에 가공해 넣어줍니다.
    response_values = []
    item_detail = {
        "id": item.id,
        "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/" \
                    +item.imageId+".jpg",
        "name": item.name,
        "price": item.price,
        "gender": item.gender,
        "category": item.category,
        "ingredients": item.ingredient_string,
        "monthlySales": item.monthly_sales
    }
    response_values.append(item_detail)

    # 'recomened_items' 이라는 변수에 스킨타입에 따른 추천 순위를 3개 넣어줍니다.
    recomened_items = input_skin_type(skin_type)
    count = 0
    for item in recomened_items:
        count += 1
        r_item = {
            "id": item.id,
            "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"\
                        +item.imageId+".jpg",
            "name": item.name,
            "price": item.price
        }
        if count > 3:
            break
        else:
            response_values.append(r_item)
    return HttpResponse(json.dumps(response_values, indent=4, ensure_ascii=False),
         content_type="application/json")


def input_skin_type(skin_type):
    # skin_type에 따른 추천 순위를 적용한 Item들을 반환하는 함수입니다.

    if skin_type is None:
        # skin_type을 선택하지 않았을 때를 가정했습니다.
        non_skin_type_Error = "please let me know your skin_type!"
        return HttpResponse(non_skin_type_Error)

    elif skin_type == "oily":
        oily_items = Item.objects.annotate(oily_point=Sum('ingredients__oily'))\
                                                .order_by('-oily_point', 'price')
        return oily_items

    elif skin_type == "dry":
        dry_items = Item.objects.annotate(dry_point=Sum('ingredients__dry'))\
                                                .order_by('-dry_point', 'price')
        return dry_items

    elif skin_type == "sensitivity":
        sensitivity_items = Item.objects.annotate(sensitivity_point=Sum('ingredients__sensitivity'))\
                                                .order_by('-sensitivity_point', 'price')
        return sensitivity_items

    else:
        # skin_type을 잘못 입력 했을 경우를 가정 했습니다.
        wrong_skin_type_Error = "please check your skin type again!"
        return HttpResponse(wrong_skin_type_Error)
    

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
        include_list = ingredients.filter(name__in=include_ingredient)
        items = items.filter(ingredients__in=include_list).distinct()
        items = items.filter(reduce(and_, (Q(ingredient_string__contains=ingredient.name) \
                                            for ingredient in include_list)))
    
    # 제외 성분은 OR 형식이기 때문에 __in을 통해 한 번만 걸렀습니다.
    if exclude_ingredient:
        exclude_list = ingredients.filter(name__in=exclude_ingredient)
        items = items.exclude(ingredients__in=exclude_list).distinct()

    # 입력받은 page 번호를 통해 이동 할 수 있게 만들었습니다. 또한 페이지가 정수가 아닐 때, 비었을 때를 고려했습니다.
    paginator = Paginator(items, 50)
    try:
        items = paginator.get_page(page)
    except PageNotAnInteger:
        items = paginator.get_page(1)
    except EmptyPage:
        items = Paginator.get_page(paginator.num_pages)
    
    return items


