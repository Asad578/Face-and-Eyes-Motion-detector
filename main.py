import cv2
import time

from camera.camera_manager import CameraManager
from camera.camera_stream import CameraStream
from detectors.face_detector import detect_faces
from detectors.head_pose_detector import is_head_straight
from detectors.eye_gaze_detector import is_eye_movement_suspicious
from validators.face_distance import is_face_distance_valid
from violations.violation_manager import ViolationManager
from violations import violation_types as vt
from timers.countdown_timer import CountdownTimer
from utils.drawing import draw_text
from config.settings import *

def main():
    camera = CameraManager()
    stream = CameraStream(camera)
    violations = ViolationManager()

    test_timer = CountdownTimer(TEST_DURATION_SECONDS)
    test_start_time = time.time()
    
    # Face alignment timer (5 sec) - face must be straight and at proper distance
    face_alignment_timer = None
    face_aligned = False
    
    # Grace timers for different violation types
    no_face_timer = None
    face_distance_timer = None
    head_movement_timer = None
    eye_movement_timer = None

    print("Test started")

    for frame in stream.frames():

        if test_timer.expired():
            print("Test time limit reached")
            break

        faces = detect_faces(frame)

        # Check for no face detection
        if len(faces) == 0:
            if no_face_timer is None:
                no_face_timer = CountdownTimer(NO_FACE_GRACE_PERIOD)
            if no_face_timer.expired():
                if not violations.register(vt.NO_FACE):
                    break
            face_aligned = False
            face_alignment_timer = None
        else:
            no_face_timer = None

        # Check for multiple faces
        if len(faces) > 1:
            if not violations.register(vt.MULTIPLE_FACES):
                break
            face_aligned = False
            face_alignment_timer = None

        # Process single face
        if len(faces) == 1:
            face = faces[0]
            head_straight = is_head_straight(frame)
            
            # Check face distance (too close or too far)
            if not is_face_distance_valid(face, frame.shape):
                if face_distance_timer is None:
                    face_distance_timer = CountdownTimer(VIOLATION_GRACE_PERIOD)
                if face_distance_timer.expired():
                    if not violations.register(vt.FACE_DISTANCE):
                        break
                face_aligned = False
                face_alignment_timer = None
            else:
                face_distance_timer = None

                # Check head movement (only if head straight check returns a value)
                if head_straight is not None and not head_straight:
                    if head_movement_timer is None:
                        head_movement_timer = CountdownTimer(VIOLATION_GRACE_PERIOD)
                    if head_movement_timer.expired():
                        if not violations.register(vt.HEAD_MOVEMENT):
                            break
                    face_aligned = False
                    face_alignment_timer = None
                else:
                    head_movement_timer = None

                    # If face distance is valid and head is straight, start alignment timer
                    if head_straight is True:
                        if face_alignment_timer is None:
                            face_alignment_timer = CountdownTimer(FACE_ALIGNMENT_GRACE_PERIOD)
                            print("Face aligned - waiting 5 seconds to stabilize...")
                        
                        if face_alignment_timer.expired():
                            face_aligned = True
                    else:
                        face_aligned = False
                        face_alignment_timer = None

                    # Check eye movement (only when face is properly aligned)
                    if face_aligned and is_eye_movement_suspicious(frame):
                        if eye_movement_timer is None:
                            eye_movement_timer = CountdownTimer(VIOLATION_GRACE_PERIOD)
                        if eye_movement_timer.expired():
                            if not violations.register(vt.EYE_MOVEMENT):
                                break
                    else:
                        eye_movement_timer = None

        elapsed_time = time.time() - test_start_time
        time_left = max(0, TEST_DURATION_SECONDS - elapsed_time)
        
        draw_text(frame, f"Time Left: {int(time_left)}s", 40)
        draw_text(frame, f"Violations: {violations.attempts}/{MAX_VIOLATIONS}", 80)
        
        if face_alignment_timer is not None and not face_aligned:
            alignment_time_left = max(0, FACE_ALIGNMENT_GRACE_PERIOD - (time.time() - face_alignment_timer.start_time))
            draw_text(frame, f"Align face: {int(alignment_time_left)}s", 120)

        cv2.imshow("Online Test Proctoring", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()

    print("\nTest Ended")
    print(f"Total violations: {violations.attempts}")
    print("Violation Details:")
    for v in violations.records:
        print(f"  - {v}")

if __name__ == "__main__":
    main()
