from Common.Utilities import Utilities, ParallelLineException, LineOverlayException


class Cushion:

    def __init__(self, line):
        # This part is not essential it just helps me to imagine it in my head
        if abs(line[0] - line[2]) > 100:
            # lines are vertical
            if line[1] < line[3]:
                self.start = (line[0], line[1])
                self.end = (line[2], line[3])
            else:
                self.start = (line[2], line[3])
                self.end = (line[0], line[1])
        else:
            # lines are horizontal
            if line[0] < line[2]:
                self.start = (line[0], line[1])
                self.end = (line[2], line[3])
            else:
                self.start = (line[2], line[3])
                self.end = (line[0], line[1])

        self.gradient = self.find_gradient()
        self.normal_gradient = -1 / self.gradient

    def find_gradient(self) -> float:
        xdiff = float(self.start[0] - self.end[0])
        ydiff = float(self.start[1] - self.end[1])
        return ydiff / xdiff

    def intersect(self, position, direction, radius):
        try:
            if self.is_right(position):
                norm_gradient = Utilities.normalize((1, self.normal_gradient * 1))
            else:
                norm_gradient = Utilities.normalize(( self.normal_gradient * 1, 1))
            start = (self.start[0] + norm_gradient[0] * radius, self.start[1] + norm_gradient[1] * radius)
            end = (self.end[0] + norm_gradient[0] * radius, self.end[1] + norm_gradient[1] * radius)

            intersection_point = Utilities.find_lines_intersection(
                list(start) + list(end),
                list(position) + [direction[0] * position[0], direction[1] * position[1]])
            if not Utilities.is_inbetween(start, end, intersection_point):
                return False
            else:
                vector_difference = (position[0] - intersection_point[0], position[1] - intersection_point[1])
                return Utilities.vector_length(vector_difference)

        except ParallelLineException:
            return False
        except LineOverlayException:
            return False

    def normal(self, point):

        if self.is_right(point):
            return Utilities.normalize((1, 1 * self.normal_gradient))
        else:
            return Utilities.normalize((-1, -1 * self.gradient))

    def is_right(self, point):
        x, y = point
        x1, y1 = self.start
        x2, y2 = self.end

        d = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
        return d > 0
