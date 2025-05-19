class Worker:
    def __init__(self, name, surname, rate, days):
        self.__name = name
        self.__surname = surname
        self.__rate = rate
        self.__days = days

    def GetSalary(self):
        salary = self.__rate * self.__days
        print(f"Зарплата сотрудника {self.get_name()} {self.get_surname()}: {salary}")

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_rate(self):
        return self.__rate

    def get_days(self):
        return self.__days

worker1 = Worker("Владимир","Сидоров",1600,30)
worker1.GetSalary()
print(f"Имя: {worker1.get_name()}")
print(f"Фамилия: {worker1.get_surname()}")
print(f"Ставка за день работы: {worker1.get_rate()}")
print(f"Кол-во отработанных дней: {worker1.get_days()}")