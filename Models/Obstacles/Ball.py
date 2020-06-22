from Common.Utilities import Utilities
from Models.Obstacles.Obstacle import Obstacle
import numpy as np


class Ball(Obstacle):

    def __init__(self, circle):
        self.position = (circle[0], circle[1])
        self.radius = circle[2]

    def intersect(self, position, direction, radius):
        a = np.power(Utilities.vector_length(direction), 2)
        om = [
            position[0] - self.position[0],
            position[1] - self.position[1]
        ]
        b = 2 * Utilities.dot(direction, om)
        c = np.power(Utilities.vector_length(om), 2) - np.power((radius + self.radius), 2)
        q = np.power(b, 2) - 4 * a * c
        if q <= 0:
            return -1, None

        g = 1 / (2 * a)
        q = g * np.sqrt(q)
        b = -b * g

        return Utilities.vector_length((direction[0] * (b - q), direction[1] * (b - q))), None

    def normal(self, point):
        x = point[0] - self.position[0]
        y = point[1] - self.position[1]

        return Utilities.normalize((x, y))

    def is_inside(self, point, radius):
        print(f"point {point}")
        print(f"radius {radius}")
        vector_difference = (self.position[0] - point[0], self.position[1] - point[1])
        vector_difference_length = Utilities.vector_length(vector_difference)
        return vector_difference_length < 2 * self.radius + 2 * radius

    def get_type(self) -> str:
        return "Ball"
