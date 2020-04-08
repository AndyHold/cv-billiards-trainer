import cv2


class VideoRecorder:

    def __init__(self, filename, dimensions):
        self.filename = filename
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter(filename, fourcc, 20.0, dimensions)

    def write_frame(self, frame):
        self.out.write(frame)

    def release(self):
        self.out.release()
