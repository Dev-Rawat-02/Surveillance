import cv2 
from core.camera import Camera
from model.detector import Detector
from core.visualizer import Visualizer
from core.threat import ThreatEngine
from core.alert import Aleart


camera = Camera()
detector = Detector()
camera.open()
visualizer = Visualizer()
alert = Aleart()
threat = ThreatEngine()

while True :
    fps = camera.fps()
    frame = camera.read()
    results = detector.detect(frame)
    threats = threat.analyze(results)
    frame = visualizer.draw(frame, threats, fps)
    alert.process(threats, frame)

    if frame is None :
        break

    cv2.imshow("Surveilance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()