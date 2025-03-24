import pytest
from PyQt5.QtWidgets import QApplication, QCheckBox
from PyQt5.QtCore import Qt
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
    assert main_window.camera_label is not None
    assert main_window.status_label is not None
    assert main_window.settings_button is not None
    assert main_window.camera_button is not None

def test_settings_window_initialization(settings_window):
    """Test if settings window initializes correctly."""
    assert settings_window is not None
    assert settings_window.windowTitle() == 'HoloGest Settings'
    assert settings_window.sensitivity_slider is not None
    assert settings_window.camera_combo is not None
    assert len(settings_window.gesture_toggles) > 0

def test_settings_slider_range(settings_window):
    """Test if sensitivity slider has correct range."""
    assert settings_window.sensitivity_slider.minimum() == 1
    assert settings_window.sensitivity_slider.maximum() == 10
    assert settings_window.sensitivity_slider.value() == 5

def test_gesture_toggles(settings_window):
    """Test if gesture toggles are properly initialized."""
    for gesture, toggle in settings_window.gesture_toggles.items():
        assert toggle.isChecked()  # All toggles should be checked by default
        assert isinstance(toggle, QCheckBox) 