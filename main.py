""" COSC428 Project - Billiards Trainer.

The objective of this program is to enable a pool player to predict
exactly where his or her shots are going to go before making them.
The program when run will identify the billiards table, the balls on the table,
and the direction of the cue. From this information the trajectory of the white
ball will be calculated and displayed along with any balls that are potentially
contacted by the white ball when hit.
"""

import cv2

from Models.Camera import Camera
from Models.HoughCircles import HoughCircles
from Models.VideoRecorder import VideoRecorder
from Models.Window import Window


def main():
    camera = Camera(-1)
    window = Window("Show me the camera")
    video_recorder = VideoRecorder("output.avi", (640, 480))
    recording = False
    hough_circles = HoughCircles(100, 30, 20, 60)
    # hough_circles = HoughCircles()

    while True:
        frame = camera.get_frame()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) & 0xFF == ord('r'):
            recording = not recording

        frame_copy = frame.copy()
        circles = hough_circles.get_circles(frame)
        if circles is not None:
            for i in circles[0, :]:
                # Draw the outer circle
                cv2.circle(frame_copy, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # Draw the center of the circle
                cv2.circle(frame_copy, (i[0], i[1]), 2, (0, 0, 255), 3)

        if recording:
            video_recorder.write_frame(frame_copy)

        window.update_window(frame_copy)

    video_recorder.release()
    camera.release()
    window.destroy()
    hough_circles.destroy()


if __name__ == "__main__":
    main()
