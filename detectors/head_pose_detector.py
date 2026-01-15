import cv2

def is_head_straight(frame):
    """
    Checks if head is approximately straight to the camera.
    Uses face detection bounding box to estimate head orientation.
    Returns True if head is straight, False otherwise, None if no face detected.
    """
    # Load face cascade classifier
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) == 0:
        return None
    
    # Check if face is roughly centered in the frame (indicating straight head)
    face = faces[0]  # Get first face
    x, y, w, h = face
    
    frame_height, frame_width = frame.shape[:2]
    face_center_x = x + w / 2
    frame_center_x = frame_width / 2
    
    # Calculate horizontal deviation from center (normalized)
    deviation = abs(face_center_x - frame_center_x) / frame_width
    
    # Head is considered straight if deviation < 0.15 (15% of frame width)
    return deviation < 0.15

