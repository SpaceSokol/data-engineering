import msgpack
import pickle
import sqlite3
import json
import csv


# Открываем файл в двоичном режиме
def load_file(file_name):
    key = ['category', 'fromCity', 'isAvailable', 'name', 'price', 'quantity', 'views']
    with open(file_name, 'rb') as f:
        data = f.read()
        unpacked_data = msgpack.unpackb(data)
        for line in range(len(unpacked_data)):
            #print(unpacked_data[line])
            if key[0] not in unpacked_data[line]:
                #print(unpacked_data[line])
                unpacked_data[line]['category'] = 'no'

        return unpacked_data


result = load_file('task_4_var_21_product_data.msgpack')


# ОТКОРРЕКТИРОВАЛИ ДАННЫЕ МСГПАК
def connect_to_bd(filenmae):
    connection = sqlite3.connect(filenmae)
    connection.row_factory = sqlite3.Row
    return connection


db = connect_to_bd('fourth.db')
cursor = db.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        id          INTEGER    PRIMARY KEY AUTOINCREMENT,
        name        TEXT (256),
        price       REAL,
        quantity    INTEGER,
        category    TEXT (256),
        fromCity    TEXT (256),
        isAvailable TEXT (256),
        views       INTEGER
        version     INTEGER    DEFAULT (0) 
    )
''')


#with open("task_4_var_21_update_data.csv", newline='\n', encoding='utf-8') as file:
  #  reader = csv.reader(file, delimiter=';')
    # for stroka in reader:
    # print(stroka)

def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
            INSERT INTO product (name, price, quantity, category, fromCity, isAvailable, views)
            VALUES(
                :name, :price, :quantity, :category, :fromCity, :isAvailable, :views)
            """, data)
    db.commit()

#db = connect_to_bd('fourth.db')

insert_data(db, result)

def parse_data(filename):            #ПАРСИМ CSV-файл
    items = list()
    with open("task_4_var_21_update_data.csv", newline='\n', encoding='utf-8') as file:
        filereader = csv.reader(file, delimiter=';')
        filereader.__next__()

        for line in filereader:
            item = {
                'name': line[0],
                'method': line[1],
                'param': line[2],
            }

            items.append(item)

    return items


#parse_data("task_4_var_21_update_data.csv")

def delete_by_name(bd, name):
    cursor = db.cursor()
    cursor.executemany("DELETE FROM product WHERE name = ?", [name])
    db.commit()

def update_price_by_percent(db, name, percent):
    cursor = db.cursor()
    cursor.execute("UPDATE product SET price = ROUND((price * (1 + ?)), 2) WHERE name =?", [percent, name])
    cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
    db.commit()

def update_price(db, name, value):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0)", [value, name, value])
    if res.rowcount > 0:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def update_available(db, name, param):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET isAvailable = ? WHERE (name = ?)", [param, name])
    cursor.execute("UPDATE product SET version + 1 WHERE name = ?", [name])
    db.commit()

def update_quantity(db, name, value):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)", [value, name, value])
    if res.rowcount > 1:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()

def handle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case "remove":
                print(f"deleting {item['name']}")
                delete_by_name(db, [item['name']])
            case "price_percent":
                print(f"update price {item['name']} {item['param']}%")
                update_price_by_percent(db, item['name'], item['param'])
            case "price_abs":
                print(f"update price {item['name']} {item['param']}")
                update_price(db, item['name'], item['param'])
            case "available":
                print(f"update available {item['name']} {item['param']}")
                update_available(db, item['nmae'], item['param'])
            case "quantity_add":
                print(f"update quantity {item['name']} {item['param']}")
                update_quantity(db, item['name'], item['param'])
            case "quantity_sub":
                print(f"update quantity {item['name']} {item['param']}")
                update_quantity(db, item['name'], item['param'])
            case _:
                print(f"unknown method {item['method']}")

update_items = parse_data("task_4_var_21_update_data.csv")
handle_update(db, update_items)