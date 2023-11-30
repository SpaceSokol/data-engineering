from bs4 import BeautifulSoup
import re
import json


def get_file(file_name):
    items = list()
    with open(file_name, encoding="utf-8") as file:
        text = ""


        for line in file.readlines():
            text += line

        items = list()

        xml_str = BeautifulSoup(text, 'xml')
        item = dict()

        for i in xml_str:
            item['name'] = xml_str.find_all('name')[0].get_text().strip()
            item['constellation'] = xml_str.find_all('constellation')[0].get_text().strip()
            item['spectral-class'] = xml_str.find_all('spectral-class')[0].get_text().strip()
            item['radius'] = xml_str.find_all('radius')[0].get_text().strip()
            item['rotation'] = xml_str.find_all('rotation')[0].get_text().strip()
            item['age'] = xml_str.find_all('age')[0].get_text().strip()
            item['distance'] = xml_str.find_all('distance')[0].get_text().strip()
            item['absolute-magnitude'] = xml_str.find_all('absolute-magnitude')[0].get_text().strip()

            items.append(item)


    return items

result_items = []

for i in range(1, 501):
    file_name = f"{i}.xml"
    #get_file(file_name)
    result_items += get_file(file_name)

#print(result_items)
#print(len(sorted_result_items))

result_items = sorted(result_items, key=lambda x: x['radius'], reverse=True)
with open("Sorted_stars.json", "w") as f:
    f.write(json.dumps(result_items))

sorted_result_items = list()
for i in result_items:
    if int(i['radius']) > 500_000_000:  # 500 миллионов
        sorted_result_items.append(i['radius'])

summ = 0
max_radius = int(sorted_result_items[0])
min_radius = int(sorted_result_items[0])
count = 0

for i in sorted_result_items:
    summ += int(i)
    if int(i) > max_radius:
        max_radius = int(i)
    elif int(i) < min_radius:
        min_radius = int(i)
    average = summ / len(sorted_result_items)

print(f"\t max_number = {max_radius} \n\t average_count = {average} \n\t min_number = {min_radius}")

# print(sorted_result_items)
# print(len(sorted_result_items))

