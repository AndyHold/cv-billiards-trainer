import cv2
import numpy as np

from Models.Filters.ColourSpaceConverter import ColourSpaceConverter
from Models.Filters.MiddleSectionCropper import MiddleSectionCropper
from Models.Filters.Morphology import Morphology
from Models.Obstacles.Ball import Ball


class HoughCircles:

    def __init__(self, canny_threshold=None, accumulator_threshold=None, min_radius=None, max_radius=None):
        if canny_threshold and accumulator_threshold and min_radius and max_radius:
            self.name = False
            self.canny_threshold = canny_threshold
            self.accumulator_threshold = accumulator_threshold
            self.min_radius = min_radius
            self.max_radius = max_radius

    def get_balls(self, frame):
        mhi = MiddleSectionCropper.max_hue_index(frame)
        hsv_fil = ColourSpaceConverter.get_hsv_filtered(frame, mhi, 30, 30)

        open_close = Morphology.open_close(hsv_fil)

        circles = cv2.HoughCircles(open_close,
                                   cv2.HOUGH_GRADIENT,
                                   1,
                                   20,
                                   param1=self.canny_threshold,
                                   param2=self.accumulator_threshold,
                                   minRadius=self.min_radius,
                                   maxRadius=self.max_radius)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            balls = []
            for circle in circles[0]:
                balls.append(Ball((float(circle[0]), float(circle[1]), float(circle[2]))))
            return balls
        else:
            return None

    def destroy(self):
        if self.name:
            cv2.destroyWindow(self.name)
