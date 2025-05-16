class Student:
    def __init__(self, lastname, birthdate, group, grade):
        self.lastname = lastname
        self.birthdate = birthdate
        self.group = group
        self.grade = grade

    def changelastname(self, newlastname):
        self.lastname = newlastname
    def changebirthdate(self, newbirthdate):
        self.birthdate = newbirthdate
    def changegroup(self, newgroup):
        self.group = newgroup
    def showinfo(self):
        return f"Фамилия: {self.lastname}, Дата рождения: {self.birthdate}, Группа: {self.group}, Успеваемость: {self.grade}"

def search_student(student):
    search_lastname = input("Введите фамилию студента: ")
    search_birthdate = input("Введите дату рождения студента: ")

    if student.lastname == search_lastname and student.birthdate == search_birthdate:
        print(student.showinfo())
    else:
        print("Студент не найден.")

student1 = Student("Хендогин", "23.12.2006", "634", [4, 5, 3, 5, 5])

student1.changelastname("Агалаков")
student1.changebirthdate("03.07.2007")
student1.changegroup("634")
print(student1.showinfo())

search_student(student1)