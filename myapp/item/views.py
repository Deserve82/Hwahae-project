import json
from django.shortcuts import render
from .models import Item, Ingredient, input_skin_type, filt_by_types
from django.http import HttpResponse


def item_list(request):
    """
    상품 목록을 반환하는 함수입니다. Model은 Item, Ingredient 둘 다 사용했습니다.
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
    
    if skin_type is None:
        # skin_type을 선택하지 않았을 때를 가정했습니다.
        non_skin_type_error = "please let me know your skin_type!"
        return HttpResponse(non_skin_type_error)

    elif skin_type == "oily" or skin_type == "dry" or skin_type == "sensitive":
        # input_skin_type은 먼저 위에서 받은 스킨타입에 따른 우선순위 정렬을 위한 함수입니다.
        items = input_skin_type(Item, skin_type, recommend=False)
    
    else:
        # skin_type을 잘못 입력 했을 경우를 가정 했습니다.
        wrong_skin_type_error = "please check your skin type again!"
        return HttpResponse(wrong_skin_type_error)

    # item_list는 위 items에서 받은 쿼리들을 카테고리, 페이지, 포함성분, 제외성분을 통해 걸러주는 작업을 합니다.
    item_list = list(filt_by_types(items, ingredients, category, page, include_ingredient, exclude_ingredient))

    # 빈 list에 값을 가공하여 반환 값들을 넣어주는 작업을 합니다.
    response_values = []
    for item in item_list:
        response_values.append({"id" : item.id,
                            "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"\
                                        +item.imageId+".jpg",
                            "name" : item.name,
                            "price" : item.price,
                            "ingredients" : item.ingredient_string ,
                            "monthlySales": item.monthly_sales,
                            })

    # django debug tool-bar용 리턴 입니다. 주석처리를 해제하면 밑에 return 값을 주석 처리 해주세요.
    # return render(request, 'list.html',{'response_values':response_values})
    
    return HttpResponse(json.dumps(response_values, indent=4, ensure_ascii=False),
                        content_type="application/json")

def item_detail(request, item_id):
    """
    특정 상품 Id를 받고 그 상품 detail을 반환하는 함수입니다. 
    또한 스킨타입에 따라 추천 상품 3가지도 같이 반환합니다. GET으로 받는 Parameter 들은 스킨타입이 있습니다.
    """
    # 특정 id를 통해 쉽게 상품 정보를 받아 옵니다. 상품이 없는 id를 입력한다면 예외처리를 합니다.
    try:
        item = Item.objects.get(id=item_id)
    except:
        non_match_item_id_error = "there'no matching item"
        return HttpResponse(non_match_item_id_error)

    # 위 'product_list' 함수와 마찬가지로 response_values 리스트에 가공해 넣어줍니다.
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
    skin_type = request.GET.get("skin_type")

    if skin_type is None:
        non_skin_type_error = "please let me know your skin_type!"
        return HttpResponse(non_skin_type_error)

    elif skin_type == "oily" or skin_type == "dry" or skin_type == "sensitive":
        recomened_items = list(input_skin_type(Item, skin_type, recommend=True))

    else:
        wrong_skin_type_error = "please check your skin type again!"
        return HttpResponse(wrong_skin_type_error)

    for item in recomened_items:
        r_item = {
            "id": item.id,
            "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"\
                        +item.imageId+".jpg",
            "name": item.name,
            "price": item.price
        }
        response_values.append(r_item)

    # django debug tool-bar용 리턴 입니다. 주석처리를 해제하면 밑에 return 값을 주석 처리 해주세요.
    # return render(request, 'detail.html',{'response_values':response_values})

    return HttpResponse(json.dumps(response_values, indent=4, ensure_ascii=False),
                         content_type="application/json")
    



