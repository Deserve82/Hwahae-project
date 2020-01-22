import json

with open('myapp\\item\\fixtures\\ingredient-data.json', 'r', encoding='UTF8') as f:
    ingre_data = json.load(f)
name_pk = []
for i in ingre_data:
    name_pk.append([i['fields']['name'], i['pk']])
with open('myapp\\item\\fixtures\\item-data.json', 'r', encoding='UTF8') as f:
    json_data = json.load(f)
for data in json_data:
    ingredient_name = data['fields']['ingredients'].split(',')
    temp = []
    for name in ingredient_name:
        for i in name_pk:
            if name == i[0]:
                temp.append(i[1])
    data['fields']['ingredients'] = temp

jstring = json.dumps(json_data, indent=4, ensure_ascii=False)
f = open('myapp\\item\\fixtures\\item-data.json', 'w', encoding='UTF8')
f.write(jstring)
f.close()

#model_field_type_item = []
#count = 0
#for data in json_data:
#    count += 1
#    temp_dict = {
#        "pk": count,
#        "model":"item.item",
#        "fields": data
#    }
#    model_field_type_item.append(temp_dict)

#jstring = json.dumps(model_field_type_item, indent=4, ensure_ascii=False)
#f = open('myapp\\item\\fixtures\\item-data.json', 'w', encoding='UTF8')
#f.write(jstring)
#f.close()



#with open('myapp\\item\\fixtures\\ingredient-data.json', 'r', encoding='UTF8') as f:
#    json_data = json.load(f)
#for data in json_data:
#    print(data)

#model_field_type_ingredient = []
#count = 0
#for data in json_data:
#    count += 1
#    temp_dict = {
#        "pk": count,
#        "model":"item.ingredient",
#        "fields": data
#    }
#    model_field_type_ingredient.append(temp_dict)

#jstring = json.dumps(model_field_type_ingredient, indent=4)
#f = open('myapp\\item\\fixtures\\ingredient-data.json', 'w')
#f.write(jstring)
#f.close()
