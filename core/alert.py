import time
import pygame
import os
from datetime import datetime
from core.database import DatabaseManager
import cv2

class Aleart():
    def __init__(self):
        self.snapshot_dir = "snapshots"
        os.makedirs(self.snapshot_dir, exist_ok=True)
        pygame.mixer.init()
        self.alarm = pygame.mixer.Sound("sound/alert.wav")
        self.cooldown = 5
        self.last_alert = 0
        self.database = DatabaseManager()

    def process(self, threat, frame):
        if not threat:
            return
        current_time = time.time()
        if current_time - self.last_alert < self.cooldown:
            return
        snapshot_path = self.save_snapshot(frame)
        for thret in threat:
             self.database.save_alert(
                  timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  label=thret["label"],
                  confidence=thret["confidence"],
                  snapshot=snapshot_path)
             
        print("THREAT DETECTED")
        snapshot_path = self.save_snapshot(frame)
        self.alarm.play()
        self.last_alert = current_time
    
    def save_snapshot(self, frame):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.jpg" 
        filepath = os.path.join(self.snapshot_dir, filename) 
        cv2.imwrite(filepath, frame) 
        print(f"Snapshot saved: {filepath}") 
        return filepath
    def save_alert( self, timestamp, label, confidence, snapshot):
        self.cursor.execute(
            """ INSERT INTO alerts (timestamp,label,confidence,snapshot) VALUES (?,?,?,?) """,
            (
            timestamp,
            label,
            confidence,
            snapshot)
            )
        self.connection.commit()