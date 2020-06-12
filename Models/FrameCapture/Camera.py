"""Module containing a camera to get frames from

Used in computer vision projects

:author: Andrew Holden

    Typical usage example:

    camera = Camera(-1)
    camera.update_brightness(50)
    camera.update_contrast(50)
    camera.update_saturation(50)

    while True:
        frame = camera.get_frame()

        if not is_frame_valid():
            break

        # Do something with frame.
"""
import cv2

from Models.FrameCapture.FrameCapture import FrameCapture


class Camera (FrameCapture):

    def __init__(self, cam_num):
        self.camera = cv2.VideoCapture(cam_num)

    def update_brightness(self, brightness):
        self.camera.set(cv2.CAP_PROP_BRIGHTNESS, brightness / 100)

    def update_contrast(self, contrast):
        self.camera.set(cv2.CAP_PROP_CONTRAST, contrast / 100)

    def update_saturation(self, saturation):
        self.camera.set(cv2.CAP_PROP_SATURATION, saturation / 100)

    def get_frame(self):
        _, frame = self.camera.read()
        return frame

    def release(self):
        self.camera.release()

    def is_frame_valid(self):
        return True

    def is_opened(self):
        return self.camera.isOpened()
