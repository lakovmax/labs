class Worker:
    def __init__(self, name, surname, rate, days):
        self.name = name
        self.surname = surname
        self.rate = rate
        self.days = days

    def GetSalary(self):
        salary = self.rate * self.days
        print(f'Зарплата сотрудника {self.name} {self.surname}: {salary}')

worker1 = Worker("Владимир","Сидоров",1600,30)
worker1.GetSalary()