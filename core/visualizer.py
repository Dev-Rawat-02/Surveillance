import cv2

class Visualizer:
   def draw(self, frame, threats, fps):
    for threat in threats:
            x1, y1, x2, y2 = threat["box"]
            label = f"{threat['label']} {threat['confidence']}"
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 0),
                2
            )
            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 0),
                2
            )
            cv2.putText(
                frame,
                f"FPS : {fps}",(20,70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,0),
                2
            )

    return frame