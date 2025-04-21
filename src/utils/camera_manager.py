import cv2
import logging

logger = logging.getLogger(__name__)

class CameraManager:
    def __init__(self, camera_index=0):
        """Initialize camera manager."""
        self.camera_index = camera_index
        self.camera = None
        logger.info("Camera manager initialized")

    def initialize(self) -> bool:
        """Initialize camera capture."""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            if not self.camera.isOpened():
                logger.error("Failed to open camera")
                return False
            logger.info("Camera initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            return False

    def read_frame(self):
        """Read a frame from the camera."""
        if self.camera is None:
            return False, None
        return self.camera.read()

    def release(self):
        """Release camera resources."""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
            logger.info("Camera resources released") 