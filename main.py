import cv2
import time
import mediapipe as mp
from camera.camera_manager import CameraManager
from camera.camera_stream import CameraStream
from detectors.face_detector import detect_faces
from detectors.head_pose_detector import is_head_straight
from validators.face_alignment import is_face_aligned
from detectors.eye_gaze_detector import is_eye_movement_suspicious
from validators.face_distance import is_face_distance_valid
from violations.violation_manager import ViolationManager
from violations import violation_types as vt
from timers.countdown_timer import CountdownTimer
from utils.drawing import draw_text, draw_face_mesh
from detectors.face_mesh_service import FaceMeshService
from config.settings import *
from config.settings import VIOLATION_GRACE_PERIOD

def main():
    camera = CameraManager()
    stream = CameraStream(camera)
    violations = ViolationManager()
    face_mesh = FaceMeshService.get()

    test_timer = CountdownTimer(TEST_DURATION_SECONDS)
    test_start_time = time.time()
    
    # Face alignment timer (5 sec) - face must be straight and at proper distance
    face_alignment_timer = None
    face_aligned = False
    
    # Grace timers for different violation types
    no_face_timer = None
    multiple_faces_timer = None
    face_distance_timer = None
    head_movement_timer = None
    eye_movement_timer = None
    violation_grace_timer = None  # Global grace period after ANY violation

    print("Test started")

    for frame in stream.frames():

        if test_timer.expired():
            print("Test time limit reached")
            break

        faces = detect_faces(frame)

        # Check for no face detection
        if len(faces) == 0:
            # No face detected - wait 1.5 seconds before counting as violation
            if no_face_timer is None:
                # Start 1.5-second timer before counting violation
                no_face_timer = CountdownTimer(1.5)
            elif no_face_timer.expired():
                # 1.5 seconds passed without face - count violation and start grace period
                if not violations.register(vt.NO_FACE):
                    # Max violations exceeded - stop test
                    print("Max violations reached - test stopped")
                    break
                # Start 3-second grace timer to detect face
                no_face_timer = CountdownTimer(NO_FACE_GRACE_PERIOD)
                print(f"No face detected - violation counted. Waiting {NO_FACE_GRACE_PERIOD}s for face...")
            face_aligned = False
            face_alignment_timer = None
            # Skip all other checks when no face is detected
            cv2.imshow("Online Test Proctoring", frame)
            elapsed_time = time.time() - test_start_time
            time_left = max(0, TEST_DURATION_SECONDS - elapsed_time)
            draw_text(frame, f"Time Left: {int(time_left)}s", 40)
            draw_text(frame, f"Violations: {violations.attempts}/{MAX_VIOLATIONS}", 80)
            cv2.imshow("Online Test Proctoring", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue
        else:
            # Face detected - reset grace period timer
            if no_face_timer is not None:
                print("Face detected - timer reset")
            no_face_timer = None

        # Check for multiple faces
        if len(faces) > 1:
            # Multiple faces detected - wait 1.5 seconds before counting as violation
            if multiple_faces_timer is None:
                # Start 1.5-second timer before counting violation
                multiple_faces_timer = CountdownTimer(1)
            elif multiple_faces_timer.expired():
                # 1.5 seconds passed with multiple faces - count violation and start grace period
                if not violations.register(vt.MULTIPLE_FACES):
                    # Max violations exceeded - stop test
                    print("Max violations reached - test stopped")
                    break
                # Start 3-second grace timer for faces to go back to 1
                multiple_faces_timer = CountdownTimer(NO_FACE_GRACE_PERIOD)
                print(f"Multiple faces detected - violation counted. Waiting {NO_FACE_GRACE_PERIOD}s...")
            face_aligned = False
            face_alignment_timer = None
            # Skip all other checks when multiple faces detected
            cv2.imshow("Online Test Proctoring", frame)
            elapsed_time = time.time() - test_start_time
            time_left = max(0, TEST_DURATION_SECONDS - elapsed_time)
            draw_text(frame, f"Time Left: {int(time_left)}s", 40)
            draw_text(frame, f"Violations: {violations.attempts}/{MAX_VIOLATIONS}", 80)
            cv2.imshow("Online Test Proctoring", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            continue
        else:
            # Face count is 1 - reset multiple faces timer
            if multiple_faces_timer is not None:
                print("Multiple faces resolved - timer reset")
            multiple_faces_timer = None

        # Process single face
        if len(faces) == 1:
            # ---- Face mesh detection (MUST happen first) ----
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            face_landmarks_result = face_mesh.detect(mp_image)

            if not face_landmarks_result.face_landmarks:
                face_aligned = False
                head_movement_timer = None
                eye_movement_timer = None
                continue

            face_landmarks = face_landmarks_result.face_landmarks[0]

            face = faces[0]
            
            # Check face distance (too close or too far)
            if not is_face_distance_valid(face, frame.shape):
                # Distance invalid (too close or too far)
                if face_distance_timer is None:
                    # Start 1-second timer before counting violation
                    face_distance_timer = CountdownTimer(1)

                elif face_distance_timer.expired():
                    # Invalid distance persisted for 1 second → violation
                    if not violations.register(vt.FACE_DISTANCE):
                        print("Max violations reached - test stopped")
                        break

                    # Start grace period after violation
                    violation_grace_timer = CountdownTimer(VIOLATION_GRACE_PERIOD)
                    # Reset timer after counting violation
                    face_distance_timer = None
                    print("Face distance violation counted")
                face_aligned = False
                face_alignment_timer = None
            else:
                # Distance back to valid → reset timer
                if face_distance_timer is not None:
                    print("Face distance valid - timer reset")
                face_distance_timer = None

                # Check if we're in violation grace period (skip other violation checks)
                if violation_grace_timer is not None and not violation_grace_timer.expired():
                    # Still in grace period - skip other violation checks
                    pass
                else:
                    # Grace period ended or doesn't exist
                    violation_grace_timer = None
                    
                    # Check head movement (left/right)
                    # Head alignment check
                    face_aligned = is_face_aligned(face_landmarks)

                    if not face_aligned:
                        if head_movement_timer is None:
                            head_movement_timer = CountdownTimer(HEAD_MOVEMENT_GRACE_PERIOD)

                        elif head_movement_timer.expired():
                            if not violations.register(vt.HEAD_MOVEMENT):
                                print("Max violations reached - test stopped")
                                break

                            # Start grace period after violation
                            violation_grace_timer = CountdownTimer(VIOLATION_GRACE_PERIOD)
                            print("Head movement violation counted")
                            head_movement_timer = None

                        # Do NOT evaluate eyes when head is not aligned
                        eye_movement_timer = None

                    else:
                        # Head is straight again
                        if head_movement_timer is not None:
                            print("Head straight - timer reset")
                        head_movement_timer = None

                        # Eye movement check (ONLY when head is straight)
                        if is_eye_movement_suspicious(frame):
                            if eye_movement_timer is None:
                                eye_movement_timer = CountdownTimer(EYE_MOVEMENT_GRACE_PERIOD)

                            elif eye_movement_timer.expired():
                                if not violations.register(vt.EYE_MOVEMENT):
                                    break
                                # Start grace period after violation
                                violation_grace_timer = CountdownTimer(VIOLATION_GRACE_PERIOD)
                        else:
                            eye_movement_timer = None


        elapsed_time = time.time() - test_start_time
        time_left = max(0, TEST_DURATION_SECONDS - elapsed_time)
        
        draw_text(frame, f"Time Left: {int(time_left)}s", 40)
        draw_text(frame, f"Violations: {violations.attempts}/{MAX_VIOLATIONS}", 80)
        
        if face_alignment_timer is not None and not face_aligned:
            alignment_time_left = max(0, FACE_ALIGNMENT_GRACE_PERIOD - (time.time() - face_alignment_timer.start_time))
            draw_text(frame, f"Align face: {int(alignment_time_left)}s", 120)
        
        # Draw face mesh landmarks (only if available)
        if len(faces) == 1:
            try:
                draw_face_mesh(frame, [face_landmarks])
            except:
                pass

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
