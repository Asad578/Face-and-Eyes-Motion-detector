# Online Test Proctoring System

A Python-based machine learning program that monitors and proctors online exams by detecting suspicious behavior through computer vision and deep learning.

## Features

- **Face Detection**: Uses Haar Cascade to detect face presence and count
- **Head Pose Detection**: Uses MediaPipe to verify head is straight to camera
- **Eye Gaze Detection**: Detects if eyes are looking away from screen
- **Phone Detection**: Uses YOLOv8 to detect mobile phones immediately
- **Face Distance Validation**: Ensures face is at proper distance from camera
- **Real-time Monitoring**: Displays violations and remaining time
- **Grace Periods**: 3-second recovery time for each violation type

## System Requirements

- Python 3.8+
- Webcam/Camera device
- 4GB+ RAM (for YOLO model)
- Windows/Linux/macOS

## Installation

### 1. Clone/Create the Project
```bash
cd c:\Users\aabah\Desktop\AI-ML\online_test
```

### 2. Create Virtual Environment (if not already done)
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config/settings.py` to customize behavior:

```python
TEST_DURATION_SECONDS = 120          # Total test time (2 minutes)
NO_FACE_GRACE_PERIOD = 3             # Time to detect face (3 seconds)
FACE_ALIGNMENT_GRACE_PERIOD = 5      # Stabilization time (5 seconds)
VIOLATION_GRACE_PERIOD = 3           # Recovery time per violation (3 seconds)
MAX_VIOLATIONS = 2                   # Maximum allowed violations
FACE_MIN_AREA_RATIO = 0.3            # Minimum face size
FACE_MAX_AREA_RATIO = 0.6            # Maximum face size
```

## Running the Program

### Basic Usage
```bash
python main.py
```

The program will:
1. Open your webcam
2. Detect your face
3. Wait for face alignment (5 seconds of proper positioning)
4. Monitor for violations during 2-minute test
5. Display violations and terminate when limits exceeded

### Exit Options
- Press **'q'** key in video window to quit
- Automatic exit when violations exceed MAX_VIOLATIONS (2)
- Automatic exit after 2-minute timer expires

## Violation Types

| Violation | Trigger | Grace Period | Action |
|-----------|---------|--------------|--------|
| **No Face** | No face detected | 3 sec | Shows timer |
| **Multiple Faces** | >1 face in frame | None | Immediate stop |
| **Phone Detected** | Mobile phone found | None | Immediate stop |
| **Face Distance** | Too close or far | 3 sec | Shows 3s recovery |
| **Head Movement** | Head not straight | 3 sec | Shows 3s recovery |
| **Eye Movement** | Eyes looking away | 3 sec | Shows 3s recovery |

## Display Information

During test, you'll see:
- **Time Left**: Countdown to 2-minute limit
- **Violations**: Current count vs maximum allowed
- **Align Face**: Countdown when waiting for proper positioning

Example:
```
Time Left: 95s
Violations: 1/2
Align face: 3s
```

## Program Flow

```
Start
  ↓
Initialize camera & timers
  ↓
Wait for face (3 sec grace)
  ↓
Check face count (1 required)
  ↓
Validate face distance
  ↓
Check head position (straight required)
  ↓
Align face (5 sec stabilization)
  ↓
Monitor eye movement
  ↓
Check for phone (any time, immediate stop)
  ↓
Repeat until:
  - Test time expires (2 min)
  - Violations exceed limit (>2)
  - 'q' key pressed
  ↓
Show violations & exit
```

## Violation Recovery

When a violation is detected:
1. **Grace Timer Starts** (3 seconds)
2. User has 3 seconds to correct behavior
3. If corrected within 3 sec → Continue test
4. If not corrected → Violation count increases
5. If violations > 2 → Program stops

### Example: Head Movement Violation
```
Sec 0: Head moves left → Grace timer starts
Sec 1: Head returns to center → Timer resets, no violation
Test continues...
```

```
Sec 0: Head moves left → Grace timer starts
Sec 3: Head still tilted → Violation registered
Sec 3: Attempt count = 1/2
```

## Output

When program ends, console shows:
```
Test Ended
Total violations: 2
Violation Details:
  - No face detected
  - Suspicious eye movement
```

## Testing

Run logic tests (without camera):
```bash
python test_logic.py
```

This verifies:
- Timer functionality
- Violation counting
- Grace period handling
- Program flow logic

## Troubleshooting

### Camera not found
- Check camera connection
- Try different camera index: Edit `camera_manager.py` line 5
- `self.cap = cv2.VideoCapture(1)  # Try camera index 1, 2, etc.`

### YOLO model slow to load
- First run downloads the model (~70MB)
- Subsequent runs load from cache (faster)
- Model loads on first phone detection call

### Face detection not working
- Ensure adequate lighting
- Face should be clearly visible
- At least 30cm from camera

### Eyes not detected
- Need clear face frontal view
- Eyes must be open
- Avoid excessive shadows on face

## File Structure

```
online_test/
├── main.py                          # Main program
├── requirements.txt                 # Dependencies
├── config/
│   └── settings.py                 # Configuration
├── camera/
│   ├── camera_manager.py          # Camera handling
│   └── camera_stream.py           # Frame streaming
├── detectors/
│   ├── face_detector.py           # Face detection
│   ├── face_mesh_service.py       # Face landmarks
│   ├── head_pose_detector.py      # Head orientation
│   ├── eye_gaze_detector.py       # Eye direction
│   └── phone_detector.py          # Phone detection
├── validators/
│   ├── face_distance.py           # Distance validation
│   └── face_alignment.py          # Alignment check
├── violations/
│   ├── violation_manager.py       # Violation tracking
│   └── violation_types.py         # Violation constants
├── timers/
│   └── countdown_timer.py         # Timer utility
└── utils/
    ├── drawing.py                 # Display utilities
    └── helpers.py                 # Helper functions
```

## Technical Stack

- **OpenCV**: Video capture and face detection
- **MediaPipe**: Face landmarks and mesh
- **YOLOv8**: Object detection (phone)
- **PyTorch**: Deep learning framework
- **NumPy**: Numerical computations

## Performance

- **FPS**: 20-30 FPS on modern hardware
- **Latency**: ~50-100ms for detection
- **Memory**: ~500MB-1GB active
- **YOLO Model**: First load ~5sec, cached runs ~0.5sec

## Limitations

- Requires adequate lighting
- Single camera input only
- Face must be frontal view
- Not foolproof against sophisticated cheating methods

## Future Improvements

- Multiple camera support
- Audio monitoring
- Screen recording integration
- Advanced anti-spoofing (liveness detection)
- Mobile app compatibility
- Cloud storage for violations
- Database logging

## Support

For issues or questions:
1. Check FIXES_AND_IMPROVEMENTS.md for recent changes
2. Review test_logic.py for expected behavior
3. Check camera permissions in OS
4. Verify all dependencies installed: `pip list`

## License

[Add your license here]

## Author

[Add author information here]

---

**Last Updated**: January 15, 2026
**Version**: 1.0 (Fixed and Enhanced)
