"""Algorithm."""

import math
from typing import NamedTuple

from exception import LackSpace, IncorrectFigure


class Figure(NamedTuple):
    """Figure module."""
    side_a: float
    side_b: float
    side_c: float
    side_d: float


class FurnitureArrangement():

    coordinates = {}  # хранение координат по схеме "ключ объекта: (координаты, маркеры углов, маркеры точек)
    free_space = [] # хранение расстояний между мебелью через запятую (в виде координат)

    def placing_in_coordinates(self):
        return None

    def corner_markings(self, length_and_width: dict, center: dict, wall_number: int) -> dict:
        corners_coordinates = {"north_west": {"x": 0, "y": 0}, "north_east": {"x": 0, "y": 0},
                               "south_west": {"x": 0, "y": 0}, "south_east": {"x": 0, "y": 0}}

        if wall_number == 1:
            corners_coordinates["north_east"]["x"] = center["x"]
            corners_coordinates["north_east"]["y"] = center["y"] + (length_and_width["width"] // 2)
            corners_coordinates["north_west"]["x"] = center["x"]
            corners_coordinates["north_west"]["y"] = center["y"] - (length_and_width["width"] // 2)
            corners_coordinates["south_east"]["x"] = center["x"] + length_and_width["length"]
            corners_coordinates["south_east"]["y"] = center["y"] + (length_and_width["width"] // 2)
            corners_coordinates["south_west"]["x"] = center["x"] + length_and_width["length"]
            corners_coordinates["south_west"]["y"] = center["y"] - (length_and_width["width"] // 2)

        elif wall_number == 2:
            corners_coordinates["north_east"]["x"] = center["x"] + (length_and_width["width"] // 2)
            corners_coordinates["north_east"]["y"] = center["y"]
            corners_coordinates["north_west"]["x"] = center["x"] - (length_and_width["width"] // 2)
            corners_coordinates["north_west"]["y"] = center["y"]
            corners_coordinates["south_east"]["x"] = center["x"] + (length_and_width["width"] // 2)
            corners_coordinates["south_east"]["y"] = center["y"] - length_and_width["length"]
            corners_coordinates["south_west"]["x"] = center["x"] - (length_and_width["width"] // 2)
            corners_coordinates["south_west"]["y"] = center["y"] - length_and_width["length"]

        elif wall_number == 3:
            corners_coordinates["north_east"]["x"] = center["x"]
            corners_coordinates["north_east"]["y"] = center["y"] - (length_and_width["width"] // 2)
            corners_coordinates["north_west"]["x"] = center["x"]
            corners_coordinates["north_west"]["y"] = center["y"] + (length_and_width["width"] // 2)
            corners_coordinates["south_east"]["x"] = center["x"] - length_and_width["length"]
            corners_coordinates["south_east"]["y"] = center["y"] - (length_and_width["width"] // 2)
            corners_coordinates["south_west"]["x"] = center["x"] - length_and_width["length"]
            corners_coordinates["south_west"]["y"] = center["y"] + (length_and_width["width"] // 2)

        elif wall_number == 4:
            corners_coordinates["north_east"]["x"] = center["x"] - (length_and_width["width"] // 2)
            corners_coordinates["north_east"]["y"] = center["y"]
            corners_coordinates["north_west"]["x"] = center["x"] + (length_and_width["width"] // 2)
            corners_coordinates["north_west"]["y"] = center["y"]
            corners_coordinates["south_east"]["x"] = center["x"] - (length_and_width["width"] // 2)
            corners_coordinates["south_east"]["y"] = center["y"] + length_and_width["length"]
            corners_coordinates["south_west"]["x"] = center["x"] + (length_and_width["width"] // 2)
            corners_coordinates["south_west"]["y"] = center["y"] + length_and_width["length"]

        return corners_coordinates

    def room_coordinates(self):
        return None

    def middle_of_the_distance_on_the_wall(self):
        return None

    def free_space_algorithm(self, objects: list) -> tuple:
        # На вход подается список с координатами углов объектов. Координаты между друг другом минусим, находим
        # по ближайшим неприлегающим углам расстояние по модулю в виде гипотенузы (вычитание по иксу -- это
        # один катет, вычитание по игрику -- другой). И записыванием самое большое расстояние в переменную. Углы
        # разбиты по сторонам света: north_west, north-east, south-west, south-east. В каждом объекте так же находится
        # значение и длина стены "wall_info": {"wall_number": 1, "wall_length": 4}
        length = {}
        counter = 1

        def longest_distance_corner(first_left, first_right, second_left, second_right):
            first_distance = abs(first_left - second_left)
            second_distance = abs(first_left - second_right)
            third_distance = abs(first_right - second_left)
            fourth_distance = abs(first_right - second_right)

            minimal_distance = min([first_distance, second_distance, third_distance, fourth_distance])
            return minimal_distance

        def x_or_y_distance(first_object, second_object, x_or_y):
            result = longest_distance_corner(
                first_object["south_west"][f"{x_or_y}"],
                first_object["south_east"][f"{x_or_y}"],
                second_object[counter]["south_west"][f"{x_or_y}"],
                second_object[counter]["south_east"][f"{x_or_y}"])
            return result

        def core_and_output(first_object, second_object):
            x_distance = x_or_y_distance(first_object, second_object, "x")
            y_distance = x_or_y_distance(first_object, second_object, "y")
            hypotenuse = math.hypot(x_distance, y_distance)
            # Расстояние высчитываем через функцию поиска гипотенузы "hypot" по двум катетам.
            length[hypotenuse] = {"left_corner": first_object["north_east"],
                                  "wall_info": first_object["wall_info"]}, \
                                 {"right_corner": second_object[counter]["north_west"],
                                  "wall_info": second_object[counter]["wall_info"]}
            # расстояния могут быть одинаковые, но нам по сути неважно какой из вариантов брать, а значит мы
            # можем просто перезаписать ключ словаря

        for item in objects:
            if counter == len(objects):
                counter = 0
            core_and_output(item, objects)
            counter += 1
        return length[max(length)]

    def alternative_free_space_algorithm(self):
        return None

    def longest_distance(self):
        return None



class DataVerificationAndImplementation(FurnitureArrangement):

    def area_calculation(self, figure: Figure) -> float:
        "Метод вычисления площади фигуры."
        if figure.side_a == figure.side_c and figure.side_b == figure.side_d:
            area = figure.side_a * figure.side_b
            return area
        # elif figure.side_b != figure.side_d and figure.side_a == figure.side_c: # Eсли условие выполняется, то фигура является равнобедренной трапецией
        #    trapezoid_height = math.sqrt(pow(figure.side_a, 2) \
        #     - (pow((pow((figure.side_d - figure.side_b), 2) \
        #     + pow(figure.side_a, 2) - pow(figure.side_c, 2)) / (2 \
        #     * (figure.side_d - figure.side_b)), 2)))
        #     area = ((figure.side_d + figure.side_b) / 2) * trapezoid_height
        #     return area
        else: 
            raise IncorrectFigure("Неверно заданы размеры помещения!")

    def area_monitoring(self, area_room: int, area_furniture: int) -> bool:
        "Метод контроля допустимой общей площади мебели в помещении."
        if (area_furniture / area_room) > 0.75:
            raise LackSpace("Общая площадь мебели превышает площадь помещения!")
        return True

    def algorithm_activation(self):
        return None

    def activation(self):
        return None