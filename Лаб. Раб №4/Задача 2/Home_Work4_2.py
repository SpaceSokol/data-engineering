import pickle
import sqlite3
import sqlite3


def load_data(items):
    with open('task_2_var_21_subitem.pkl', 'rb') as f:
        data = pickle.load(f)
        items = []
        for line in data:
            items.append(line)


def connect_to_bd(file_name):
    connection = sqlite3.connect("1/database.db")
    connection.row_factory = sqlite3.Row
    return connection

def insert_data(db, items):

    cursor = db.cursor()

    # Создание таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_table2 (
            id       INTEGER    PRIMARY KEY AUTOINCREMENT,
            books_id INTEGER    REFERENCES my_table (id),
            title    TEXT (256),
            price    INTEGER,
            place    TEXT (256),
            date     REAL
        )
    ''')

    cursor.executemany("""
            INSERT INTO my_table2 (books_id, title, price, place, date)
            VALUES(
                (SELECT in from my_table WHERE title = title),
                :title, :price, :place, :date
            )
    """, items)
    db.commit()


items = load_data("task_2_var_21_subitem.pkl")
db = connect_to_bd("1/database.db")
insert_data(db, items)













"""import pickle
import sqlite3


connection = sqlite3.connect("database0.db")
cursor = connection.cursor()

result = cursor.execute("SELECT * FROM my_table2")
print(result.fetchall())


"""