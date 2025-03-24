import pytest
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.settings import SettingsWindow
from src.gesture_recognition.gesture_detector import GestureDetector

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def gesture_detector():
    return GestureDetector()

@pytest.fixture
def main_window(app, gesture_detector):
    window = MainWindow(gesture_detector)
    yield window
    window.close()
    window.deleteLater()

@pytest.fixture
def settings_window(app):
    window = SettingsWindow()
    yield window
    window.close()
    window.deleteLater()

def test_main_window_initialization(main_window):
    """Test if main window initializes correctly."""
    assert main_window is not None
    assert main_window.windowTitle() == 'HoloGest'

def test_settings_window_initialization(settings_window):
    """Test if settings window initializes correctly."""
    assert settings_window is not None
    assert settings_window.windowTitle() == 'HoloGest Settings'

def test_settings_slider_range(settings_window):
    """Test if sensitivity slider has correct range."""
    assert settings_window.sensitivity_slider.minimum() == 1
    assert settings_window.sensitivity_slider.maximum() == 10
    assert settings_window.sensitivity_slider.value() == 5 