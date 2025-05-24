import psutil, sqlite3, time
from datetime import datetime

class SystemMonitor:
    def __init__(self, db_name="system_monitor.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL
            )
        """)
        self.conn.commit()

    def get_cpu_usage(self):
        return psutil.cpu_percent()

    def get_memory_usage(self):
        return psutil.virtual_memory().percent

    def get_disk_usage(self):
        return psutil.disk_usage('/').percent

    def record_data(self):
        timestamp = datetime.now()
        cpu_usage = self.get_cpu_usage()
        memory_usage = self.get_memory_usage()
        disk_usage = self.get_disk_usage()

        self.cursor.execute(
            "INSERT INTO system_data (timestamp, cpu_usage, memory_usage, disk_usage) VALUES (?, ?, ?, ?)",
            (timestamp, cpu_usage, memory_usage, disk_usage)
        )
        self.conn.commit()
        print(f"Данные записаны: {timestamp}")

    def view_data(self):
        self.cursor.execute("SELECT * FROM system_data")
        data = self.cursor.fetchall()
        if data:
            for row in data:
                print(f"ID: {row[0]}")
                print(f"Время: {row[1]}")
                print(f"CPU Usage: {row[2]}%")
                print(f"Memory Usage: {row[3]}%")
                print(f"Disk Usage: {row[4]}%")
                print("-" * 30)
        else:
            print("Нет сохраненных данных.")

    def close_connection(self):
        self.conn.close()

def main():
    monitor = SystemMonitor()
    while True:
        print("\nМеню:")
        print("1. Записать данные")
        print("2. Просмотреть данные")
        print("3. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            monitor.record_data()
        elif choice == "2":
            monitor.view_data()
        elif choice == "3":
            print("До свидания!")
            monitor.close_connection()
            break
        else:
            print("Неверный выбор.")

        time.sleep(5)

main()