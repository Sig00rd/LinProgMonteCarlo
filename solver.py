from typing import Dict, Any

from parser import Parser
import speaker
import points

from queue import Queue

# magical numbers
POINTS_PER_ITERATION = 1000
STARTING_RADIUS = 4000
RELATIVE_DIFFERENCE_THRESHOLD = 0.01
MAX_NUMBER_OF_RETRIES = 50


# get data from user
variable_list = speaker.get_variables()
dziedzina = "r"
constraint_list = speaker.get_constraint_functions()
goal_function = speaker.get_goal_function()
objective = speaker.get_min_or_max()
new_parser = Parser()

fail_count = 0

# set starting point, value at point and radius
starting_point = points.generate_starting_point(variable_list, STARTING_RADIUS)
current_radius = STARTING_RADIUS
current_best_point, current_best_value = starting_point, None

while True:
    points_queue = Queue()
    valid_points = []

    for i in range(POINTS_PER_ITERATION):
        if dziedzina == "n":
            new_point = points.generate_point_int(current_best_point,
                                                  current_radius, variable_list)
        else:
            new_point = points.generate_point(current_best_point,
                                              current_radius, variable_list)
        points_queue.put(new_point)

    while not points_queue.empty():
        point = points_queue.get()
        if points.check_point_for_constraints(new_parser, point, constraint_list) is True:
            goal_function_value_at_point = new_parser.evaluate(goal_function, point)
            valid_points.append((point, goal_function_value_at_point))
        points_queue.task_done()

    if objective == "max":
        try:
            current_step_best_point, current_step_best_value = points.get_best_point_and_value(valid_points, objective)
            # if there was no valid point previously or this step's best point is better than current best
            if current_best_value is None or\
                    current_step_best_value * (1 - RELATIVE_DIFFERENCE_THRESHOLD) > current_best_value:

                fail_count = 0
                current_radius = points.distance(current_best_point, current_step_best_point, variable_list)
                current_best_point = current_step_best_point
                current_best_value = current_step_best_value

            else:
                fail_count += 1
                if fail_count >= MAX_NUMBER_OF_RETRIES/2:
                    break

        # if this step yields no valid point
        except points.ListEmptyError:
            fail_count += 1
            if fail_count >= MAX_NUMBER_OF_RETRIES:
                break

    else:
        try:
            current_step_best_point, current_step_best_value = points.get_best_point_and_value(valid_points, objective)
            # if there was no valid point previously or this step's best point is better than current best
            if current_best_value is None or\
                    current_step_best_value * (1+RELATIVE_DIFFERENCE_THRESHOLD) < current_best_value:

                fail_count = 0
                current_radius = points.distance(current_best_point, current_step_best_point, variable_list)
                current_best_point = current_step_best_point
                current_best_value = current_step_best_value

            else:
                fail_count += 1
                if fail_count >= MAX_NUMBER_OF_RETRIES/2:
                    break

        # if this step yields no valid point
        except points.ListEmptyError:
            fail_count += 1
            if fail_count >= MAX_NUMBER_OF_RETRIES:
                break


points.present(current_best_point, variable_list, current_best_value)
