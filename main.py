""" COSC428 Project - Billiards Trainer.

The objective of this program is to enable a pool player to predict
exactly where his or her shots are going to go before making them.
The program when run will identify the billiards table, the balls on the table,
and the direction of the cue. From this information the trajectory of the white
ball will be calculated and displayed along with any balls that are potentially
contacted by the white ball when hit.
"""

import cv2

from Common.Utilities import Utilities, ListTooShortException
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

    reference_frame = camera.get_frame()
    while True:
        frame = camera.get_frame()
        display_frame = frame.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) & 0xFF == ord('r'):
            recording = not recording

        if not are_balls_moving(frame, reference_frame):
            table_bounds = find_table(reference_frame)
            cushions = find_table_cushions(reference_frame, table_bounds)

            # Identify the locations of all balls.
            balls = hough_circles.get_circles(frame)

            cue_direction, cue_ball, balls = find_cue_direction(frame, reference_frame, balls[0, :])

            # # Draw each ball
            # if balls is not None:
            #     for i in balls[0, :]:
            #         # Draw the outer circle
            #         cv2.circle(display_frame, (i[0], i[1]), i[2], (0, 255, 0), cv2.FILLED)
            #         # Draw the center of the circle
            #         cv2.circle(display_frame, (i[0], i[1]), 2, (0, 0, 255), 3)
            #     # Draw lines between each ball
            #     try:
            #         Utilities.draw_ball_path(display_frame, balls[0, :])
            #     except ListTooShortException:
            #         print("Not enough circles")

            lines = []
            # Recursive function to find collisions
            find_collisions(cue_ball, cue_direction, balls[0, :], cushions, table_bounds, lines, 0)
            # draw paths

        else:
            reference_frame = frame

        if recording:
            video_recorder.write_frame(display_frame)

        window.update_window(display_frame)

    video_recorder.release()
    camera.release()
    window.destroy()
    hough_circles.destroy()


def are_balls_moving(frame, reference_frame) -> bool:
    pass


def find_cue_direction(frame, reference_frame, balls) -> ((float, float), (int, int, int), list):
    # Perform image diff
    # enhance edges
    # look for edges
    # look for lines from edges
    # look for two almost parallel lines going through the nearest ball
    # Save this ball as the cue ball and remove it from balls
    # Calculate center line of these two lines
    # Find end closest to ball
    # normalize this for cue direction
    # return (cue_direction, cue_ball, balls)
    pass


def find_table(reference_frame) -> list:
    pass


def find_table_cushions(reference_frame, table) -> list:
    pass


def find_collisions(start_ball, direction, balls_left, cushions, table_bounds, lines, recursion_counter):
    if recursion_counter > 2:
      return
    # loop through balls and cushions finding the nearest collision (contains ball or cushion collided with, balls minus the collided ball, position of start_ball at collision
    # if no collisions:
    #   add line to exit point of table bounds
    #   return
    # else:
    #   increment counter by 1
    #   add collision line to lines
    #   if collided with ball:
    #       calculate collided_ball direction
    #       use this to calculate start_ball new direction
    #       recursively call this function for collided ball
    #       recursively call this function for new position of start ball
    #   else:
    #       calculate start_ball new direction
    #       recursively call this function for new direction at collision point
    pass

if __name__ == "__main__":
    main()
