"""Algorithm."""

import math
from typing import NamedTuple

from exception import LackSpace, IncorrectFigure


class FurnitureArrangement():

    coordinates = []  # хранение координат по схеме "ключ объекта: (координаты, маркеры углов, маркеры точек)
    free_space = [] # хранение расстояний между мебелью через запятую (в виде координат)



    def free_space_algorithm(self, objects: list, walls_length: dict) -> tuple:
        # На вход подается список с координатами углов объектов. Координаты между друг другом минусим, находим
        # по ближайшим неприлегающим углам расстояние по модулю в виде гипотенузы (вычитание по иксу -- это
        # один катет, вычитание по игрику -- другой). И записыванием самое большое расстояние в переменную. Углы
        # разбиты по сторонам света: north_west, north-east, south-west, south-east. Отдельно так же идет
        # значение и длина стены "walls_length": {"first_wall": 1, "second_wall": 2, "third_wall": 1, "fourth_wall": 2}
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
                                  "right_corner": second_object[counter]["north_west"]}, walls_length

            # расстояния могут быть одинаковые, но нам по сути неважно какой из вариантов брать, а значит мы
            # можем просто перезаписать ключ словаря

        for item in objects:
            if counter == len(objects):
                counter = 0
            core_and_output(item, objects)
            counter += 1
        return length[max(length)]

    # Доделать по алгоритму. Вариант с единственным объектом в комнате. Вариант с примыкающими со стороны
    # к объекту стенами. Модернизировать алгоритм на высчитывание расстояния по стене, а не по диагоналям

    def alternative_free_space_algorithm(self):
        return None

    def middle_of_the_distance_on_the_wall(self, free_space: dict, walls: dict) -> dict:
        """
        Функция для нахождения средней точки в оставшемся пустом пространстве комнаты.
        Получает на вход координаты точек и длины стен.
        Возвращает координаты средней точки.
        """
        walls_length = tuple(walls.values())
        room_perimeter = sum(walls_length)

        def convert_coords_to_line(coords: dict, length_of_walls: tuple) -> float|int:
            """Функция преобразует координаты в точку на прямой."""
            nonlocal room_perimeter
            if coords['x'] == 0:
                return coords['y']
            elif coords['y'] == length_of_walls[0]:
                return length_of_walls[0] + coords['x']
            elif coords['x'] == length_of_walls[1]:
                return sum(length_of_walls[:3]) - coords['y']
            return sum(length_of_walls) - coords['x']

        def convert_line_to_coords(point: float|int, length_of_walls: tuple) -> dict:
            """Функция преобразует точку на прямой в координаты"""
            nonlocal room_perimeter
            if 0 <= point <= walls_length[0]:
                return {'x': 0, 'y': point}
            elif walls_length[0] < point <= sum(length_of_walls[:2]):
                return {'x': point - length_of_walls[0], 'y': length_of_walls[0]}
            elif sum(length_of_walls[:2]) < point <= sum(length_of_walls[:3]):
                return {'x': length_of_walls[1], 'y': sum(length_of_walls[:3]) - point}
            elif sum(length_of_walls[:3]) < point <= room_perimeter:
                return {'x': room_perimeter - point, 'y': 0}
            raise Exception('Ошибка данных, нет возможности разместить среднюю точку на одной из стен комнаты.')

        if 'left_corner' in free_space:
            point_1 = convert_coords_to_line(free_space['left_corner'], walls_length)
            point_2 = convert_coords_to_line(free_space['right_corner'], walls_length)
            middle_point = (point_2 + point_1) / 2 if point_1 < point_2 else (point_2 + point_1 + room_perimeter) / 2
            if middle_point > room_perimeter:
                middle_point = middle_point - room_perimeter
            return convert_line_to_coords(middle_point, walls_length)

        elif "middle_point" in free_space:
            point = convert_coords_to_line(free_space["middle_point"], walls_length)
            shifted_point = point


    def placing_in_coordinates(self, middle_point: dict, figure: dict, walls: dict, objects: dict) -> bool:
        """Функция проверки возможности резервирования места для мебели в комнате.

        Args:
            middle_point (dict): {"x": 0, "y": 0}
            figure (dict): координаты для мебели. {"north_west": {"x": 0, "y": 0},
                   "north_east": {"x": 0, "y": 0}, "south_west": {"x": 0, "y": 0}, "south_east": {"x": 0, "y": 0}}
            walls (dict): стены комнаты начиная от левой {"first_wall": 0, "second_wall": 0, "third_wall": 0, "fourth_wall":0}
            objects (dict): словарь с координатами других объектов в комнате

        Returns:
            bool: True, если место зарезервировано, иначе False
        """

        # counter = 0
        # breaker = 0
        # counter_border = 2
        #
        # displacement_start = 0
        # middle_point["displacement_value"] = 7
        # middle_point["shift_method"] = "plus"
        #
        # while counter < counter_border:
        #     for item in objects:
                # Проверяем пересечение с другими объектами в комнате
                # if  item["north_west"]["x"] < figure["north_east"]["x"] <= item["north_east"]["x"] and \
                #     item["north_east"]["y"] < figure["north_east"]["y"] <= item["north_east"]["y"]:
                #
                #
                # elif item["north_west"]["x"] <= figure["north_west"]["x"] < item["north_east"]["x"] and \
                #      item["north_west"]["y"] <= figure["north_west"]["y"] < item["north_east"]["y"]:
                #
                #
                # elif item["south_west"]["x"] > figure["south_east"]["x"] >= item["south_east"]["x"] and \
                #      item["south_west"]["y"] <= figure["south_east"]["y"] < item["north_east"]["y"]:
                #
                #
                # elif item["south_west"]["x"] >= figure["south_west"]["x"] > item["south_east"]["x"] and \
                #      item["south_west"]["y"] <= figure["south_west"]["y"] < item["north_east"]["y"]:
                #
                #
                # else:
                #     breaker += 1


                # Проверяем, что мебель не выходит за пределы комнаты
                # if figure["north_east"]["x"] > walls["second_wall"] \
                # or figure["south_east"]["x"] > walls["second_wall"]:
                #
                #
                # elif figure["north_east"]["y"] > walls["first_wall"] \
                #   or figure["south_east"]["y"] > walls["first_wall"]:
                #
                #
                # elif figure["north_east"]["x"] < 0 or figure["north_west"]["x"] < 0 or \
                #
                #
                # else:
                #     breaker += 1

            #     if breaker == 2:
            #         break
            #
            #     breaker = 0
            #     counter += 1
            #     if counter %2 != 0:
            #         middle_point["shift_method"] = "minus"
            #     elif counter % 2 == 0:
            #         middle_point["shift_method"] = "plus"
            #     displacement_start += middle_point["displacement_value"]
            #
            #
            # if counter < counter_border:
            #     # Если все проверки прошли, добавляем координаты мебели в словарь coordinates
            #     self.coordinates.append(figure)
            #     return True
            #
            # return False


    def corner_markings(self, length_and_width: dict, center: dict, wall_number: int) -> dict:
        """Функция для определения угловых маркеров мебели."""
        # Распаковка исходных данных в кортеж
        x, y, l, w = tuple({**center, **length_and_width}.values())
        # Составление кортежа со всеми вариантами угловых маркеров и словаря с набором маркеров для каждой стены
        options = (x, y, x - l, x + l, x - w / 2, x + w / 2, y - l, y + l, y - w / 2, y + w / 2)
        coord_for_walls = {
            1: (options[0], options[9], options[0], options[8], options[3], options[9], options[3], options[8]),
            2: (options[5], options[1], options[4], options[1], options[5], options[6], options[4], options[6]),
            3: (options[0], options[8], options[0], options[9], options[2], options[8], options[2], options[9]),
            4: (options[4], options[1], options[5], options[1], options[4], options[7], options[5], options[7])
        }

        corners_coordinates = {"north_west": {"x": 0, "y": 0}, "north_east": {"x": 0, "y": 0},
                               "south_west": {"x": 0, "y": 0}, "south_east": {"x": 0, "y": 0}}
        if wall_number in coord_for_walls:
            corners_coordinates["north_east"]["x"] = coord_for_walls[wall_number][0]
            corners_coordinates["north_east"]["y"] = coord_for_walls[wall_number][1]
            corners_coordinates["north_west"]["x"] = coord_for_walls[wall_number][2]
            corners_coordinates["north_west"]["y"] = coord_for_walls[wall_number][3]
            corners_coordinates["south_east"]["x"] = coord_for_walls[wall_number][4]
            corners_coordinates["south_east"]["y"] = coord_for_walls[wall_number][5]
            corners_coordinates["south_west"]["x"] = coord_for_walls[wall_number][6]
            corners_coordinates["south_west"]["y"] = coord_for_walls[wall_number][7]
        else:
            raise Exception('Номер стены указан неверно.')
        return corners_coordinates


# class DataVerificationAndImplementation(FurnitureArrangement):
#
#     def area_calculation(self, figure: Figure) -> float:
#         "Метод вычисления площади фигуры."
#         if figure.side_a == figure.side_c and figure.side_b == figure.side_d:
#             area = figure.side_a * figure.side_b
#             return area
#
#         else:
#             raise IncorrectFigure("Неверно заданы размеры помещения!")
#
#     def area_monitoring(self, area: dict) -> bool:
#         "Метод контроля допустимой общей площади мебели в помещении."
#         if (area["area_furniture"] / area["area_room"]) > 0.75:
#             raise LackSpace("Общая площадь мебели превышает площадь помещения!")
#         return True
#
#     def algorithm_activation(self, furniture: tuple, room_size: dict, random_switcher: bool):
#         furniture_check = self.area_monitoring(db_operations(furniture))
#         # надо дописать функции с возратом данных из бд и переделать входящие данные для area_monitoring
#
#         if furniture_check is False:
#             raise_area_error(False)
#
#         # прописать функцию ошибки с выводом во фронт
#
#         def activation_core(algorithm_type):
#             counter = 1
#             while counter != len(furniture):
#                 result_free_space = algorithm_type(db_operations(furniture))
#                 self.middle_of_the_distance_on_the_wall(result_free_space)
#                 draw_objects(self.coordinates)
#                 counter += 1
#
#         if random_switcher is True:
#             # условные переменные вызова (пока что)
#             activation_core(self.random_free_space_algorithm(db_operations(furniture)))
#
#         elif random_switcher is False:
#             activation_core(self.free_space_algorithm(db_operations(furniture)))
#

    # def room_coordinates(self, figure: dict) -> tuple:
    #     "Метод создания координат комнаты."
    #     room_coordinates = (
    #         {"west_wall": {"x_1": 0, "y_1": 0, "x_2": 0, "y_2": figure.side_a}},
    #         {"north_wall": {"x_1": 0, "y_1": figure.side_a, "x_2": figure.side_b, "y_2": figure.side_a}},
    #         {"east_wall": {"x_1": figure.side_b, "y_1": figure.side_c, "x_2": figure.side_b, "y_2": 0}},
    #         {"south_wall": {"x_1": figure.side_d, "y_1": 0, "x_2": 0, "y_2": 0}})
    #     return room_coordinates
