"""
Class file to represent a collision of two objects.

:author: Andrew Holden
"""


class Collision:

    def __init__(self, object_collided, remaining_balls, position_at_collision):
        self.object_collided = object_collided
        self.remaining_balls = remaining_balls
        self.position_at_collision = position_at_collision
