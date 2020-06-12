"""Module containing a frame capture abstract class to get frames from

Used in computer vision projects

:author: Andrew Holden

    defines the methods required for a frame capture class.
"""
from abc import abstractmethod


class FrameCapture:

    @abstractmethod
    def get_frame(self):
        """
        Returns a frame to be used by a computer vision project.

        :return: frame
        """
        pass

    @abstractmethod
    def release(self):
        """
        Releases all resources used by the class.
        """
        pass

    @abstractmethod
    def is_frame_valid(self) -> bool:
        """
        Checks if the current frame is valid.

        :return: True if the current frame is valid.
        """
        pass
