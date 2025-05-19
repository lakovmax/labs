class Class1:
    def __init__(self, a=0, b=1):
        self.a = a
        self.b = b
        print(f"Создан объект Class1 с a={self.a} и b={self.b}")

    def __del__(self):
        print(f"Объект Class1 с a={self.a} и b={self.b} удален.")

obj1 = Class1(10, 20)
obj2 = Class1()
del obj1
del obj2