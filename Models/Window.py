"""
:author: Andrew Holden
"""
import cv2


class Window:

    def __init__(self, name):
        self.name = name
        cv2.namedWindow(name)

    def update_window(self, frame):
        cv2.imshow(self.name, frame)

    def destroy(self):
        cv2.destroyWindow(self.name)
