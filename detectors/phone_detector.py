import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
try:
    model = YOLO('yolov8n.pt')  # nano model for speed
except Exception as e:
    print(f"Warning: Could not load YOLO model: {e}")
    model = None

def detect_phone(frame):
    """
    Detects mobile phone using YOLOv8.
    Returns True if phone is detected in the frame.
    """
    if model is None:
        return False
    
    try:
        # Run inference
        results = model(frame, conf=0.5, verbose=False)
        
        if results and len(results) > 0:
            # Class 67 is "cell phone" in COCO dataset
            # Class 77 is "laptop" 
            # We're looking for class 67 (cell phone)
            detections = results[0]
            if detections.boxes is not None:
                for box in detections.boxes:
                    class_id = int(box.cls[0])
                    # 67 = cell phone in COCO
                    if class_id == 67:
                        return True
        
        return False
    except Exception as e:
        print(f"Error in phone detection: {e}")
        return False
