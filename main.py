""" COSC428 Project - Billiards Trainer.

The objective of this program is to enable a pool player to predict
exactly where his or her shots are going to go before making them.
The program when run will identify the billiards table, the balls on the table,
and the direction of the cue. From this information the trajectory of the white
ball will be calculated and displayed along with any balls that are potentially
contacted by the white ball when hit.
"""
import sys
import cv2

from Common.Utilities import Utilities
from Models.Obstacles.Ball import Ball
from Models.Filters.ColourSpaceConverter import ColourSpaceConverter
from Models.Filters.MiddleSectionCropper import MiddleSectionCropper
from Models.Filters.Morphology import Morphology
from Models.FrameCapture.Camera import Camera
from Models.Obstacles.Cushion import Cushion
from Models.Transformations.HoughCircles import HoughCircles
from Models.FrameCapture.VideoReader import VideoReader
from Models.Transformations.HoughLines import HoughLines
from Models.VideoRecorder import VideoRecorder
from Models.Window import Window


def main():
    args = sys.argv[1:]

    tag = None if len(args) == 0 else args[0]
    try:
        if tag is not None:
            arg = args[1]
        if tag == '-f':
            frame_capture = VideoReader(arg)
        elif tag == '-v':
            frame_capture = Camera(int(arg))
        else:
            frame_capture = Camera(-1)
    except IndexError:
        if tag == '-f':
            missing = 'filename'
        else:
            missing = 'camera number'
        print(f"Missing argument '{missing}'")
        sys.exit(1)

    if not frame_capture.is_opened():
        print("Failed to open frame capture device or file.")
        sys.exit(1)

    window = Window("Show me the camera")
    video_recorder = VideoRecorder("output.avi", (640, 480))
    hough_circles = HoughCircles(20, 25, 20, 30)
    recording = False

    reference_frame = frame_capture.get_frame()
    while frame_capture.is_frame_valid():
        frame = frame_capture.get_frame()
        display_frame = frame.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) & 0xFF == ord('r'):
            recording = not recording

        if not are_balls_moving(frame, reference_frame, hough_circles):
            cushions = find_table(reference_frame)

            # TODO: delete this, for debugging
            for cushion in cushions:
                cv2.line(display_frame,
                         (int(round(cushion.start[0])), int(round(cushion.start[1]))),
                         (int(round(cushion.end[0])), int(round(cushion.end[1]))), (255, 255, 100), thickness=2)

            # # Identify the locations of all balls.
            balls = find_balls(frame)

            # TODO: delete this, for debugging
            for ball in balls:
                cv2.circle(display_frame, ball.position, ball.radius, (100, 255, 100), 2)

            # cue_direction, cue_ball, balls = find_cue_direction(frame, reference_frame, balls)

            # lines = []
            # # Recursive function to find collisions
            # find_collisions(Ball(cue_ball), cue_direction, balls[0, :] + cushions, table_bounds, lines, 0)
            # # draw lines
            # Utilities.draw_lines()

        else:
            reference_frame = frame

        # if recording:
        #     video_recorder.write_frame(display_frame)

        window.update_window(display_frame)

    video_recorder.release()
    frame_capture.release()
    window.destroy()
    hough_circles.destroy()


def are_balls_moving(frame, reference_frame, hough_circles) -> bool: # , display_frame, display_reference_frame) -> bool:

    reference_balls = hough_circles.get_circles(reference_frame)
    frame_balls = hough_circles.get_circles(frame)

    if reference_balls is not None and frame_balls is not None:
        for i in range(len(reference_balls[0])):
            ball_found = False
            for j in range(len(frame_balls[0])):
                # print(reference_balls[i], frame_balls[j])
                if abs(reference_balls[0][i][0] - frame_balls[0][j][0]) < 5 and abs(
                        reference_balls[0][i][1] - frame_balls[0][j][1] < 5):
                    ball_found = True
                    break

            if not ball_found:
                return False
    else:
        return True
    return True


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


def find_table(frame) -> list:
    height, width, _ = frame.shape
    frame_max_hue = MiddleSectionCropper.max_hue_index(frame)
    hsv_filtered = ColourSpaceConverter.get_hsv_filtered(
        frame,
        frame_max_hue,
        positive_threshold=7,
        negative_threshold=7)

    open_closed = Morphology.open_close(hsv_filtered)
    hough_lines = HoughLines(150, 150)
    lines = hough_lines.get_lines(open_closed)

    lines = lines if lines is not None else []

    return find_table_cushions(lines, width / 2, height / 2)


def find_table_cushions(lines, width_halfway, height_halfway) -> list:
    left_lines = []
    right_lines = []
    top_lines = []
    bottom_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            gradient = 1000000 if (x2 - x1) == 0 else float(y2 - y1) / float(x2 - x1)  # Added catch for vertical lines
            print(gradient)
            if abs(gradient) < 1:
                if y1 > height_halfway:
                    bottom_lines.append(line)
                else:
                    top_lines.append(line)
            elif x1 < width_halfway:
                left_lines.append(line)
            else:
                right_lines.append(line)

    # return bottom_lines
    cushions = []
    if len(top_lines) > 0:
        cushions.append(Cushion(Utilities.add_horizontal_lines(top_lines), "top"))
    if len(bottom_lines) > 0:
        cushions.append(Cushion(Utilities.add_horizontal_lines(bottom_lines), "bottom"))
    if len(left_lines) > 0:
        cushions.append(Cushion(Utilities.calculate_line_average(left_lines), "left"))
    if len(right_lines) > 0:
        cushions.append(Cushion(Utilities.calculate_line_average(right_lines), "right"))

    return cushions


def find_balls(frame):
    hough_circles = HoughCircles(50, 6, 27, 32)

    return hough_circles.get_balls(frame)


def find_collisions(start_ball, direction, obstacles, table_bounds, lines, recursion_counter):
    if recursion_counter > 2:
        return

    minimum = 1.e+6
    collision_point = None
    index = None
    collision_distance = 0.0
    for i in range(len(obstacles)):
        t = obstacles[i].intersect(start_ball.position, direction, start_ball.radius)
        if t > 0:
            # Object is intersected
            point = (start_ball.position[0] + direction[0] * t, start_ball.position[1] + direction[1] * t)
            if (t < minimum):
                minimum = t
                index = i
                collision_point = point
                collision_distance = t

    if index is not None:
        recursion_counter += 1
        lines.append(start_ball.position + collision_point)

        #       increment counter by 1
        if obstacles[index].get_type() == "Ball":
            collision_ball = obstacles.pop(index)
            vector_diff = (
                collision_ball.position[0] - collision_point[0], collision_ball.position[1] - collision_point[1])
            collided_ball_direction = Utilities.normalize(vector_diff)
            collision_vector = (collision_distance * direction[0], collision_distance * direction[1])
            start_ball_new_direction = Utilities.normalize((collision_vector[0] - vector_diff[0],
                                                            collision_vector[1] - vector_diff[1]))

            find_collisions(collision_ball,
                            collided_ball_direction,
                            obstacles,
                            table_bounds,
                            lines,
                            recursion_counter)

            find_collisions(Ball(list(collision_point) + [start_ball.radius]),
                            start_ball_new_direction,
                            obstacles,
                            table_bounds,
                            lines,
                            recursion_counter)
        else:
            # Reflect along normal line
            #           calculate start_ball new direction
            #           recursively call this function for new direction at collision point
            pass

    else:
        #   add line to exit point of table bounds using direction
        #   return
        pass


if __name__ == "__main__":
    main()
