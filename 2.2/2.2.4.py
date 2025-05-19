class Counter:
    def __init__(self, initial_value=0):
        self.value = initial_value

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1

    def get_value(self):
        return self.value

counter1 = Counter()
counter2 = Counter(100)

print(f"Значение счетчика 1: {counter1.get_value()}")
counter1.increment()
print(f"Значение счетчика 1 после увеличения: {counter1.get_value()}")
counter1.decrement()
print(f"Значение счетчика 1 после уменьшения: {counter1.get_value()}")

print(f"Значение счетчика 2: {counter2.get_value()}")
counter2.increment()
print(f"Значение счетчика 2 после увеличения: {counter2.get_value()}")
counter2.decrement()
print(f"Значение счетчика 2 после уменьшения: {counter2.get_value()}")