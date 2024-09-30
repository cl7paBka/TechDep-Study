from abc import ABC, abstractmethod
from math import pi


def validate_value(name: str, value: int | float):
    """Функция для проверки валидности вводимых данных, например радиуса круга"""
    if not isinstance(value, (int, float)):
        raise TypeError(f"Тип данных переменной '{name}' должен быть int или float, а не {type(value)}.")
    if value <= 0:
        raise ValueError(f"Значение переменной '{name}' должно быть больше нуля, а не {value}.")


class Shape(ABC):
    def __init__(self, color: str):
        if isinstance(color, str):
            self.color = color
        else:
            raise Exception(f"Тип данных переменной color должен быть str, а не {type(color)}.")

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, color: str, radius: int | float):
        super().__init__(color)
        validate_value("radius", radius)
        self.radius = radius

    def draw(self):
        print(f"Это круг цвета: {self.color}\nЕго радиус равен: {self.radius}")

    def area(self):
        return pi * self.radius ** 2


class Triangle(Shape):
    def __init__(self, color: str, base: int | float, height: int | float):
        super().__init__(color)
        validate_value("base", base)
        validate_value("height", height)
        self.base = base
        self.height = height

    def draw(self):
        print(f"Это треугольник цвета: {self.color}\nЕго основание равно: {self.base}\nЕго высота равна: {self.height}")

    def area(self):
        return self.base * self.height


class Square(Shape):
    def __init__(self, color: str, side: int | float):
        super().__init__(color)
        validate_value("side", side)
        self.side = side

    def draw(self):
        print(f"Это Квадрат цвета: {self.color}\nЕго радиус равен: {self.side}")

    def area(self):
        return self.side ** 2


shapes = [Circle("фиолетовый", 100), Square("белый", 15), Triangle("бежевый", 20, 57)]

for shape in shapes:
    shape.draw()
    print(f"Площадь равна: {shape.area()}\n")

assert shapes[0].area() == 31415.926535897932, f"Проблема в классе Circle"
assert shapes[1].area() == 225, f"Проблема в классе Square"
assert shapes[2].area() == 1140, f"Проблема в классе Triangle"
