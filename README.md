# Online Test Proctoring System

A real-time AI/ML-powered proctoring solution for monitoring candidates during remote online tests. Built with Python, OpenCV, and MediaPipe to detect and log violations with intelligent grace periods to minimize false positives.

## 🎯 Features

- **Real-time Face Detection** — Detects and validates face presence using OpenCV Haar Cascades
- **Face Mesh Landmarks** — Advanced facial geometry tracking via MediaPipe for precise head pose and alignment validation
- **Multi-violation Tracking** — Monitors:
  - No face detected
  - Multiple faces in frame
  - Invalid face distance (too close/far)
  - Head movement/misalignment
  - Eye movement (placeholder for future enhancement)
- **Grace Period Logic** — Configurable timers prevent false alarms from transient camera glitches
- **Countdown Timers** — Temporal gating with countdown logic for violation detection
- **Violation Management** — Central violation registry with max violation limit enforcement
- **Live Visual Overlay** — Real-time display of:
  - Remaining test time
  - Current violation count
  - Active violation types
  - Face mesh landmarks
- **Automatic Test Termination** — Stops when max violations reached or test duration expires
- **Modular Architecture** — Cleanly separated concerns for easy testing and extension

## 📦 Project Structure

```
online_test/
├── main.py                          # Entry point & main test loop
├── requirements.txt                 # Python dependencies
├── yolov8n.pt                       # YOLOv8 nano model
├── camera/
│   ├── camera_manager.py            # Camera capture initialization
│   └── camera_stream.py             # Frame iteration pipeline
├── config/
│   └── settings.py                  # Global configuration & constants
├── detectors/
│   ├── face_detector.py             # Haar Cascade face detection
│   ├── face_mesh_service.py         # MediaPipe face mesh service
│   ├── head_pose_detector.py        # Head orientation analysis
│   ├── eye_gaze_detector.py         # Eye movement detection
│   ├── phone_detector.py            # Object detection for phones (future)
│   ├── haarcascade_eye.xml          # Pre-trained eye classifier
│   └── haarcascade_frontalface_default.xml  # Pre-trained face classifier
├── models/
│   └── face_landmarker.task         # MediaPipe face landmarker model
├── validators/
│   ├── face_alignment.py            # Face straightness validation
│   └── face_distance.py             # Face distance validation
├── timers/
│   └── countdown_timer.py           # Reusable countdown timer utility
├── utils/
│   └── drawing.py                   # OpenCV frame drawing utilities
└── violations/
    ├── violation_manager.py         # Violation registry & tracking
    └── violation_types.py           # Violation type enumerations
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Windows/Linux/macOS
- Webcam/Camera device

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd online_test
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

Run the proctoring system:

```bash
python main.py
```

**Controls:**
- Press `Q` to quit at any time
- The test runs for a configured duration (default: 300 seconds / 5 minutes)
- Maximum violations limit stops the test early (default: 5 violations)

**Output:**
The system displays:
- Real-time video feed with face mesh overlay
- Time remaining countdown
- Current violation count
- Active violation types (red status boxes)
- Exits with violation summary

## ⚙️ Configuration

Edit [config/settings.py](config/settings.py) to customize:

```python
TEST_DURATION_SECONDS        # Test duration in seconds (default: 300)
MAX_VIOLATIONS               # Maximum allowed violations (default: 5)
NO_FACE_GRACE_PERIOD         # Grace period when no face (default: 3s)
FACE_DISTANCE_GRACE_PERIOD   # Grace period for face distance (default: 1s)
HEAD_MOVEMENT_GRACE_PERIOD   # Grace period for head movement (default: 2s)
EYE_MOVEMENT_GRACE_PERIOD    # Grace period for eye movement (default: 1.5s)
VIOLATION_GRACE_PERIOD       # Global grace period after any violation (default: 3s)
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Computer Vision** | OpenCV 4.x |
| **Face Detection** | Haar Cascades (OpenCV) |
| **Face Landmarks** | MediaPipe Face Mesh |
| **Language** | Python 3.x |
| **Real-time Processing** | Webcam stream via OpenCV |

## 📊 Violation Types

| Type | Trigger | Grace Period |
|------|---------|--------------|
| **NO_FACE** | No face detected for 1.5s | 3s to recover |
| **MULTIPLE_FACES** | >1 face in frame for 1s | 3s to recover |
| **FACE_DISTANCE** | Face too close/far for 1s | Grace period applies |
| **HEAD_MOVEMENT** | Head not aligned for 2s | Grace period applies |
| **EYE_MOVEMENT** | Suspicious eye gaze (disabled) | — |

## 🔄 Violation Logic Flow

```
Detect Face → Validate Distance → Validate Alignment → Validate Eyes
                                        ↓
                        Grace Period Applied After Violation
                                        ↓
                        Other Checks Skip During Grace Period
```

## 📈 Future Enhancements

- [ ] Enable eye movement detection (currently commented out)
- [ ] Add phone/external device detection
- [ ] Implement screen recording capability
- [ ] Database integration for violation logging
- [ ] Dashboard for test administrators
- [ ] Multi-camera support
- [ ] Performance optimization for low-end devices
- [ ] LMS integration (Moodle, Canvas, etc.)
- [ ] Facial recognition for identity verification

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Eye gaze detection refinement
- Object detection for disallowed items
- Network synchronization for remote monitoring
- Unit tests & integration tests
- Documentation enhancements

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this project, provided you include the original copyright notice and license.

## 👤 Author

Name: Asad Ahmad Bajwa
GitHub Profile: https://github.com/Asad578

## 📧 Support

For questions, feedback, or collaboration:
- Open an issue on GitHub
- DM on LinkedIn: https://www.linkedin.com/in/asad-ahmad-bajwa-0b59a7270/

---

**Note:** This is a prototype for research and educational purposes. For production use in high-stakes exams, additional security measures and user privacy considerations are required.
