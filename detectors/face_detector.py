import cv2
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
cascade_path = os.path.join(current_dir, "haarcascade_frontalface_default.xml")
FACE_CASCADE = cv2.CascadeClassifier(cascade_path)

if FACE_CASCADE.empty():
    print("ERROR: Cascade file not loaded properly!")


def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=3,
    minSize=(30, 30)
    )
    return faces