from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions, RunningMode
from mediapipe.tasks.python.core import base_options
import mediapipe as mp

class FaceMeshService:
    _instance = None

    def __init__(self):
        # Create Face Landmarker with MediaPipe Tasks API
        b_options = base_options.BaseOptions(model_asset_path=None)
        options = FaceLandmarkerOptions(base_options=b_options, running_mode=RunningMode.IMAGE)
        self.mesh = FaceLandmarker.create_from_options(options)

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = FaceMeshService()
        return cls._instance.mesh
