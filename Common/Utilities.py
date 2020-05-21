import cv2
import numpy as np

from Common.Exceptions import *


class Utilities:

    @staticmethod
    def calculate_line_average(lines: list) -> list:
        """
        Calculates the average line of a list of lines.

        :type lines: list list of lines to calculate average of.
        :raises EmptyLinesException when the list is empty or None
        """
        sums = {"x1": 0.0, "x2": 0.0, "y1": 0.0, "y2": 0.0}
        averages = {"x1": 0.0, "x2": 0.0, "y1": 0.0, "y2": 0.0}

        if type(lines) is not list or len(lines) == 0:
            raise EmptyListException()

        num_lines = len(lines)
        for line in lines:
            num_lines += 1
            for x1, y1, x2, y2 in line:
                sums["x1"] += x1
                sums["x2"] += x2
                sums["y1"] += y1
                sums["y2"] += y2

        for key in sums.keys():
            averages[key] = sums[key] / num_lines

        return [averages["x1"], averages["y1"], averages["x2"], averages["y2"]]

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
