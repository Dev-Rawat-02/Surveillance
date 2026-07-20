import sys

import cv2 
from core.camera import Camera
from model.detector import Detector
from core.visualizer import Visualizer
from core.threat import ThreatEngine
from core.alert import Aleart


def run_surveillance():
    camera = Camera()
    detector = Detector()
    camera.open()
    visualizer = Visualizer()
    alert = Aleart()
    threat = ThreatEngine()

    while True:
        fps = camera.fps()
        frame = camera.read()

        if frame is None:
            break

        results = detector.detect(frame)
        threats = threat.analyze(results)
        frame = visualizer.draw(frame, threats, fps)
        alert.process(threats, frame)

        cv2.imshow("Surveilance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if "--dashboard" in sys.argv:
        from core.dashboard import launch_dashboard

        launch_dashboard()
    elif "--run" in sys.argv:
        run_surveillance()
    else:
        from core.ui import launch_ui

        launch_ui()