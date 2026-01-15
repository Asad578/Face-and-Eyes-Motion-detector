import cv2

def draw_text(frame, text, y):
    cv2.putText(frame, text, (30, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                (0, 255, 255), 2)
