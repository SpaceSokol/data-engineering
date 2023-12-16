import csv
from pymongo import MongoClient
import json

def connect():
    client = MongoClient()
    db = client["database2"]
    return db.person


def file_reader(filename):
    with open('task_2_item.csv', newline='\n', encoding="UTF-8") as file:
        items = list()
        # item = {'job', 'salary', 'id', 'city', 'year', 'age'}
        item = dict()

        lines = csv.reader(file, delimiter=';')
        lines.__next__()

        for line in lines:
            item = {
                'job': line[0],
                'salary': int(line[1]),
                'id': int(line[2]),
                'city': line[3],
                'year': int(line[4]),
                'age': int(line[5])
            }
            items.append(item)

    return items


def insert_many(collection, data):
    result = collection.insert_many(data) # many or one - если один объект
    print(result)



data = file_reader("task_2_item.csv")
result_insert_many = insert_many(connect(), data)

with open("result_insert_many.json", "w") as file:  #1
    file.write(json.dumps(result_insert_many))

def filter_by_age(collection):  # ЭТОТ КУСОК КОДА ПЕРВОЙ ЗАДАЧИ
    for person in (collection
            .find({"age": {"$lt": 30}}, {"_id": -1, "age": 1}, limit=15)
            .sort({'salary': -1})):
        print(person)

result_filter_by_age = filter_by_age (connect())

with open("result_filter_by_age.json", "w") as file:  #2
    file.write(json.dumps(result_filter_by_age))

def complex_filter_by_city_and_job(collection):
    for person in (collection
            .find({"city": "Москва",
                  "job": {"$in": ["Продавец","IT-специалист","Инженер"]}
                   }, limit=10)
            .sort({'age':1})):
        print(person)

result_complex_filter_by_city_and_job = complex_filter_by_city_and_job(connect())

with open("complex_filter_by_city_and_job.json", "w") as file:  #3
    file.write(json.dumps(result_complex_filter_by_city_and_job))

def get_stat_by_salary(collection):
    q = [
        {
            "$group": {
                "_id":  "result",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"},
            }
        }
    ]
    for stat in collection.aggregate(q):
        print(stat)

result_get_stat_by_salary = get_stat_by_salary(connect())

with open("result_get_stat_by_salary.json", "w") as file:  #4
    file.write(json.dumps(result_get_stat_by_salary))

def get_freq_by_job(collection):
    q = [
        {
            "$group": {
                "_id":  "$job",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]
    for stat in collection.aggregate(q):
        print(stat)

result_get_freq_by_job = get_freq_by_job(connect())

with open("result_get_freq_by_job.json", "w") as file:  #5
    file.write(json.dumps(result_get_freq_by_job))

def get_salary_stat_by_columm(collection, column_name):
    q = [
        {
            "$group": {
                "_id":  f"${column_name}",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"},
            }
        }
    ]
    for stat in collection.aggregate(q):
        print(stat)

result_get_salary_stat_by_columm =  get_salary_stat_by_columm(connect(), 'city')
# print("=========================================")
result_get_salary_stat_by_columm = get_salary_stat_by_columm(connect(), 'job')


with open("result_get_salary_stat_by_columm.json", "w") as file:  #6
    file.write(json.dumps(result_get_salary_stat_by_columm))

with open("result_get_salary_stat_by_columm.json", "w") as file:  #7
    file.write(json.dumps(result_get_salary_stat_by_columm))


def get_age_stat_by_columm(collection, column_name):
    q = [
        {
            "$group": {
                "_id":  f"${column_name}",
                "max": {"$max": "$age"},
                "min": {"$min": "$age"},
                "avg": {"$avg": "$age"},
            }
        }
    ]
    for stat in collection.aggregate(q):
        print(stat)

result_get_age_stat_by_columm = get_age_stat_by_columm(connect(), 'city')
result_get_age_stat_by_columm = get_age_stat_by_columm(connect(), 'job')

with open("result_get_age_stat_by_columm.json", "w") as file:  #9
    file.write(json.dumps(result_get_age_stat_by_columm))

with open("result_get_age_stat_by_columm.json", "w") as file:  #10
    file.write(json.dumps(result_get_age_stat_by_columm))

def max_salary_by_min_age(collection):
    q = [
        {
            "$group": {
                "_id": "$age",
                "max_salary": {"$max": "$salary"}
            }
        },
        {
            "$group": {
                "_id": "result",
                "min_age": {"$min": "$_id"},
                "max_salary": {"$max": "$max_salary"}
            }
        }
    ]
    for stat in collection.aggregate(q):
        print(stat)

result_max_salary_by_min_age = max_salary_by_min_age(connect())

with open("result_max_salary_by_min_age.json", "w") as file:  #11
    file.write(json.dumps(result_max_salary_by_min_age))

def min_salary_by_max_age(collection):
    q = [
        {
            "$group": {
                "_id": "$age",
                "min_salary": {"$min": "$salary"}
            }
        },
        {
            "$group": {
                "_id": "result",
                "max_age": {"$max": "$_id"},
                "min_salary": {"$min": "$min_salary"}
            }
        }
    ]
    for stat in collection.aggregate(q):
        print(stat)

result_min_salary_by_max_age = min_salary_by_max_age(connect())

with open("result_min_salary_by_max_age.json", "w") as file:  #12
    file.write(json.dumps(result_min_salary_by_max_age))

def big_query(collection):
    q = [
        {
            "$match": {
                "salary": {"$gt": 50_000}
            },
        },
        {
            "$group": {
                "_id": "$city",
                "min": {"$min": "$age"},
                "max": {"$max": "$age"},
                "avg": {"$avg": "$age"}
            }
        },
        {
            "$sort":{
                "avg":-1
            }
        }
    ]

    for stat in collection.aggregate(q):
        print(stat)

result_big_query = big_query(connect())

with open("result_big_query.json", "w") as file:  #13
    file.write(json.dumps(result_big_query))


def big_query_2(collection):
    q = [
        {
            "$match": {
                "city": {"$in": ["Москва","Ташкент","Афины","Мадрид"]},
                "job": {"$in": ["Программист","Учитель","Продавец"]},
                "$or": [
                    {"age": {"$gt": 18, "$lt": 25}},
                    {"age": {"$gt": 50, "$lt": 65}}
                ]
            },
        },
        {
            "$group": {
                "_id": "$city",
                "min": {"$min": "$salary"},
                "max": {"$max": "$salary"},
                "avg": {"$avg": "$salary"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        print(stat)

result_big_query_2 = big_query_2(connect())

with open("result_big_query_2.json", "w") as file:  #13
    file.write(json.dumps(result_big_query_2))


