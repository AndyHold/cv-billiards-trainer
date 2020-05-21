"""
Exceptions Module for use in a computer vision project
:author: Andrew Holden
"""


class ParallelLineException(Exception):
    """
    Raised when lines are parallel. Specifically when looking for an intersection point.
    """

    def __init__(self):
        super()


class LineOverlayException(Exception):
    """
    Raised when lines overlay. Specifically when looking for an intersection point.
    """

    def __init__(self):
        super()


class EmptyListException(Exception):
    """
    Raised when a list is empty.
    """

    def __init__(self):
        super()


class ListTooShortException(Exception):
    """
    Raised when a list does not have the required amount of items.
    """

    def __init__(self):
        super()
