class Train:
    def __init__(self, destination, train_number, departure_time):
        self.destination = destination
        self.train_number = train_number
        self.departure_time = departure_time

    def show_info(self):
        return f"Пункт назначения: {self.destination}, Номер поезда: {self.train_number}, Время отправления: {self.departure_time}"

def find(trains):
    search = input("Введите номер поезда: ")
    for train in trains:
        if train.train_number == search:
            print(train.show_info())
            return
    print("Поезд не найден.")

trains = []

train1 = Train("Москва", "123", "10:00")
train2 = Train("Санкт-Петербург", "456", "12:30")
trains.append(train1)
trains.append(train2)

print(train1.show_info())
print(train2.show_info())

find(trains)