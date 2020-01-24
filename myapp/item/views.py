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
        Error_non_skin_type = "please let me know your skin_type!"
        return HttpResponse(Error_non_skin_type)
    elif skin_type == "oily":
        items = list_oily_type(ingredients, category, page, include_ingredient, exclude_ingredient)
    elif skin_type == "dry":
        items = list_dry_type(ingredients, category, page, include_ingredient, exclude_ingredient)
    elif skin_type == "sensitivity":
        items = list_sensitivity_type(ingredients, category, page, include_ingredient, exclude_ingredient)
    
    response_values = []
    for item in items:
        response_values.append({"id" : item.id,
                            "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"+item.imageId+".jpg",
                            "name" : item.name,
                            "price" : item.price,
                            "ingredients" : item.ingredient_string ,
                            "monthlySales": item.monthlySales})
    
    return HttpResponse(json.dumps(response_values, indent=4, ensure_ascii=False),
         content_type="application/json")

def product_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    skin_type = request.GET.get("skin_type")
    
    if skin_type is None:
        Error_non_skin_type = "please let me know your skin_type!"
        return HttpResponse(Error_non_skin_type)
    elif skin_type == "oily":
        recomened_items = Item.objects.annotate(oily_point=Sum('ingredients__oily')).order_by('-oily_point', 'price')
    elif skin_type == "dry":
        recomened_items = Item.objects.annotate(dry_point=Sum('ingredients__dry')).order_by('-dry_point', 'price')
    elif skin_type == "sensitivity":
        recomened_items = Item.objects.annotate(sensitivity_point=Sum('ingredients__sensitivity')).order_by('-sensitivity_point', 'price')
    
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

def list_oily_type(ingredients, category, page, include_ingredient, exclude_ingredient):
    order_by_oily = Item.objects.annotate(oily_point=Sum('ingredients__oily')).order_by('-oily_point', 'price')

    if category:
        order_by_oily = order_by_oily.filter(category=category)
    
    if include_ingredient:
        include_list = ingredients.filter(name__in=include_ingredient)
        order_by_oily = order_by_oily.filter(ingredients__in=include_list).distinct()
        order_by_oily = order_by_oily.filter(reduce(and_, (Q(ingredient_string__contains=c.name) for c in include_list)))
    
    if exclude_ingredient:
        exclude_list = ingredients.filter(name__in=exclude_ingredient)
        order_by_oily = order_by_oily.exclude(ingredients__in=exclude_list).distinct()

    paginator = Paginator(order_by_oily, 50)
    try:
        order_by_oily = paginator.get_page(page)
    except PageNotAnInteger:
        order_by_oily = paginator.get_page(1)
    except EmptyPage:
        order_by_oily = Paginator.get_page(paginator.num_pages)
    return order_by_oily

def list_dry_type(ingredients, category, page, include_ingredient, exclude_ingredient):
    order_by_dry = Item.objects.annotate(dry_point=Sum('ingredients__dry')).order_by('-dry_point', 'price')

    if category:
        order_by_dry = order_by_dry.filter(category=category)
    
    if include_ingredient:
        include_list = ingredients.filter(name__in=include_ingredient)
        order_by_oily = order_by_oily.filter(ingredients__in=include_list).distinct()
        order_by_oily = order_by_oily.filter(reduce(and_, (Q(ingredient_string__contains=c.name) for c in include_list)))
    
    if exclude_ingredient:
        exclude_list = ingredients.filter(name__in=exclude_ingredient)
        order_by_oily = order_by_oily.exclude(ingredients__in=exclude_list).distinct()

    paginator = Paginator(order_by_dry, 50)
    try:
        order_by_dry = paginator.get_page(page)
    except PageNotAnInteger:
        order_by_dry = paginator.get_page(1)
    except EmptyPage:
        order_by_dry = Paginator.get_page(paginator.num_pages)

    return order_by_dry

def list_sensitivity_type(ingredients, category, page, include_ingredient, exclude_ingredient):
    order_by_sensitivity = Item.objects.annotate(sensitivity_point=Sum('sensitivity__dry')).order_by('-sensitivity_point', 'price')

    if category:
        order_by_sensitivity = order_by_sensitivity.filter(category=category)
    
    if include_ingredient:
        include_list = ingredients.filter(name__in=include_ingredient)
        order_by_sensitivity = order_by_sensitivity.filter(ingredients__in=include_list).distinct()
        order_by_sensitivity = order_by_sensitivity.filter(reduce(and_, (Q(ingredient_string__contains=c.name) for c in include_list)))
    
    if exclude_ingredient:
        exclude_list = ingredients.filter(name__in=exclude_ingredient)
        order_by_sensitivity = order_by_sensitivity.exclude(ingredients__in=exclude_list).distinct()

    paginator = Paginator(order_by_dry, 50)
    try:
        order_by_sensitivity = paginator.get_page(page)
    except PageNotAnInteger:
        order_by_sensitivity = paginator.get_page(1)
    except EmptyPage:
        order_by_sensitivity = Paginator.get_page(paginator.num_pages)
    
    return order_by_sensitivity
