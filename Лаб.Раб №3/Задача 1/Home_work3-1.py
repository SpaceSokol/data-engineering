from collections import Counter
from bs4 import BeautifulSoup
import re
import json


def get_file(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""

        for line in file.readlines():
            text += line

        html_str = BeautifulSoup(text, 'html.parser')

        item = dict()
        # print(html_str.find_all("span", string=re.compile("Тип:"))[0].get_text().split(":")[1].strip())

        item['Type'] = html_str.find_all("span", string=re.compile("Тип:"))[0].get_text().split(":")[1].strip()
        item['Title'] = html_str.find_all("h1")[0].get_text().split(":")[1].strip()
        town_and_start = html_str.find_all("p")[0].get_text().split("Начало:")
        item['City'] = town_and_start[0].split(":")[1].strip()
        item['Start'] = float(town_and_start[1].strip())
        item['tournaments'] = int(
            html_str.find_all("span", string=re.compile("Количество туров:"))[0].get_text().split(":")[1].strip())
        item['Control_time'] = \
        html_str.find_all("span", string=re.compile("Контроль времени:"))[0].get_text().split((":"))[1].strip()
        item['Min_rating'] = \
        html_str.find_all("span", string=re.compile("Минимальный рейтинг для участия:"))[0].get_text().split((":"))[
            1].strip()
        item['IMG'] = html_str.find_all("img")[0]['src']
        item['Rating'] = float(
            html_str.find_all("span", string=re.compile("Рейтинг:"))[0].get_text().split((":"))[1].strip())
        item['Views'] = int(
            html_str.find_all("span", string=re.compile("Просмотры:"))[0].get_text().split((":"))[1].strip())
        # print( item['Control_time'])

    return item


get_file("1.html")
result_items = []

for i in range(1, 1000):
    file_name = f"{i}.html"
    result_items.append(get_file(file_name))

result_items = sorted(result_items, key=lambda x: x['Rating'], reverse=True)
with open("Sorted_Raiting.json", "w") as f:
    f.write(json.dumps(result_items))

filtered_views = []

for view in result_items:
    if view['Views'] > 50000:
        filtered_views.append(view['Views'])

summ = 0
max_number = filtered_views[0]
min_number = filtered_views[0]
i = 0

for count in filtered_views:
    summ += count
    if (count > max_number):
        max_number = count
        i += 1
    elif (count < min_number):
        min_number = count
        i += 1
    average_numb = summ / len(filtered_views)

print(f"\t max_number = {max_number} \n\t average count = {average_numb} \n\t min_number = {min_number}")

with open("filtered_views.json", "w") as f:
    f.write(json.dumps(filtered_views))

# print(filtered_views)
# print(len(filtered_views))
