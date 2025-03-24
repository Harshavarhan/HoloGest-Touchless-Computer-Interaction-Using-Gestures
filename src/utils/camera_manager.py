import cv2
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class CameraManager:
    def __init__(self, camera_index: int = 0):
        """
        Initialize the camera manager.
        
        Args:
            camera_index: Index of the camera to use (default: 0)
        """
        self.camera_index = camera_index
        self.cap = None
        self.frame_width = 640
        self.frame_height = 480
        self.fps = 30
        
    def initialize(self) -> bool:
        """
        Initialize the camera with proper settings.
        
        Returns:
            bool: True if camera initialized successfully, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open camera at index {self.camera_index}")
                return False
                
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Verify settings
            actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            logger.info(f"Camera initialized with resolution: {actual_width}x{actual_height} @ {actual_fps}fps")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            return False
            
    def read_frame(self) -> Tuple[bool, Optional[cv2.Mat]]:
        """
        Read a frame from the camera.
        
        Returns:
            Tuple[bool, Optional[cv2.Mat]]: (success, frame)
        """
        if self.cap is None:
            return False, None
            
        ret, frame = self.cap.read()
        if not ret:
            logger.warning("Failed to read frame from camera")
            return False, None
            
        return True, frame
        
    def release(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            logger.info("Camera resources released")
            
    def set_resolution(self, width: int, height: int):
        """
        Set camera resolution.
        
        Args:
            width: Frame width
            height: Frame height
        """
        if self.cap is not None:
            self.frame_width = width
            self.frame_height = height
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
    def set_fps(self, fps: int):
        """
        Set camera FPS.
        
        Args:
            fps: Frames per second
        """
        if self.cap is not None:
            self.fps = fps
            self.cap.set(cv2.CAP_PROP_FPS, fps) 