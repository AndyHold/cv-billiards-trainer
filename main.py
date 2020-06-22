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
# from Models.VideoRecorder import VideoRecorder
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

    window = Window("Show me the way")
    # video_recorder = VideoRecorder("output.avi", (640, 480))
    hough_circles = HoughCircles(50, 6, 27, 32)
    recording = False

    reference_frame = frame_capture.get_frame()
    frame = frame_capture.get_frame()
    while frame is not None:
        display_frame = frame.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(1) & 0xFF == ord('r'):
            recording = not recording

        if not are_balls_moving(frame, reference_frame, hough_circles):
            cushions = find_table(reference_frame)

            balls = find_balls(frame)

            avg_cue_line = find_cue(frame, reference_frame, display_frame)

            if avg_cue_line is not None:
                # look in both directions, find nearest collision. get direction
                # from cue line and closest ball is starting ball.
                collision_distance = 1.e+6  # further away than any ball
                ball_index = -1
                collision_direction = None
                direction = Utilities.normalize((avg_cue_line[0] - avg_cue_line[2], avg_cue_line[1] - avg_cue_line[3]))
                for i in range(len(balls)):
                    t, _ = balls[i].intersect((avg_cue_line[0], avg_cue_line[1]), direction, 0.0)
                    if t > 0:  # there is a collision
                        if t < collision_distance:
                            collision_distance = t
                            ball_index = i
                            collision_direction = direction

                direction = Utilities.normalize((avg_cue_line[2] - avg_cue_line[0], avg_cue_line[3] - avg_cue_line[1]))

                for i in range(len(balls)):
                    t, _ = balls[i].intersect((avg_cue_line[2], avg_cue_line[3]), direction, 0.0)
                    if t > 0:  # there is a collision
                        if t < collision_distance:
                            collision_distance = t
                            ball_index = i
                            collision_direction = direction

                if ball_index is not -1:
                    cue_ball = balls.pop(ball_index)
                    # Uncomment to display the cue ball
                    # cv2.circle(display_frame,
                    #            (int(round(cue_ball.position[0])),
                    #             int(round(cue_ball.position[1]))),
                    #            int(round(cue_ball.radius)),
                    #            (100, 255, 100),
                    #            2)

                    # Uncomment to show imaginary lines next to cushions
                    if cushions is not None:
                        for cushion in cushions:
                            imaginary_line = cushion.get_imaginary_line(cue_ball.radius)
                            cv2.line(display_frame,
                                     (int(round(imaginary_line[0])), int(round(imaginary_line[1]))),
                                     (int(round(imaginary_line[2])), int(round(imaginary_line[3]))),
                                     (255, 255, 100),
                                     thickness=2)
                    lines = []
                    find_collisions(cue_ball, collision_direction, balls + cushions, lines, 0, display_frame, True)
                    Utilities.draw_lines(lines, display_frame)

        else:
            reference_frame = frame

        # if recording:
        #     video_recorder.write_frame(display_frame)

        window.update_window(display_frame)

        frame = frame_capture.get_frame()

    # video_recorder.release()
    frame_capture.release()
    window.destroy()
    hough_circles.destroy()


def filter_outlyers(lines):
    data = []
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i is not j:
                if Utilities.shortest_distance_two_lines(lines[i], lines[j]) < 50:
                    data.append(lines[i])
                    break

    return data


def are_balls_moving(frame, reference_frame,
                     hough_circles) -> bool:  # , display_frame, display_reference_frame) -> bool:
    reference_balls = hough_circles.get_balls(reference_frame)
    frame_balls = hough_circles.get_balls(frame)

    if reference_balls is not None and frame_balls is not None:
        for i in range(len(reference_balls)):
            ball_found = False
            for j in range(len(frame_balls)):
                if abs(reference_balls[i].position[0] - frame_balls[j].position[0]) < 5 and \
                        abs(reference_balls[i].position[1] - frame_balls[j].position[1] < 5):
                    ball_found = True
                    break
            if not ball_found:
                return False
    else:
        return True
    return False


def find_cue(frame, reference_frame, display_frame) -> (float, float, float, float):
    diff = cv2.subtract(frame, reference_frame)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)

    _, binary = cv2.threshold(blur, 75, 255, cv2.THRESH_BINARY)
    morphed = Morphology.close_morph(binary)

    hough_lines = HoughLines(110, 20)
    line_set, edges = hough_lines.get_lines(morphed)

    lines = []
    if line_set is not None:
        if len(line_set) > 2:
            # Split the lines
            for line in line_set:
                for x1, y1, x2, y2 in line:
                    i = 0
                    found = False
                    while not found and i < len(lines):
                        if Utilities.shortest_distance_two_lines(lines[i][0], (x1, y1, x2, y2)) < 10:
                            lines[i].append((x1, y1, x2, y2))
                            found = True
                        i += 1
                    if not found:
                        lines.append([(x1, y1, x2, y2)])

            avg_lines = []

            for i in range(len(lines)):
                avg_lines.append(Utilities.calculate_line_average(lines[i]))

            # Filter Outliers
            new_avg_lines = filter_outlyers(avg_lines)

            if len(new_avg_lines) == 2:
                avg_line = Utilities.calculate_line_average(new_avg_lines)

                # Uncomment to show cue line
                # cv2.line(display_frame,
                #          (int(round(avg_line[0])), int(round(avg_line[1]))),
                #          (int(round(avg_line[2])), int(round(avg_line[3]))),
                #          (255, 100, 100),
                #          thickness=2)

                return avg_line
    return None


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
    lines, _ = hough_lines.get_lines(open_closed)

    lines = lines if lines is not None else []

    return find_table_cushions(lines, width / 2.0, height / 2.0)


def find_table_cushions(lines, width_halfway, height_halfway) -> list:
    left_lines = []
    right_lines = []
    top_lines = []
    bottom_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            gradient = 1000000 if (x2 - x1) == 0 else float(y2 - y1) / float(x2 - x1)  # Added catch for vertical lines
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


def find_collisions(start_ball, direction, obstacles, lines, recursion_counter, display_frame, is_cue_ball):
    if recursion_counter > 3:
        return

    collision_point = None
    index = None
    collision_distance = 1.e+6
    intersection_point = None
    for i in range(len(obstacles)):
        t, intersection_pt = obstacles[i].intersect(start_ball.position, direction, start_ball.radius)
        if t > 0:
            # Object is intersected
            point = (
                start_ball.position[0] + direction[0] * t,
                start_ball.position[1] + direction[1] * t
            )
            if t < collision_distance:
                index = i
                collision_point = point
                collision_distance = t
                intersection_point = intersection_pt

    recursion_counter += 1
    if index is not None:
        lines.append(list(start_ball.position) + list(collision_point))

        if obstacles[index].get_type() == "Ball":
            collision_ball = obstacles.pop(index)
            vector_diff = [
                collision_ball.position[0] - collision_point[0],
                collision_ball.position[1] - collision_point[1]
            ]
            collided_ball_direction = Utilities.normalize(vector_diff)
            collision_vector = (collision_distance * direction[0], collision_distance * direction[1])
            imaginary_ball = Ball([
                start_ball.position[0] + collision_vector[0],
                start_ball.position[1] + collision_vector[1],
                start_ball.radius
            ])
            imaginary_ball_new_direction = Utilities.find_perpendicular_vector(
                collided_ball_direction,
                list(start_ball.position) + list(collision_point),
                collision_ball.position
            )

            cv2.circle(display_frame,
                       (int(round(collision_point[0])),
                        int(round(collision_point[1]))),
                       int(round(start_ball.radius)),
                       (100, 255, 100), 2)

            find_collisions(collision_ball,
                            collided_ball_direction,
                            obstacles,
                            lines,
                            recursion_counter, display_frame, False)

            if not is_cue_ball:
                find_collisions(imaginary_ball,
                                imaginary_ball_new_direction,
                                obstacles,
                                lines,
                                recursion_counter, display_frame, False)
        else:
            collision_cushion = obstacles[index]
            if intersection_point is not None:
                cv2.circle(display_frame,
                           (int(round(intersection_point[0])), int(round(intersection_point[1]))),
                           28,
                           (0, 0, 0),
                           thickness=2)
            normal = collision_cushion.normal(collision_point)
            new_direction = Utilities.normalize(
                Utilities.find_reflection(normal, direction)
            )

            find_collisions(Ball(list(collision_point) + [start_ball.radius]),
                            new_direction,
                            obstacles,
                            lines,
                            recursion_counter,
                            display_frame,
                            is_cue_ball)

    else:
        height, width, _ = display_frame.shape
        start = start_ball.position
        end = Utilities.find_bounds_exit_point(height, width, start, direction)
        lines.append(list(start) + list(end))


if __name__ == "__main__":
    main()
