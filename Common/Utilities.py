import cv2
import numpy as np

from Common.Exceptions import *


class Utilities:

    @staticmethod
    def find_bounds_exit_point(height, width, start, direction):
        top = [0, 0, width, 0]
        bottom = [0, height, width, height]
        left = [0, 0, 0, height]
        right = [width, 0, width, height]
        try:
            left_point = Utilities.find_lines_intersection(left, list(start) + [start[0] + direction[0], start[1] + direction[1]])
            if Utilities.is_inbetween(left[:2], left[2:], left_point):
                return left_point
        except LineOverlayException:
            pass
        try:
            right_point = Utilities.find_lines_intersection(right, list(start) + [start[0] + direction[0],
                                                                              start[1] + direction[1]])
            if Utilities.is_inbetween(right[:2], right[2:], right_point):
                return right_point
        except LineOverlayException:
            pass
        try:
            top_point = Utilities.find_lines_intersection(top, list(start) + [start[0] + direction[0], start[1] + direction[1]])
            if Utilities.is_inbetween(top[:2], top[2:], top_point):
                return top_point
        except LineOverlayException:
            pass
        try:
            bottom_point = Utilities.find_lines_intersection(bottom, list(start) + [start[0] + direction[0],
                                                                                start[1] + direction[1]])
            if Utilities.is_inbetween(bottom[:2], bottom[2:], bottom_point):
                return bottom_point
        except LineOverlayException:
            pass

        if direction[0] < 0:
            if direction[1] < 0:
                return 0, 0
            else:
                return 0, height
        else:
            if direction[1] < 0:
                return width, 0
            else:
                return width, height



    @staticmethod
    def calculate_line_average(lines: list) -> list:
        """
        Calculates the average line of a list of lines.

        :type lines: list list of lines to calculate average of.
        :raises EmptyLinesException when the list is empty or None
        """
        sums = {"x1": 0.0, "x2": 0.0, "y1": 0.0, "y2": 0.0}
        averages = {"x1": 0.0, "x2": 0.0, "y1": 0.0, "y2": 0.0}

        if len(lines) == 0:
            raise EmptyListException()

        num_lines = float(len(lines))
        for line in lines:
            if len(line) == 4:
                line = [line]
            for x1, y1, x2, y2 in line:
                sums["x1"] += x1
                sums["x2"] += x2
                sums["y1"] += y1
                sums["y2"] += y2

        for key in sums.keys():
            averages[key] = sums[key] / num_lines

        return [averages["x1"], averages["y1"], averages["x2"], averages["y2"]]

    @staticmethod
    def shortest_distance_two_lines(line1, line2):
        """
        Finds the shortest distance between two line segments

        :param line1: the first line [x1, y1, x2, y2]
        :param line2: the second line [x1, y1, x2, y2]
        :return: the shortest distance as a float.
        """
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2
        dist1 = Utilities.line_point_distance(line2, (x1, y1))
        dist2 = Utilities.line_point_distance(line2, (x2, y2))
        dist3 = Utilities.line_point_distance(line1, (x3, y3))
        dist4 = Utilities.line_point_distance(line1, (x4, y4))

        return min(dist1, dist2, dist3, dist4)

    @staticmethod
    def line_point_distance(line, point):
        """
        Finds the closest distance between a line segment and a point

        :param line: the line segment represented by [x1, y1, x2, y2]
        :param point: the point represented by (x, y)
        :return: the distance as a float
        """
        x1, y1, x2, y2 = line
        x3, y3 = point

        x_delta = x2 - x1
        y_delta = y2 - y1
        if x_delta == 0 and y_delta == 0:
            return None
        u = ((x3 - x1) * x_delta + (y3 - y1) * y_delta) / (x_delta * x_delta + y_delta * y_delta)

        if u < 0:
            closest_x = x1
            closest_y = y1
        elif u > 1:
            closest_x = x2
            closest_y = y2
        else:
            closest_x = x1 + u * x_delta
            closest_y = y1 + u * y_delta

        return np.math.sqrt((closest_x - x3) ** 2 + (closest_y - y3) ** 2)

    @staticmethod
    def add_horizontal_lines(lines: list) -> list:
        """
        Adds a group of lines together

        :type lines: list list of lines to add.
        :raises EmptyLinesException when the list is empty or None
        """
        max_x = -1
        max_y = -1
        min_x = -1
        min_y = -1

        if type(lines) is not list or len(lines) == 0:
            raise EmptyListException()

        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 > max_x:
                    max_x, min_y = x1, y1
                if x1 < min_x:
                    min_x, min_y = x1, y1
                if x2 > max_x:
                    max_x, max_y = x2, y2
                if x2 < min_x:
                    min_x, min_y = x2, y2

        return [min_x, min_y, max_x, max_y]

    @staticmethod
    def add_vertical_lines(lines: list) -> list:
        """
        Adds a group of lines together

        :type lines: list list of lines to add.
        :raises EmptyLinesException when the list is empty or None
        """
        max_x = -1
        max_y = -1
        min_x = -1
        min_y = -1

        if type(lines) is not list or len(lines) == 0:
            raise EmptyListException()

        for line in lines:
            for x1, y1, x2, y2 in line:
                if y1 > max_y:
                    max_x, min_y = x1, y1
                if y1 < min_y:
                    min_x, min_y = x1, y1
                if y2 > max_y:
                    max_x, max_y = x2, y2
                if y2 < min_y:
                    min_x, min_y = x2, y2

        return [min_x, min_y, max_x, max_y]

    @staticmethod
    def find_lines_intersection(line1: list, line2: list) -> list:
        """
        Finds the intersection of two lines.

        :type line1: list list of coordinates that represent the first line, format: [x1, y1, x2, y2]
        :type line2: list list of coordinates that represent the second line, format: [x3, y3, x4, y4]
        :raises LineOverlayException when line2 is an overlay of line 1 (they intersect at multiple points)
        :raises ParallelLineException when the two lines are parallel (they do not intersect)
        """
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        a = (x1 * y2 - y1 * x2)
        b = (x3 * y4 - y3 * x4)
        c = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if abs(a) < 0.0001 or abs(b) < 0.0001:
            raise LineOverlayException()
        elif abs(c) < 0.0001:
            raise ParallelLineException()

        x_position = (a * (x3 - x4) - (x1 - x2) * b) / c
        y_position = (a * (y3 - y4) - (y1 - y2) * b) / c
        return [x_position, y_position]

    @staticmethod
    def get_average_colour(circle, frame):
        """
        Finds the average colour of a circle.

        :type circle: tuple(tuple(float, float), float) the location (x, y) and radius of the circle
        :type frame: list the image containing the circle
        :return: the average colour of the circle
        """
        x, y, radius = circle
        circle_mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
        cv2.circle(circle_mask, (x, y), radius, (255, 255, 255), cv2.FILLED)
        return cv2.mean(frame, mask=circle_mask)[::-1]

    @staticmethod
    def draw_ball_path(frame, circles):
        if len(circles) > 1:
            x1, y1, radius = circles[0]
            circle_mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            cv2.circle(circle_mask, (x1, y1), radius, (255, 255, 255), cv2.FILLED)
            colour = Utilities.get_average_colour(circles[0], frame)
            for line in circles[1:]:
                x2, y2, _ = line
                cv2.line(frame, (x1, y1), (x2, y2), colour, thickness=2 * radius or 1, mask=circle_mask)
                x1, y1, _ = line

    @staticmethod
    def draw_lines(lines, frame):
        for x1, y1, x2, y2 in lines:
            cv2.line(
                frame,
                (int(round(x1)), int(round(y1))),
                (int(round(x2)), int(round(y2))),
                (100, 100, 100),
                thickness=4
            )

    @staticmethod
    def find_reflection(normal, direction):
        i_dot_n = Utilities.dot(direction, normal)
        return direction[0] - 2 * i_dot_n * normal[0], direction[1] - 2 * i_dot_n * normal[1]

    @staticmethod
    def normalize(point):
        length = Utilities.vector_length(point)

        return point[0] / length, point[1] / length

    @staticmethod
    def dot(x, y):
        return sum(float(x_i) * float(y_i) for x_i, y_i in zip(x, y))

    @staticmethod
    def find_perpendicular_vector(vector, origin_line, collided_ball_position):
        x, y = vector
        x1, x2 = 1, -1
        perp1 = Utilities.normalize((x1, (-x * x1) / y))
        perp2 = Utilities.normalize((x2, (-x * x2) / y))

        perp_point1 = (collided_ball_position[0] + perp1[0], collided_ball_position[1] + perp1[1])
        perp_point2 = (collided_ball_position[0] + perp2[0], collided_ball_position[1] + perp2[1])
        if Utilities.is_right(collided_ball_position, origin_line):
            if Utilities.is_right(perp_point1, origin_line):
                return perp_point2
            return perp_point1
        if Utilities.is_right(perp_point1, origin_line):
            return perp_point1
        return perp_point2

    @staticmethod
    def is_right(point, line):
        x, y = point
        x1, y1, x2, y2 = line

        d = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
        return d > 0

    @staticmethod
    def vector_length(vector):
        return np.math.sqrt(np.math.pow(vector[0], 2) + np.math.pow(vector[1], 2))

    @staticmethod
    def is_inbetween(start, end, point) -> bool:
        x, y = point
        x1, y1 = start
        x2, y2 = end
        beta = y2 - y1
        delta = x2 - x1
        if abs(delta) < 1:
            return x1 < x < x2 or x1 > x > x2
        if abs(beta) < 1:
            return y1 < y < y2 or y1 > y > y2
        return (x1 < x < x2 or x1 > x > x2) and (y1 < y < y2 or y1 > y > y2)
