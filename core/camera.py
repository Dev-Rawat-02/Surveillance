import cv2
import time

class Camera:
    def __init__(self, source = 0):
        self.prev_time = time.time()
        self.source = source
        self.cap = None
    
    def open(self):
        self.cap = cv2.VideoCapture(self.source)
        
        if not self.cap.isOpened():
            return RuntimeError("Camera not Found")
        
    def read(self):
        success , frame = self.cap.read()

        if not success :
            return None
        return frame
    
    def release(self):
        if self.cap:
            self.cap.release()

    def fps(self):
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = time.time()
        return round(fps, 2)