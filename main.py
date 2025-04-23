import json
import os
from datetime import datetime, timedelta

TASKS_FILE = 'tasks.json'


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)


def add_task(tasks):
    title = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")
    due_date = input("Введите дату выполнения (YYYY-MM-DD): ")

    task = {
        'title': title,
        'description': description,
        'due_date': due_date
    }

    tasks.append(task)
    save_tasks(tasks)
    print("Задача добавлена.")


def delete_task(tasks):
    title = input("Введите название задачи для удаления: ")
    tasks = [task for task in tasks if task['title'] != title]
    save_tasks(tasks)
    print("Задача удалена.")


def edit_task(tasks):
    title = input("Введите название задачи для редактирования: ")
    for task in tasks:
        if task['title'] == title:
            new_title = input("Введите новое название задачи (оставьте пустым, чтобы не менять): ")
            if new_title:
                task['title'] = new_title

            task['description'] = input("Введите новое описание задачи: ")
            task['due_date'] = input("Введите новую дату выполнения (YYYY-MM-DD): ")
            save_tasks(tasks)
            print("Задача отредактирована.")
            return
    print("Задача не найдена.")


def view_tasks(tasks, filter_func=None):
    if filter_func:
        tasks = list(filter(filter_func, tasks))

    if not tasks:
        print("Нет задач для отображения.")
        return

    for task in tasks:
        print(f"Название: {task['title']}, Описание: {task['description']}, Дата выполнения: {task['due_date']}")


def view_today_tasks(tasks):
    today = datetime.now().date()
    view_tasks(tasks, lambda task: datetime.strptime(task['due_date'], '%Y-%m-%d').date() == today)


def view_tomorrow_tasks(tasks):
    tomorrow = datetime.now().date() + timedelta(days=1)
    view_tasks(tasks, lambda task: datetime.strptime(task['due_date'], '%Y-%m-%d').date() == tomorrow)


def view_week_tasks(tasks):
    today = datetime.now().date()
    week_end = today + timedelta(days=7)
    view_tasks(tasks, lambda task: today <= datetime.strptime(task['due_date'], '%Y-%m-%d').date() <= week_end)


def view_all_tasks(tasks):
    view_tasks(tasks)


def view_pending_tasks(tasks):
    today = datetime.now().date()
    view_tasks(tasks, lambda task: datetime.strptime(task['due_date'], '%Y-%m-%d').date() >= today)


def view_passed_tasks(tasks):
    today = datetime.now().date()
    view_tasks(tasks, lambda task: datetime.strptime(task['due_date'], '%Y-%m-%d').date() < today)


def main():
    tasks = load_tasks()

    while True:
        print("\nМеню:")
        print("1. Добавить задачу")
        print("2. Удалить задачу")
        print("3. Редактировать задачу")
        print("4. Просмотреть задачи на сегодня")
        print("5. Просмотреть задачи на завтра")
        print("6. Просмотреть задачи на неделю")
        print("7. Просмотреть все задачи")
        print("8. Просмотреть незавершенные задачи")
        print("9. Просмотреть прошедшие задачи")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            delete_task(tasks)
        elif choice == '3':
            edit_task(tasks)
        elif choice == '4':
            view_today_tasks(tasks)
        elif choice == '5':
            view_tomorrow_tasks(tasks)
        elif choice == '6':
            view_week_tasks(tasks)
        elif choice == '7':
            view_all_tasks(tasks)
        elif choice == '8':
            view_pending_tasks(tasks)
        elif choice == '9':
            view_passed_tasks(tasks)
        elif choice == '0':
            break
        else:
            print("Неверный ввод. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()

