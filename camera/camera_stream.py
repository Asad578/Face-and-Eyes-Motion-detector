class CameraStream:
    def __init__(self, camera_manager):
        self.camera = camera_manager

    def frames(self):
        while True:
            frame = self.camera.read_frame()
            if frame is None:
                break
            yield frame
