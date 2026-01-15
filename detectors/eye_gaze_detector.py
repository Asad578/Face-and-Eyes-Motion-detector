import cv2
import numpy as np
from config.settings import EYE_MOVEMENT_THRESHOLD

def is_eye_movement_suspicious(frame):
    """
    Detects if eyes are looking away from the screen.
    Uses simple eye detection based on face region analysis.
    Returns True if gaze direction is suspicious (looking away).
    """
    # Load face and eye cascade classifiers
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_eye.xml"
    )
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) == 0:
        return False
    
    # Get the first (largest) face
    face = faces[0]
    x, y, w, h = face
    roi_gray = gray[y:y+h, x:x+w]
    
    # Detect eyes within face region
    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4)
    
    if len(eyes) < 2:
        # Not enough eyes detected, assume normal gaze
        return False
    
    # Sort eyes by x position (left to right)
    eyes = sorted(eyes, key=lambda e: e[0])
    left_eye = eyes[0]
    right_eye = eyes[1]
    
    # Check if eyes are roughly centered in their regions
    # If eyes are too far to one side, they might be looking away
    eye_x_positions = [left_eye[0] + left_eye[2]/2, right_eye[0] + right_eye[2]/2]
    
    # Normalize positions within face ROI
    left_eye_center_ratio = (left_eye[0] + left_eye[2]/2) / w
    right_eye_center_ratio = (right_eye[0] + right_eye[2]/2) / w
    
    # Eyes should be roughly centered (between 0.25 and 0.75 of face width)
    # If ratio is too extreme, eyes are looking to the side
    left_eye_suspicious = left_eye_center_ratio < 0.2 or left_eye_center_ratio > 0.8
    right_eye_suspicious = right_eye_center_ratio < 0.2 or right_eye_center_ratio > 0.8
    
    # Eyes looking away if both are extreme or significantly off-center
    return left_eye_suspicious or right_eye_suspicious
