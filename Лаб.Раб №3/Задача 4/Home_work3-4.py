from bs4 import BeautifulSoup
import re
import json

def get_file(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = file.read()
        items = list()

        soup = BeautifulSoup(text, 'xml')
        products = soup.find_all('clothing')


        for product in products:
            item = dict()

            if product.find('id') != None:
                item['id'] = product.find('id').get_text().strip()
            else:
                item['id'] = 'NAN'
            if product.find('name') != None:
                item['name'] = product.find('name').get_text().strip()
            else:
                item['name'] = 'NAN'
            if product.find('size') != None:
                item['size'] = product.find('size').get_text().strip()
            else:
                item['size'] = 'NAN'
            if product.find('color') != None:
                item['color'] = product.find('color').get_text().strip()
            else:
                item['color'] = 'NAN'
            if product.find('material') != None:
                item['material'] = product.find('material').get_text().strip()
            else:
                item['material'] = 'NAN'
            if product.find('price') != None:
                item['price'] = int(product.find('price').get_text().strip())
            else:
                item['price'] = 'NAN'
            if product.find('rating') != None:
                item['rating'] = float(product.find('rating').get_text().strip())
            else:
                item['rating'] = 'NAN'
            if product.find('reviews') != None:
                item['reviews'] = product.find('reviews').get_text().strip()
            else:
                item['reviews'] = 'NAN'
            if product.find('category') != None:
                item['category'] = product.find('category').get_text().strip()
            else:
                item['category'] = 'NAN'
            if product.find('exclusive') != None:
                item['exclusive'] = product.find('exclusive').get_text().strip()
            else:
                item['exclusive'] = 'NAN'
            if product.find('new') != None:
                item['new'] = product.find('new').get_text().strip()
            else:
                item['new'] = 'NAN'
            if product.find('sporty') != None:
                item['sporty'] = product.find('sporty').get_text().strip()
            else:
                item['sporty'] = 'NAN'


            items.append(item)


        return items

result_items = []


for i in range(1, 101):
    file_name = f"{i}.xml"
    result_items += get_file(file_name)

result_items = sorted(result_items, key=lambda x: x['rating'], reverse=False)
with open("Sorted_stars.json", "w") as f:
    f.write(json.dumps(result_items))

sorted_result_items = list()
for i in result_items:
    if i['rating'] > 4.2:
        sorted_result_items.append(i['rating'])

for i in sorted_result_items:
    print(len(sorted_result_items), i)

####################

summ = 0
max_rating = float(sorted_result_items[0])
min_rating = float(sorted_result_items[0])
count = 0

for i in sorted_result_items:
    summ += float(i)
    if float(i) > max_rating:
        max_rating = float(i)
    elif float(i) < min_rating:
        min_rating = float(i)
    average = float(summ / len(sorted_result_items))

print(f"\t max_rating = {max_rating} \n\t average_count = {average} \n\t min_rating = {min_rating}")