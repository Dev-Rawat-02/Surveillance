"""import cv2
from model.detector import Detector

frame = cv2.imread('1353238.jpeg')
if frame is None:
    print("Image not found")
else:
    detector = Detector()
    results = detector.detect(frame)
    result = results[0]
    print(results[0].boxes)"""
import pygame
pygame.mixer.init()
pygame.mixer.music.load('sound/alert.wav')
pygame.mixer.music.play(-1)
pygame.time.wait(2000)