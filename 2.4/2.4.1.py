import sqlite3
from enum import Enum

class EditFields(Enum):
    first_name = 1
    last_name = 2
    middle_name = 3
    group_number = 4
    grades = 5

def add_student(first_name, last_name, middle_name, group_number, grades):
    cursor.execute("""
    INSERT INTO students (first_name, last_name, middle_name, group_number)
    VALUES (?, ?, ?, ?)
    """, (first_name, last_name, middle_name, group_number))
    student_id = cursor.lastrowid
    cursor.executemany("""
    INSERT INTO grades (grade, student_id)
    VALUES (?, ?)
    """, ((x, student_id) for x in grades))
    connection.commit()

    print(f"Студент {last_name} {first_name} {middle_name} с номером ID {student_id} был добавлен в группу {group_number}.")

def print_all_students():
    cursor.execute("SELECT * FROM students")
    for values in cursor.fetchall():
        print(f"{values[0]}. {values[2]} {values[1]} {values[3]} - гр. {values[4]}")

def print_student(id):
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()

    cursor.execute("SELECT AVG(grade) FROM grades WHERE student_id = ?", (id,))
    avg_grade = cursor.fetchone()

    print(f"""{student[2]} {student[1]} {student[3]}:
  ID: {student[0]}
  Группа: {student[4]}
  Средний балл: {avg_grade[0]}""")

def edit_student(id, field: EditFields, value):
    if field != EditFields.grades:
        cursor.execute(f"UPDATE students SET {field.name} = ? WHERE id = ?", (value, id))
        print(f"Данные студента с номером ID {id} были изменены.")
    else:
        cursor.execute("DELETE FROM grades WHERE student_id = ?", (id,))
        cursor.executemany("""
        INSERT INTO grades (grade, student_id)
        VALUES (?, ?)
        """, ((x, id) for x in value))
        print(f"Оценки студента с номером ID {id} были изменены.")

    connection.commit()

def delete_student(id):
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
    print(f"Средний балл группы {group_number}: {avg_grade[0]}")

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
    print("6. Просмотреть средний балл студентов конкретной группы")
    print("7. Закрыть приложение")
    action = int(input(": "))
    match action:
        case 1:
            first_name = input("Введите имя студента: ")
            last_name = input("Введите фамилию студента: ")
            middle_name = input("Введите отчество студента: ")
            group_number = int(input("Введите номер группы студента: "))
            grades = input("Введите оценки студента (через пробел): ").split()
            grades = (int(x) for x in grades)
            add_student(first_name, last_name, middle_name, group_number, grades)
        case 2:
            print_all_students()
        case 3:
            print_student(int(input("Введите ID студента: ")))
        case 4:
            id = int(input("Введите ID студента: "))

            print("Введите номер поля, которое хотите отредактировать:")
            print("1. Имя")
            print("2. Фамилия")
            print("3. Отчество")
            print("4. Номер группы")
            print("5. Оценки")
            edit_field = EditFields(int(input(": ")))

            if edit_field < EditFields.group_number:
                edit_student(id, edit_field, input("Введите новое значение: "))
            elif edit_field == EditFields.group_number:
                edit_student(id, edit_field, int(input("Введите номер группы: ")))
            else:
                grades = input("Введите новые оценки (через пробел(например 5 4 3 2)): ").split()
                grades = (int(x) for x in grades)
                edit_student(id, edit_field, grades)
        case 5:
            delete_student(int(input("Введите ID студента: ")))
        case 6:
            print_group_avg_grade(int(input("Введите номер группы: ")))
        case 7:
            break
        case _:
            print("Неверная команда")