import msgpack
import pickle
import sqlite3
import json


# Открываем файл в двоичном режиме
def load_file_1(file_name1):
    with open('task_3_var_21_part_1.msgpack', 'rb') as file:
        # Читаем содержимое файла
        data = file.read()

        # Декодируем данные из формата msgpack
        unpacked_data = msgpack.unpackb(data)
        items = list()

        for line in unpacked_data:
            items.append({"artist":line['artist'],
                          "song": line['song'],
                          "duration_ms": line['duration_ms'],
                          "year": line['year'],
                          "tempo": line['tempo'],
                          "genre": line['genre'],
                          "acousticness": line['acousticness']})
    return items

def load_file_2(file_name2):
    with open('task_3_var_21_part_2.pkl', 'rb') as f:
        data = pickle.load(f)

        for item in data:
            item.pop('energy')
            item.pop('popularity')
    return data


def connect_to_bd(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
            INSERT INTO first (artist, song, duration_ms, year, tempo, genre, acousticness)
            VALUES(
            :artist, :song, :duration_ms, :year, :tempo, :genre, :acousticness
            )
    """, data)
    db.commit()


#ОБЪЕДИНЯЕМ ДАННЫЕ С ОБОИХ ФАЙЛОВ
general_items = load_file_1("task_3_var_21_part_1.msgpack") + load_file_2("task_3_var_21_part_2.pkl")

db = connect_to_bd("db.db")

cursor = db.cursor()
# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS first (
        id           INTEGER    PRIMARY KEY AUTOINCREMENT,
        artist       TEXT (256),
        song         TEXT (256),
        duration_ms  INTEGER,
        year         INTEGER,
        tempo        REAL,
        genre        TEXT (256),
        acousticness REAL
    )
''')

insert_data(db, general_items)

# ЗАПИССЫВАЕМ В JSON ИЗ ТАБЛИЦЫ ПЕРВЫХ 31 СТРОК ОТСОРТИРОВАННЫХ ПО ПОЛЮ 'pages' (ПОДЗАДАЧА 1)
def get_top_year(db, limit):
    cursor = db.cursor()
    res = cursor.execute(f"SELECT artist, song, duration_ms, year FROM first ORDER BY year DESC LIMIT ?", [limit])
    sort_list = []
    for row in res.fetchall():
        sort_list.append(dict(row))

    cursor.close()

    return sort_list

get_top_year(db, 31)

result = get_top_year(db, 31)

# ЗАТЕМ СЧИТЫВАЕМ ЗАПИСАНННЫЙ ФАЙЛ ДЛЯ ПРОВЕРКИ

with open("result_get_sorted_year.json", "w") as r_json:
    r_json.write(json.dumps(result))

with open("result_get_sorted_year.json") as file:
    data = json.load(file)

    #for line in data:
      #  print(line)

# ВЫВОД (СУММУ, МИН., МАКС., СРЕДНЕЕ) ПО ПОЛЮ rating (ПОДЗАДАЧА 2)
def min_max_ave_counts(db):
    cursor = db.cursor()
    min_max_ave_counts_list = []
    result = cursor.execute("""
        SELECT
            SUM(tempo) as sum,
            AVG(tempo) as avg, 
            MIN(tempo) as min,
            MAX(tempo) as max
        FROM first   
    """)
    #print(dict(result.fetchone()))

    min_max_ave_counts_list.append(dict(result.fetchone()))
    return min_max_ave_counts_list

    #return []
    cursor.close()

min_max_ave_counts_result = min_max_ave_counts(db)

with open("min_max_ave_counts_result.json", "w") as r_json:
    r_json.write(json.dumps(min_max_ave_counts_result))

"""with open("min_max_ave_counts_result.json") as file:
    data_res = json.load(file)
    #for line in data_res:
     #   print(line)
"""

# ВЫВОД ЧАСТОТЫВСТРЕЧАЕМОСТИ ДЛЯ КАТЕГОРИАЛЬНОГО ПОЛЯ (ПОДЗАДАЧА 3)
def frequency_of_occurrence_year(db):
    cursor = db.cursor()
    result = cursor.execute("""
                SELECT
                    (FLOOR(year/100) + 1) as century
                FROM first
                GROUP by (FLOOR(year/100) + 1)
    """)

    for line in result.fetchall():
        print(dict(line))

    cursor.close()
    return []


frequency_of_occurrence_year(db)

# ВЫВОД ПЕРВЫХ (VAR+15.....  (ПОДЗАДАЧА 4)
def conclusion_first_counts(db, duration_ms, limit):
    cursor = db.cursor()
    result = cursor.execute("""
                SELECT *
                FROM first
                WHERE duration_ms > ?
                ORDER by duration_ms DESC
                LIMIT ?
                """, [duration_ms, limit])

    for line in result.fetchall():
        print(dict(line))

    cursor.close()
    return []

conclusion_first_counts(db, 200000, 36)