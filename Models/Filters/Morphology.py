import cv2
import numpy as np


class Morphology:

    @staticmethod
    def open_morph(frame):
        ones = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(frame, cv2.MORPH_OPEN, ones)

    @staticmethod
    def close_morph(frame):
        ones = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(frame, cv2.MORPH_CLOSE, ones)

    @staticmethod
    def open_close(frame):
        return Morphology.close_morph(Morphology.open_morph(frame))
