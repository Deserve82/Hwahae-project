import json
from django.shortcuts import render
from django.db.models import Sum, Q
from operator import and_
from functools import reduce
from .models import Item, Ingredient
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request):
    ingredients = Ingredient.objects.all()

    skin_type = request.GET.get("skin_type")
    category = request.GET.get("category")
    page = request.GET.get("page")

    try:
        include_ingredient = request.GET.get("include_ingredient").split(',')
    except:
        include_ingredient = []
        
    try:
        exclude_ingredient = request.GET.get("exclude_ingredient").split(',')
    except:
        exclude_ingredient = []
    
    if skin_type is None:
        non_skin_type_Error = "please let me know your skin type!"
        return HttpResponse(non_skin_type_Error)
    elif skin_type == "oily":
        items = Item.objects.annotate(oily_point=Sum('ingredients__oily')).order_by('-oily_point', 'price')
    elif skin_type == "dry":
        items = Item.objects.annotate(dry_point=Sum('ingredients__dry')).order_by('-dry_point', 'price')
    elif skin_type == "sensitivity":
        items = Item.objects.annotate(sensitivity_point=Sum('ingredients__sensitivity')).order_by('-sensitivity_point', 'price')
    else:
        wrong_skin_type_Error = "please check your skin type again!"
        return HttpResponse(wrong_skin_type_Error)

    item_list = filt_by_types(items, ingredients, category, page, include_ingredient, exclude_ingredient)

    response_values = []
    for item in item_list:
        response_values.append({"id" : item.id,
                            "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"+item.imageId+".jpg",
                            "name" : item.name,
                            "price" : item.price,
                            "ingredients" : item.ingredient_string ,
                            "monthlySales": item.monthlySales,
                            })
    
    return HttpResponse(json.dumps(response_values, indent=4, ensure_ascii=False),
         content_type="application/json")

def product_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    skin_type = request.GET.get("skin_type")
    
    if skin_type is None:
        error_non_skin_type = "please let me know your skin_type!"
        return HttpResponse(error_non_skin_type)
    elif skin_type == "oily":
        recomened_items = Item.objects.annotate(oily_point=Sum('ingredients__oily')).order_by('-oily_point', 'price')
    elif skin_type == "dry":
        recomened_items = Item.objects.annotate(dry_point=Sum('ingredients__dry')).order_by('-dry_point', 'price')
    elif skin_type == "sensitivity":
        recomened_items = Item.objects.annotate(sensitivity_point=Sum('ingredients__sensitivity')).order_by('-sensitivity_point', 'price')
    else:
        error_wrong_skin_type = "please check your skin type again!"
        return HttpResponse(error_wrong_skin_type)

    response_values = []
    item_detail = {
        "id": item.id,
        "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/"+item.imageId+".jpg",
        "name": item.name,
        "price": item.price,
        "gender": item.gender,
        "category": item.category,
        "ingredients": item.ingredient_string,
        "monthlySales": item.monthlySales
    }
    response_values.append(item_detail)

    count = 0
    for item in recomened_items:
        count += 1
        r_item = {
            "id": item.id,
            "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"+item.imageId+".jpg",
            "name": item.name,
            "price": item.price
        }
        if count>3:
            break
        else:
            response_values.append(r_item)
    return HttpResponse(json.dumps(response_values, indent=4, ensure_ascii=False),
         content_type="application/json")

def filt_by_types(items, ingredients, category, page, include_ingredient, exclude_ingredient):

    if category:
        items = items.filter(category=category)
    
    if include_ingredient:
        include_list = ingredients.filter(name__in=include_ingredient)
        items = items.filter(ingredients__in=include_list).distinct()
        items = items.filter(reduce(and_, (Q(ingredient_string__contains=c.name) for c in include_list)))
    
    if exclude_ingredient:
        exclude_list = ingredients.filter(name__in=exclude_ingredient)
        items = items.exclude(ingredients__in=exclude_list).distinct()

    paginator = Paginator(items, 50)
    try:
        items = paginator.get_page(page)
    except PageNotAnInteger:
        items = paginator.get_page(1)
    except EmptyPage:
        items = Paginator.get_page(paginator.num_pages)
    
    return items