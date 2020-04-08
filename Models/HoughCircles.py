import cv2
import numpy as np


class HoughCircles:

    def __init__(self, canny_threshold=None, accumulator_threshold=None, min_radius=None, max_radius=None):
        if canny_threshold and accumulator_threshold and min_radius and max_radius:
            self.name = False
            self.canny_threshold = canny_threshold
            self.accumulator_threshold = accumulator_threshold
            self.min_radius = min_radius
            self.max_radius = max_radius
        else:
            self.name = "Track Bars"
            cv2.namedWindow(self.name)
            cv2.createTrackbar('Canny Threshold', self.name, 1, 500, lambda x: None)
            cv2.createTrackbar('Accumulator Threshold', self.name, 1, 500, lambda x: None)
            cv2.createTrackbar("Min Radius", self.name, 0, 100, lambda x: None)
            cv2.createTrackbar("Max Radius", self.name, 1, 100, lambda x: None)

            cv2.setTrackbarPos("Max Radius", self.name, 100)
            cv2.setTrackbarPos("Canny Threshold", self.name, 100)
            cv2.setTrackbarPos("Accumulator Threshold", self.name, 20)

    def get_circles(self, frame):
        blur = cv2.GaussianBlur(frame, (9, 9), 0)
        # Convert the image to grayscale for processing
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

        if self.name:
            self.canny_threshold = cv2.getTrackbarPos('Canny Threshold', self.name)
            self.accumulator_threshold = cv2.getTrackbarPos('Accumulator Threshold', self.name)
            self.min_radius = cv2.getTrackbarPos('Min Radius', self.name)
            self.max_radius = cv2.getTrackbarPos('Max Radius', self.name)

        circles = cv2.HoughCircles(gray,
                                   cv2.HOUGH_GRADIENT,
                                   1,
                                   20,
                                   param1=self.canny_threshold,
                                   param2=self.accumulator_threshold,
                                   minRadius=self.min_radius,
                                   maxRadius=self.max_radius)

        if circles is not None:
            return np.uint16(np.around(circles))

        else:
            return None

    def destroy(self):
        if self.name:
            cv2.destroyWindow(self.name)
