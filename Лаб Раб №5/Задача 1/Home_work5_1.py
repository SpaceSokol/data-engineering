from pymongo import MongoClient
import json

def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.person

def get_from_txt(filename):
    items = []
    with open("task_1_item.text", encoding="utf-8") as file:
        lines = file.readlines()
        item = dict()
        for line in lines:
            if line == "=====\n":
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                splitted = line.split("::")
                if splitted[0] in ['job', 'city']:
                    item[splitted[0]] = splitted[1]
                elif splitted[0] in ['salary', 'id', 'year', 'age']:
                    item[splitted[0]] = int(splitted[1])
    return items

def insert_many(collection, data):
    result = collection.insert_many(data) # many or one - если один объект
    print(result)



data = get_from_txt("task_1_item.text")
result_insert_many = insert_many(connect(), data)
with open("insert_data.json", "w") as file:
    file.write(json.dumps(result_insert_many))

def sort_by_salary(collection):
    for person in collection.find({}, limit=10).sort({'salary':-1}): # 1 - по возрастанию, -1 - по убыванию
        print(person)

result_sort_by_salary = sort_by_salary(connect())
with open("sort_by_salary.json", "w") as file:
    file.write(json.dumps(result_sort_by_salary))

def filter_by_age(collections):
    for person in collections.find({"age":30}, limit=15).sort({'salary':-1}):
        print(person)

result_filter_by_age =  filter_by_age(connect())
with open("filter_by_age.json", "w") as file:
    file.write(json.dumps(result_filter_by_age))

def complex_filter_by_city_job(collections):
    for person in (collections.find({'city': "Мадрид", "job": {"$in": ["Повар", "Водитель", "Инженер"]}}, limit=10).sort({"age":1})):
        print(person)

reuslt_complex_filter_by_city_job = complex_filter_by_city_job(connect())
with open("complex_filter_by_city_job.json", "w") as file:
    file.write(json.dumps(reuslt_complex_filter_by_city_job))

def count_obj(collection):
    result = collection.count_documents({
        "age": {"$gt":25, "$lt":35},
        "year":{"$in": [2019, 2020, 2021, 2022]},
        "$or": [
            {"salary": {"gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}]
    })
    print(result)

result_count_obj = count_obj(connect())

with open("count_obj.json", "w") as file:
    file.write(json.dumps(result_count_obj))