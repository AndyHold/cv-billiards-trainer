import cv2
import numpy as np


class ColourSpaceConverter:

    @staticmethod
    def get_hsv_filtered(frame, max_hue_index, negative_threshold, positive_threshold):
        hsv_colour = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hue_min = np.array([int(max_hue_index[0]) - negative_threshold, 20, 20], np.uint8)
        hue_max = np.array([int(max_hue_index[0]) + positive_threshold, 255, 255], np.uint8)

        return cv2.inRange(hsv_colour, hue_min, hue_max)
