from pymongo import MongoClient
import json

def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.person


def file_reader(filename):
    with open('task_3_item.json', encoding="UTF-8") as file:
        lines = json.load(file)
    return lines


def insert_many(collection, data):
    result = collection.insert_many(data) # many or one - если один объект
    print(result)


def delete_by_salary(collection):
    result = collection.delete_many({
        "$or": [
            {"salary": {"$lt": 25_000}},
            {"salary": {"$gt": 175_000}},
            {"city": {"$lt": "Ташкент"}}
        ]
    })
    print(result)

def update_age(collection):
    result = collection.update_many({}, {
        "$inc": {
            "age" : 1
        }
    })
    print(result)

def increase_salary_by_job(collection):
    filter = {
        "job": {"$in": ["Повар", "IT-специалист", "Инженер", "Врач"]}
    }
    update = {
            "$mul": {
                "salary": 1.05
            }
    }
    result = collection.update_many(filter, update)
    print(result)

def increase_salary_by_city(collection):
    filter = {
        "city": {"$nin": ["Алма-Ата", "Афины", "Москва", "Ташкент"]}
    }
    update = {
            "$mul": {
                "salary": 1.07
            }
    }
    result = collection.update_many(filter, update)
    print(result)

def increase_salary_by_city_job_age(collection):
    filter = {
        "city": {"$in": ["Москва"]},
        "job": {"$in": ["Инженер"]},
        "age": {"$lt": 44}
    }
    update = {
            "$mul": {
                "salary": 1.1
            }
    }
    result = collection.update_many(filter, update)
    print(result)




data = file_reader("task_3_item.json")
insert_many(connect(), data)

result_delete_by_salary = delete_by_salary(connect())  # к последней подзадаче добавлено поле city
with open("result_delete_by_salary.json", "w") as file:
    file.write(json.dumps(result_delete_by_salary))

result_update_age = update_age(connect())
with open("result_update_age.json", "w") as file:
    file.write(json.dumps(result_update_age))

result_increase_salary_by_job = increase_salary_by_job(connect())
with open("result_increase_salary_by_job.json", "w") as file:
    file.write(json.dumps(result_increase_salary_by_job))

result_increase_salary_by_city = increase_salary_by_city(connect())
with open("result_increase_salary_by_city.json", "w") as file:
    file.write(json.dumps(result_increase_salary_by_city))

result_increase_salary_by_city_job_age = increase_salary_by_city_job_age(connect())
with open("result_increase_salary_by_city_job_age.json", "w") as file:
    file.write(json.dumps(result_increase_salary_by_city_job_age))