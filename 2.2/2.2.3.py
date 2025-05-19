class Numbers:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def show_numbers(self):
        print(f"Числа: {self.num1}, {self.num2}")

    def change_numbers(self, new_num1, new_num2):
        self.num1 = new_num1
        self.num2 = new_num2

    def sum_numbers(self):
        return self.num1 + self.num2

    def max_number(self):
        return max(self.num1, self.num2)

numbers = Numbers(1, 10)
numbers.show_numbers()

numbers.change_numbers(2, 20)
numbers.show_numbers()

sum_result = numbers.sum_numbers()
print(f"Сумма чисел: {sum_result}")

max_result = numbers.max_number()
print(f"Наибольшее число: {max_result}")