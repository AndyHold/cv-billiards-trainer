import cv2
import numpy as np


class HoughLines:

    def __init__(self, min_length, max_gap):
        self.min_length = min_length
        self.max_gap = max_gap

    def get_lines(self, frame):
        edges = cv2.Canny(frame, 50, 100)
        return cv2.HoughLinesP(edges, 1, np.pi / 180, 75, minLineLength=self.min_length, maxLineGap=self.max_gap), edges
