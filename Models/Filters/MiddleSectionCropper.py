import cv2
import numpy as np


class MiddleSectionCropper:

    @staticmethod
    def crop_frame(frame):
        height, width, _ = frame.shape
        middle_section = frame[int(height / 3): int(3 * height / 4),
                         int(width / 3): int(2 * width / 3)]
        return cv2.cvtColor(middle_section, cv2.COLOR_BGR2HSV)

    @staticmethod
    def max_hue_index(frame):
        hist = cv2.calcHist(MiddleSectionCropper.crop_frame(frame), [0], None, [180], [0, 180])
        max_hue_index = np.where(hist == np.max(hist))
        if len(max_hue_index) > 1:
            max_hue_index = max_hue_index[0]

        return max_hue_index
