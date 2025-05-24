import sqlite3

def add_new_ingredient(name, count):
    cursor.execute("INSERT INTO ingredients (name, count) VALUES (?, ?)", (name, count))
    connection.commit()
    print(f"Ингредиент {name} ({count}) был добавлен в базу данных.")


def add_new_drink(name, abv, cost, ingredients, count):
    cursor.execute("INSERT INTO drinks (name, abv, cost, count) VALUES (?, ?, ?, ?)",
                   (name, abv, cost, count))
    drink_id = cursor.lastrowid

    cursor.executemany("""
    INSERT INTO drinks_ingredients (drink_id, ingredient_id)
    VALUES (?, ?)
    """, ((drink_id, x) for x in ingredients))

    connection.commit()

    print(f"Напиток {name} ({cost} руб., {count}) был добавлен в базу данных.")


def add_new_cocktail(name, cost, composition):
    cursor.execute("INSERT INTO cocktails (name, cost) VALUES (?, ?)", (name, cost))
    cocktail_id = cursor.lastrowid

    cursor.executemany("""
    INSERT INTO cocktails_composition (cocktail_id, drink_id)
    VALUES (?, ?)
    """, ((cocktail_id, x) for x in composition))

    connection.commit()

    print(f"Коктейль {name} ({cost} руб., {count}) был добавлен в базу данных.")


def print_all_ingredients():
    cursor.execute("SELECT * FROM ingredients")
    for values in cursor.fetchall():
        print(f"{values[0]}. {values[1]} (осталось {values[2]})")

def print_all_drinks():
    cursor.execute("SELECT * FROM drinks")
    for values in cursor.fetchall():
        print(f"""{values[0]}. {values[1]} (осталось {values[4]}):
  Крепость: {values[2]}%
  Цена: {values[3]}""")

def print_all_cocktails():
    cursor.execute("""
    SELECT c.id, c.name, c.cost, AVG(d.abv) 
    FROM cocktails c
    LEFT JOIN cocktails_composition composition ON c.id = composition.cocktail_id
    LEFT JOIN drinks d ON d.id = composition.drink_id
    GROUP BY c.id
    """)
    for values in cursor.fetchall():
        print(f"""{values[0]}. {values[1]}:
  Крепость: {values[3]}%
  Цена: {values[2]}""")

def restock_ingredient(id, count):
    cursor.execute("UPDATE ingredient SET count = count + ? WHERE id = ?", (count, id))
    connection.commit()
    print(f"Запасы ингредиента под ID {id} были пополнены на {count}ед.")

def make_drink(id, count):
    cursor.execute("BEGIN")
    try:
        cursor.execute("""
        UPDATE ingredients
        SET count = count - ?
        WHERE id IN (SELECT ingredient_id
                     FROM drinks_ingredients
                     WHERE drink_id = ?)
        """, (count, id))

        cursor.execute("UPDATE drinks SET count = count + ? WHERE id = ?", (count, id))

        cursor.execute("COMMIT")
    except connection.Error:
        print("Не хватает ингредиентов!")
        cursor.execute("ROLLBACK")

    connection.commit()

    print(f"Запасы напитка под ID {id} были пополнены на {count}ед.")

def sell_drink(id, count, money):
    change = money
    cursor.execute("SELECT cost * ? FROM drinks WHERE id = ?", (count, id))
    cost = cursor.fetchone()[0]
    change -= cost
    if change < 0:
        print(f"Для покупки нехватает {-change} руб.!")
        return money
    else:
        cursor.execute("BEGIN")
        try:
            cursor.execute("UPDATE drinks SET count = count - ? WHERE id = ?", (count, id))
            cursor.execute("COMMIT")
            print(f"Напиток под ID {id} ({count}) был продан за {cost} руб.")
        except connection.Error:
            print("Не хватает напитков!")
            cursor.execute("ROLLBACK")
            change = money

        connection.commit()
        return change

def sell_cocktail(id, count, money):
    change = money
    cursor.execute("SELECT cost * ? FROM cocktails WHERE id = ?", (count, id))
    cost = cursor.fetchone()[0]
    change -= cost
    if change < 0:
        print(f"Для покупки нехватает {-change} руб.!")
        return money
    else:
        cursor.execute("BEGIN")
        try:
            cursor.execute("""
            UPDATE drinks
            SET count = count - ?
            WHERE id IN (SELECT drink_id
                         FROM cocktails_composition
                         WHERE cocktail_id = ?)
            """, (count, id))

            cursor.execute("COMMIT")
            print(f"Коктейль под ID {id} ({count}) был продан за {cost}руб.")
        except connection.Error:
            print("Не хватает напитков!")
            cursor.execute("ROLLBACK")
            change = money

        connection.commit()
        return change

connection = sqlite3.connect("i_love_drink.db")
connection.isolation_level = None
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredients (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	count INTEGER CHECK (count >= 0)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS drinks (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	abv REAL,
	cost REAL,
	count INTEGER CHECK (count >= 0)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS drinks_ingredients (
	drink_id INTEGER,
	ingredient_id INTEGER,

	PRIMARY KEY (drink_id, ingredient_id),
	FOREIGN KEY (drink_id) REFERENCES drinks(id) ON DELETE CASCADE,
	FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS cocktails (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	cost REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS cocktails_composition (
	cocktail_id INTEGER,
	drink_id INTEGER,

	PRIMARY KEY (cocktail_id, drink_id),
	FOREIGN KEY (cocktail_id) REFERENCES cocktails(id) ON DELETE CASCADE,
	FOREIGN KEY (drink_id) REFERENCES drinks(id) ON DELETE CASCADE
)
""")

print("I love drink")
while True:
    print()
    print("Введите номер действия, которое хотите сделать:")
    print("1. Добавить новый предмет в базу данных")
    print("2. Посмотреть все предметы в базе данных")
    print("3. Пополнить запасы")
    print("4. Продать")
    print("5. Закрыть приложение")
    action = int(input(": "))
    match action:
        case 1:
            print("Выберите что именно хотите добавить:")
            print("1. Ингредиент")
            print("2. Алкогольный напиток")
            print("3. Коктейль")
            type = int(input(": "))
            match type:
                case 1:
                    name = input("Введите название ингредиента: ")
                    count = int(input("Введите текущее количество ингредиента: "))
                    add_new_ingredient(name, count)
                case 2:
                    name = input("Введите название напитка: ")
                    abv = float(input("Введите крепость напитка: "))
                    cost = float(input("Введите цену напитка: "))
                    ingredients = input("Введите ID ингредиентов (через пробел): ").split()
                    ingredients = (int(x) for x in ingredients)
                    count = int(input("Введите текущее количество напитка: "))
                    add_new_drink(name, abv, cost, ingredients, count)
                case 3:
                    name = input("Введите название коктейля: ")
                    cost = float(input("Введите цену коктейля: "))
                    composition = input("Введите ID напитков в составе (через пробел): ").split()
                    composition = (int(x) for x in composition)
                    add_new_cocktail(name, cost, composition)
                case _:
                    print("Неверная команда")
        case 2:
            print("Выберите что именно хотите просмотреть:")
            print("1. Ингредиенты")
            print("2. Алкогольные напитки")
            print("3. Коктейли")
            type = int(input(": "))
            match type:
                case 1:
                    print_all_ingredients()
                case 2:
                    print_all_drinks()
                case 3:
                    print_all_cocktails()
                case _:
                    print("Неверная команда")
        case 3:
            print("Выберите запасы чего хотите пополнить:")
            print("1. Ингредиентов")
            print("2. Алкогольных напитков")
            type = int(input(": "))
            id = int(input("Введите ID: "))
            count = int(input("Введите сколько нужно пополнить: "))
            match type:
                case 1:
                    restock_ingredient(id, count)
                case 2:
                    make_drink(id, count)
                case _:
                    print("Неверная команда!")
        case 4:
            print("Выберите что именно хотите продать:")
            print("1. Алкогольный напиток")
            print("2. Коктейль")
            type = int(input(": "))
            id = int(input("Введите ID: "))
            count = int(input("Введите сколько нужно продать: "))
            money = float(input("Введите сумму денег, данную покупателем: "))
            match type:
                case 1:
                    change = sell_drink(id, count, money)
                case 2:
                    change = sell_cocktail(id, count, money)
                case _:
                    change = money
                    print("Неверная команда!")
                    continue
            print(f"Сдача: {change} руб.")
        case 5:
            break
        case _:
            print("Неверная команда!")