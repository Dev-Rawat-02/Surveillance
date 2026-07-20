# Drone Surveillance System

A real-time computer vision surveillance app that uses a YOLOv8 model to detect threats from a live camera feed, draw detections on screen, trigger an audio alert, and save snapshots plus alert history to SQLite.

## Features

- Real-time camera capture with FPS display
- YOLOv8-based object detection using `yolov8n.pt`
- Threat filtering for `person`, `car`, `truck`, and `motorcycle`
- Snapshot saving when a threat is detected
- Audio alarm playback on detection
- Local SQLite logging of alerts

## Tech Stack

- Python
- OpenCV
- Ultralytics YOLOv8
- Pygame
- SQLite

## Project Structure

```text
app.py               # Main application loop
config.py            # Project configuration
core/
	camera.py          # Camera handling and FPS calculation
	alert.py           # Snapshot, sound, and database alert processing
	database.py        # SQLite alert storage
	threat.py          # Threat filtering logic
	visualizer.py      # Bounding box and FPS rendering
model/
	detector.py        # YOLO model wrapper
sound/
	alert.wav          # Alarm sound
snapshots/           # Saved threat snapshots
database/            # SQLite database file location
```

## Requirements

Install the dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the requirements.
4. Make sure your camera is connected and available.
5. Confirm `sound/alert.wav` and `yolov8n.pt` are present in the project root.

## Run

```bash
python app.py
```

Press `q` to close the video window.

## What Happens When a Threat Is Detected

- The app highlights the detected object on the video feed.
- A snapshot is saved in `snapshots/`.
- An alert row is written to `database/surveillance.db`.
- The alarm sound plays through the configured audio device.

## Notes

- The app expects a working webcam or another camera source configured in `core/camera.py`.
- If you change the camera source, update the `Camera` class in `core/camera.py`.
- `database/surveillance.db` is created automatically the first time the app runs.
