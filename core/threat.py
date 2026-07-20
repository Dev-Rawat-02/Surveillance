class ThreatEngine:

    def __init__(self):

        self.threat_classes = {
            "person",
            "car",
            "truck",
            "motorcycle"
        }
    def analyze(self, results):
        threats = []
        for box in results[0].boxes:

            class_id = int(box.cls[0])
            class_name = results[0].names[class_id]
            confidence = float(box.conf[0])
            if confidence < 0.5:
                continue
            confidence = f"{confidence:.2f}"
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if class_name in self.threat_classes:

                threats.append({
                    "label": class_name,
                    "confidence": confidence,
                    "box": (x1, y1, x2, y2)
                })
        return threats