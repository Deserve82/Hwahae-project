from django.shortcuts import render
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
    include_ingredient = request.GET.get("include_ingredient")
    exclude_ingredient = request.GET.get("exclude_ingredient")

    for item in items:
        oily_point = 0
        for id in item.ingredients.all():
            oily_point += id.oily
        print(oily_point)
    ctx = {}
    return JsonResponse(ctx) 

def product_detail(request):
    ctx = {}
    return JsonResponse(ctx)   
