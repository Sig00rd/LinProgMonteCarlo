import math
import random

from queue import Queue

RELATIVE_BOUNDARY_THICKNESS = 0.05
RELATIVE_RADIUS_ENLARGEMENT = 1.5


class QueueEmptyException(Exception):
    pass


def generate_point(previous_best_point, radius, variables):
    _point = {}
    for variable in variables:
        start = 0.0
        end = previous_best_point[variable] + radius

        if previous_best_point[variable] - radius > 0:
            start = previous_best_point[variable]

        _point[variable] = random.uniform(start, end)
    return _point


def generate_starting_point(variables, _starting_radius):
    _point = {}
    for variable in variables:
        _point[variable] = 0.0
    return _point


def check_point_for_constraints(parser, given_point, constraints):
    for constraint in constraints:
        if parser.evaluate(constraint, given_point) is not True:
            return False
    return True


def distance(point1, point2):
    total_distance = 0.0
    for variable in point1:
        total_distance += (point1[variable] - point2[variable])**2
    return math.sqrt(total_distance)


def present(point, variables, best_value):
    if best_value is None:
        print("Nie znaleziono punktu spełniajacego założenia :-(")
    else:
        for variable in variables:
            print("Wartość: {0:8.8f} zmiennej {1}:".format(point[variable], variable))

        print("Wartość funkcji celu w tym punkcie: {:8.4f}".format(best_value))


def get_best_point_and_value(point_queue, _objective):
    if point_queue.empty():
        raise QueueEmptyException()

    else:
        _point, _value = point_queue.get()

        while not point_queue.empty():
            new_point, new_point_value = point_queue.get()

            if _objective == "max":
                if new_point_value > _value:
                    _point, _value = new_point, new_point_value
            else:
                if new_point_value < _value:
                    _point, _value = new_point, new_point_value

        return _point, _value


def choose_new_radius(previous_radius, point1, point2):
    _distance = distance(point1, point2)
    relative_difference = math.fabs(previous_radius - _distance)/previous_radius
    if relative_difference <= RELATIVE_BOUNDARY_THICKNESS:
        return previous_radius * 1.5
    else:
        return _distance


def fill_queue_with_points(q, queue_size, best_point, radius, variables):
    for i in range(queue_size):
        new_point = generate_point(best_point, radius, variables)
        q.put(new_point)

