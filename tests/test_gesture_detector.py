import pytest
import numpy as np
from src.gesture_recognition.gesture_detector import GestureDetector

@pytest.fixture
def gesture_detector():
    return GestureDetector()

def test_gesture_detector_initialization(gesture_detector):
    """Test if gesture detector initializes correctly."""
    assert gesture_detector is not None
    assert gesture_detector.hands is not None
    assert gesture_detector.mp_draw is not None

def test_detect_gestures_empty_frame(gesture_detector):
    """Test gesture detection with empty frame."""
    empty_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    processed_frame, gesture = gesture_detector.detect_gestures(empty_frame)
    
    assert processed_frame is not None
    assert gesture is None
    assert processed_frame.shape == empty_frame.shape

def test_release_resources(gesture_detector):
    """Test if resources are released properly."""
    gesture_detector.release()
    # Add assertions based on your implementation 