import math

from Common.Utilities import Utilities


class Ball:

    def __init__(self, circle):
        self.position = (circle[0], circle[1])
        self.radius = circle[2]

    def intersect(self, position, direction, radius):
        norm = self.normal(position)
        vector_difference = (self.position[0] - position[0], self.position[1] - position[1])
        vdotn = Utilities.dot(direction, norm)
        if abs(vdotn) < 1.e-4:
            return False
        t = Utilities.dot(vector_difference, norm) / vdotn
        if abs(t) < 0.001:
            return False
        q = (position[0] + direction[0] * t, position[1] + direction[1] * t)
        if self.is_inside(q, radius):
            return t
        else:
            return False

    def normal(self, point):
        x = point[0] - self.position[0]
        y = point[1] - self.position[1]

        return Utilities.normalize((x, y))

    def is_inside(self, point, radius):
        vector_difference = (self.position[0] - point[0], self.position[1] - point[1])
        vector_difference_length = Utilities.vector_length(vector_difference)
        return vector_difference_length < self.radius + radius
