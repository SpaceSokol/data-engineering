import sqlite3
import csv
import json

def connect_to_bd(filenmae):
    connection = sqlite3.connect(filenmae)
    connection.row_factory = sqlite3.Row
    return connection

conn = connect_to_bd('database.db')
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT (256),
        author TEXT (256),
        genre TEXT (256),
        pages INTEGER,
        published_year INTEGER,
        isbn TEXT (256),
        rating REAL,
        views INTEGER
    )
''')

def parse_data(filename):            #ПАРСИМ CSV-файл
    items = list()
    with open("task_1_var_21_item.csv", newline='\n', encoding='utf-8') as file:
        filereader = csv.reader(file, delimiter=';')
        filereader.__next__()

        for line in filereader:
            item = {
                'title': line[0],
                'author': line[1],
                'genre': line[2],
                'pages': int(line[3]),
                'published_year': int(line[4]),
                'isbn': line[5],
                'rating': float(line[6]),
                'views': int(line[7])
            }

            items.append(item)

    return items

def insert_data(conn, data):     # ВСТАВЛЯЕМ ДАННЫЕ
    cursor = conn.cursor()

    cursor.executemany("""
                INSERT INTO my_table (title, author, genre, pages, published_year, isbn, rating, views)
                VALUES(
                    :title, :author, :genre, :pages,
                    :published_year, :isbn, :rating, :views
                )
            """, data)

    conn.commit()


items = parse_data("task_1_var_21_item.csv")
insert_data(conn, items)

#res = conn.cursor().execute("SELECT * FROM my_table")

# ЗАПИССЫВАЕМ В JSON ПОСЛЕ ТОГО КАК ПЕРВЫЙ РАЗ ЗАПОЛНИЛИ ТАБЛИЦУ (ПОДЗАДАЧА 1)
def get_top_views(conn, limit):
    cursor = conn.cursor()
    res = cursor.execute(f"SELECT title, author, published_year, views FROM my_table ORDER BY views DESC LIMIT ?", [limit])
    sort_list = []
    for row in res.fetchall():
        sort_list.append(dict(row))

    return sort_list

get_top_views(conn, 31)

result = get_top_views(conn, 31)

# ЗАПИСЫВАЕМ В JSON И ЗАТЕМ СЧИТЫВАЕМ ЗАПИСАНННЫЙ ФАЙЛ ДЛЯ ПРОВЕРКИ

with open("result_get_sorted_lines.json", "w") as r_json:
    r_json.write(json.dumps(result))

"""with open("result_get_sorted_lines.json") as file:
    data = json.load(file)"""


# ВЫВОД (СУММУ, МИН., МАКС., СРЕДНЕЕ) ПО ПОЛЮ rating (ПОДЗАДАЧА 2)
def min_max_ave_counts(conn):
    cursor = conn.cursor()
    min_max_ave_counts_list = []
    result = cursor.execute("""
        SELECT
            SUM(rating) as sum,
            AVG(rating) as avg, 
            MIN(rating) as min,
            MAX(rating) as max
        FROM my_table   
    """)
    #print(dict(result.fetchone()))
    #print(f"\t min_count = {min_count}, \n\t max_count = {max_count})#  #\n\t average_count = {result}")
    min_max_ave_counts_list.append(dict(result.fetchone()))
    return min_max_ave_counts_list

    cursor.close()
    return []

min_max_ave_counts_result = min_max_ave_counts(conn)

with open("min_max_ave_counts_result.json", "w") as r_json:
    r_json.write(json.dumps(min_max_ave_counts_result))

"""with open("min_max_ave_counts_result.json") as file:
    data_res = json.load(file)
    print(data_res)
"""
# ВЫВОД ЧАСТОТЫВСТРЕЧАЕМОСТИ ДЛЯ КАТЕГОРИАЛЬНОГО ПОЛЯ (ПОДЗАДАЧА 3)

def frequency_of_occurrence_published_year(conn):
    cursor = conn.cursor()
    result = cursor.execute("""
                SELECT
                    (FLOOR(published_year/100) + 1) as century
                FROM my_table
                GROUP by (FLOOR(published_year/100) + 1)
    """)

    for line in result.fetchall():
        print(dict(line))

    cursor.close()
    return []


frequency_of_occurrence_published_year(conn)

# ВЫВОД ПЕРВЫХ (VAR+10.....  (ПОДЗАДАЧА 4)
def conclusion_first_counts(conn, min_year, limit):
    cursor = conn.cursor()
    result = cursor.execute("""
                SELECT *
                FROM my_table
                WHERE published_year > ?
                ORDER by views DESC
                LIMIT ?
                """, [min_year, limit])

    for line in result.fetchall():
        print(dict(line))

    cursor.close()
    return []

conclusion_first_counts(conn, 1970, 31)

