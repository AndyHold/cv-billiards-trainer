"""Module containing a video reader to get frames from

Used in computer vision projects

:author: Andrew Holden

    Typical usage example:

    video_reader = VideoReader("input.avi")

    while video_reader.next_available():
        frame = videoReader.get_frame()

        if not video_reader.is_frame_valid():
            break;

        # Do something with frame.
"""
import cv2

from Models.FrameCapture.FrameCapture import FrameCapture


class VideoReader(FrameCapture):

    def __init__(self, filename):
        self.filename = filename
        self.video = cv2.VideoCapture(filename)
        self.frame_available = True

    def is_opened(self):
        return self.video.isOpened()

    def get_frame(self):
        self.frame_available, frame = self.video.read()
        return frame

    def is_frame_valid(self) -> bool:
        return self.frame_available

    def release(self):
        self.video.release()
