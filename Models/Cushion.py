from Common.Utilities import Utilities, ParallelLineException, LineOverlayException


class Cushion:

    def __init__(self, line):
        self.start = line[0]
        self.end = line[1]

    def intersect(self, position, direction, radius):
        try:
            ### Add Buffer for radius!!!!!
            intersection_point = Utilities.find_lines_intersection(
                list(self.start) + list(self.end),
                list(position) + [direction[0] * position[0], direction[1] * position[1]])
            if not Utilities.is_inbetween(self.start, self.end, intersection_point):
                return False
            else:
                vector_difference = (position[0] - intersection_point[0], position[1] - intersection_point[1])
                return Utilities.vector_length(vector_difference)

        except ParallelLineException:
            return False
        except LineOverlayException:
            return False

    def normal(self, point):
        xdiff = float(self.start[0] - self.end[0])
        ydiff = float(self.start[1] - self.end[1])
        gradient = ydiff / xdiff
        normal_gradient = -1 / gradient

        if self.is_right(point):
            return Utilities.normalize((1, 1 * normal_gradient))
        else:
            return Utilities.normalize((-1, -1 * gradient))

    def is_right(self, point):
        x, y = point
        x1, y1 = self.start
        x2, y2 = self.end

        d = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
        return d > 0
