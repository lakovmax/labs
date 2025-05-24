import sqlite3
from enum import Enum

class EditFields(Enum):
    first_name = 1
    last_name = 2
    middle_name = 3
    group_number = 4
    grades = 5

def add_student(first_name, last_name, middle_name, group_number, grades):
    if len(grades) != 4:
        print("Ошибка: нужно ввести ровно 4 оценки!")
        return
    cursor.execute("""
    INSERT INTO students (first_name, last_name, middle_name, group_number)
    VALUES (?, ?, ?, ?)
    """, (first_name, last_name, middle_name, group_number))
    student_id = cursor.lastrowid
    cursor.executemany("""
    INSERT INTO grades (grade, student_id)
    VALUES (?, ?)
    """, [(x, student_id) for x in grades])
    connection.commit()
    print(f"Студент {last_name} {first_name} {middle_name} с номером ID {student_id} был добавлен в группу {group_number}.")

def print_all_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    if not students:
        print("Нет студентов в базе.")
        return
    for values in students:
        print(f"{values[0]}. {values[2]} {values[1]} {values[3]} - гр. {values[4]}")

def print_student(id):
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()
    if not student:
        print("Студент не найден.")
        return
    cursor.execute("SELECT AVG(grade) FROM grades WHERE student_id = ?", (id,))
    avg_grade = cursor.fetchone()
    avg = avg_grade[0] if avg_grade and avg_grade[0] is not None else "нет оценок"
    print(f"""{student[2]} {student[1]} {student[3]}:
  ID: {student[0]}
  Группа: {student[4]}
  Средний балл: {avg}""")

def edit_student(id, field: EditFields, value):
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    if not cursor.fetchone():
        print("Студент не найден.")
        return
    if field != EditFields.grades:
        cursor.execute(f"UPDATE students SET {field.name} = ? WHERE id = ?", (value, id))
        print(f"Данные студента с номером ID {id} были изменены.")
    else:
        if len(value) != 4:
            print("Ошибка: нужно ввести ровно 4 оценки!")
            return
        cursor.execute("DELETE FROM grades WHERE student_id = ?", (id,))
        cursor.executemany("""
        INSERT INTO grades (grade, student_id)
        VALUES (?, ?)
        """, [(x, id) for x in value])
        print(f"Оценки студента с номером ID {id} были изменены.")
    connection.commit()

def delete_student(id):
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    if not cursor.fetchone():
        print("Студент не найден.")
        return
    cursor.execute("DELETE FROM students WHERE id = ?", (id,))
    connection.commit()
    print(f"Студент с ID {id} был удалён.")

def print_group_avg_grade(group_number):
    cursor.execute("""
    SELECT AVG(grade)
    FROM grades
    WHERE student_id IN (SELECT id
                        FROM students
                        WHERE group_number = ?)
    """, (group_number,))
    avg_grade = cursor.fetchone()
    avg = avg_grade[0] if avg_grade and avg_grade[0] is not None else "нет оценок"
    print(f"Средний балл группы {group_number}: {avg}")

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT,
  last_name TEXT,
  middle_name TEXT,
  group_number INTEGER
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  grade INTEGER CHECK (grade >= 1 AND grade <= 5),
  student_id INTEGER,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
)
""")

while True:
    print()
    print("Введите номер действия, которое хотите сделать:")
    print("1. Добавить нового студента")
    print("2. Просмотреть всех студентов")
    print("3. Просмотреть одного студента")
    print("4. Отредактировать студента")
    print("5. Удалить студента")
    print("6. Просмотреть средний балл студентов определённой группы")
    print("7. Закрыть приложение")
    try:
        action = int(input(": "))
    except ValueError:
        print("Ошибка: введите число!")
        continue
    match action:
        case 1:
            first_name = input("Введите имя студента: ")
            last_name = input("Введите фамилию студента: ")
            middle_name = input("Введите отчество студента: ")
            try:
                group_number = int(input("Введите номер группы студента: "))
            except ValueError:
                print("Ошибка: номер группы должен быть числом!")
                continue
            grades = input("Введите оценки студента (через пробел): ").split()
            try:
                grades = [int(x) for x in grades]
            except ValueError:
                print("Ошибка: оценки должны быть числами!")
                continue
            add_student(first_name, last_name, middle_name, group_number, grades)
        case 2:
            print_all_students()
        case 3:
            try:
                student_id = int(input("Введите ID студента: "))
            except ValueError:
                print("Ошибка: ID должен быть числом!")
                continue
            print_student(student_id)
        case 4:
            try:
                id = int(input("Введите ID студента: "))
            except ValueError:
                print("Ошибка: ID должен быть числом!")
                continue
            print("Введите номер поля, которое хотите отредактировать:")
            print("1. Имя")
            print("2. Фамилия")
            print("3. Отчество")
            print("4. Номер группы")
            print("5. Оценки")
            try:
                edit_field = EditFields(int(input("> ")))
            except (ValueError, KeyError):
                print("Ошибка: введите число от 1 до 5.")
                continue
            if edit_field in [EditFields.first_name, EditFields.last_name, EditFields.middle_name]:
                new_value = input("Введите новое значение: ")
                edit_student(id, edit_field, new_value)
            elif edit_field == EditFields.group_number:
                try:
                    new_value = int(input("Введите номер группы: "))
                except ValueError:
                    print("Ошибка: номер группы должен быть числом!")
                    continue
                edit_student(id, edit_field, new_value)
            elif edit_field == EditFields.grades:
                grades = input("Введите новые оценки (через пробел): ").split()
                try:
                    grades = [int(x) for x in grades]
                except ValueError:
                    print("Ошибка: оценки должны быть числами!")
                    continue
                edit_student(id, edit_field, grades)
        case 5:
            try:
                student_id = int(input("Введите ID студента: "))
            except ValueError:
                print("Ошибка: ID должен быть числом!")
                continue
            delete_student(student_id)
        case 6:
            try:
                group_number = int(input("Введите номер группы: "))
            except ValueError:
                print("Ошибка: номер группы должен быть числом!")
                continue
            print_group_avg_grade(group_number)
        case 7:
            print("Выход из программы.")
            connection.close()
            break
        case _:
            print("Нет такого действия!")