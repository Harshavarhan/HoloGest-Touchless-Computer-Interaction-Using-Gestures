import logging
import os
from datetime import datetime
import cv2
from typing import List

def setup_logging() -> logging.Logger:
    """
    Setup logging configuration.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging
    log_file = f'logs/hologest_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def get_camera_devices() -> List[int]:
    """
    Get list of available camera devices.
    
    Returns:
        List[int]: List of available camera indices
    """
    devices = []
    for i in range(10):  # Check first 10 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            devices.append(i)
            cap.release()
    return devices

def calculate_gesture_confidence(landmarks, gesture_type: str) -> float:
    """
    Calculate confidence score for a detected gesture.
    
    Args:
        landmarks: Hand landmarks from MediaPipe
        gesture_type: Type of gesture to check
        
    Returns:
        float: Confidence score between 0 and 1
    """
    # TODO: Implement gesture confidence calculation
    return 0.0 