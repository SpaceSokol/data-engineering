from bs4 import BeautifulSoup
import re
import json


def get_file(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""

        for line in file.readlines():
            text += line


        items = list()
        html_str = BeautifulSoup(text, 'html.parser')
        products = html_str.find("div", attrs={'class':"product-item"})
        #print(products)

        for product in products:
            item = dict()
            # print(html_str.find_all("span", string=re.compile("Тип:"))[0].get_text().split(":")[1].strip())

            item['id'] = products.a["data-id"]
            item['link'] = products.find_all('a')[1]['href']
            item['Image_url'] = products.find_all("img")[0]['src']
            item['title'] = products.find_all("span")[0].get_text().strip()
            item['price'] = int(products.price.get_text().replace("₽", "").replace(" ", "").strip())
            item['bonus'] = int(products.strong.get_text().replace("+ начислим ", "").replace(" бонусов", "").strip())

            props = products.ul.find_all("li")
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)

    return items

result_items = []

for i in range(1, 75):
    file_name = f"{i}.html"
    result_items += get_file(file_name)

result_items = sorted(result_items, key=lambda x: x['price'], reverse=True)
with open("Sorted_Price.json", "w") as f:
    f.write(json.dumps(result_items))

sorted_result_items = list()
for i in result_items:
    if i['price'] > 480000:
        sorted_result_items.append(i['price'])

#print(sorted_result_items)
#print(len(sorted_result_items))

summ = 0
max_number = sorted_result_items[0]
min_number = sorted_result_items[0]
count = 0

for i in sorted_result_items:
    summ += i
    if i > max_number:
        max_number = i
    elif i < min_number:
        min_number = i
    average = summ / len(sorted_result_items)


print(f"\t max_number = {max_number} \n\t average_count = {average} \n\t min_number = {min_number}")

with open("filtered_price.json", "w") as f:
    f.write(json.dumps(sorted_result_items))
    f.write(json.dumps(f"\t max_number = {max_number}, average_count = {average}, min_number = {min_number}"))




#get_file("2.html")
#result_items = []

#print(result_items)
