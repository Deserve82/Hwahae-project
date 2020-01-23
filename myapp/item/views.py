from django.shortcuts import render
from django.db.models import Sum, Count, Q
from operator import and_
from functools import reduce
from .models import Item, Ingredient
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request):
    items = Item.objects.all().order_by("id")
    ingredients = Ingredient.objects.all()
    paginator = Paginator(items, 50)

    skin_type = request.GET.get("skin_type")
    category = request.GET.get("category")
    page = request.GET.get("page")
    include_ingredient = request.GET.get("include_ingredient").split(',')
    exclude_ingredient = request.GET.get("exclude_ingredient")

    
    order_by_oily = Item.objects.annotate(oily_point=Sum('ingredients__oily')).order_by('-oily_point', 'price').filter(category=category)
    order_by_dry = Item.objects.annotate(dry_point=Sum('ingredients__dry')).order_by('-dry_point', 'price')
    order_by_sensitivity = Item.objects.annotate(sensitivity_point=Sum('ingredients__sensitivity')).order_by('-sensitivity_point', 'price')
    
    include_list = ingredients.filter(name__in=include_ingredient)
    #exclude_list = ingredients.filter(name__in=exclude_ingredient)
    order_by_oily = order_by_oily.filter(ingredients__in=include_list).distinct()
    #order_by_oily = order_by_oily.filter(reduce(and_, (Q(ingredient_string__contains=c.name) for c in include_list)))
    #order_by_oily = order_by_oily.exclude(ingredients__in=exclude_list)

    #test
    for i in order_by_oily:
        print(i.name, i.ingredient_string)
    ctx = {}
    return JsonResponse(ctx) 

def product_detail(request):
    ctx = {}
    return JsonResponse(ctx)   
