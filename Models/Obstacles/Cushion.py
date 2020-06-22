from Common.Utilities import Utilities, ParallelLineException, LineOverlayException
from Models.Obstacles.Obstacle import Obstacle


class Cushion(Obstacle):

    def __init__(self, line, line_orientation):
        self.orientation = line_orientation
        # This part is not essential it just helps me to imagine it in my head
        if self.orientation in ["left", "right"]:  # Line is vertical
            if line[1] < line[3]:
                self.start = (line[0], line[1])
                self.end = (line[2], line[3])
            else:
                self.start = (line[2], line[3])
                self.end = (line[0], line[1])
        else:  # Line is horizontal
            if line[0] < line[2]:
                self.start = (line[0], line[1])
                self.end = (line[2], line[3])
            else:
                self.start = (line[2], line[3])
                self.end = (line[0], line[1])

        self.gradient = self.find_gradient()
        try:
            self.normal_gradient = -1 / self.gradient
        except ZeroDivisionError:
            # Line must be horizontal
            self.normal_gradient = -1000000.0

    def find_gradient(self) -> float:
        xdiff = float(self.start[0] - self.end[0])
        ydiff = float(self.start[1] - self.end[1])
        try:
            return ydiff / xdiff
        except ZeroDivisionError:
            # Line must be vertical
            return 1000000.0

    def get_imaginary_line(self, radius):
        if self.orientation is "left":
            return [
                self.start[0] + radius,
                self.start[1],
                self.end[0] + radius,
                self.end[1]
            ]
        elif self.orientation is "right":
            return [
                self.start[0] - radius,
                self.start[1],
                self.end[0] - radius,
                self.end[1]
            ]
        elif self.orientation is "top":
            return [
                self.start[0],
                self.start[1] + radius,
                self.end[0],
                self.end[1] + radius
            ]
        else:
            return [
                self.start[0],
                self.start[1] - radius,
                self.end[0],
                self.end[1] - radius
            ]

    def intersect(self, position, direction, radius):
        imaginary_line = self.get_imaginary_line(radius)
        try:
            intersection_point = Utilities.find_lines_intersection(
                imaginary_line,
                list(position) + [
                    direction[0] + position[0],
                    direction[1] + position[1]
                ])
            if (direction[0] < 0 and intersection_point[0] > position[0]) or \
                    (direction[0] > 0 and intersection_point[0] < position[0]):
                return -1.0, None
            if not Utilities.is_inbetween(imaginary_line[:2], imaginary_line[2:], intersection_point):
                return -1.0, None

            vector_difference = (position[0] - intersection_point[0], position[1] - intersection_point[1])
            return Utilities.vector_length(vector_difference), intersection_point

        except ParallelLineException:
            return -1.0, None
        except LineOverlayException:
            return -1.0, None

    def normal(self, point):
        if self.orientation is "left":
            return Utilities.normalize((1, 1 * self.normal_gradient))
        if self.orientation is "right":
            return Utilities.normalize((-1, -1 * self.normal_gradient))
        if self.orientation is "top":
            if self.normal_gradient > 0:
                return Utilities.normalize((1, 1 * self.normal_gradient))
            else:
                return Utilities.normalize((1, -1 * self.normal_gradient))
        if self.orientation is "bottom":
            if self.normal_gradient > 0:
                return Utilities.normalize((1, -1 * self.normal_gradient))
            else:
                return Utilities.normalize((1, 1 * self.normal_gradient))


    def get_type(self):
        return "Cushion"
