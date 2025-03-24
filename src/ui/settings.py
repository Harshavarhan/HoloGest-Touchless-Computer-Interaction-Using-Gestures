import logging
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QSlider, QPushButton, QCheckBox,
                             QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
from utils.camera_manager import CameraManager

logger = logging.getLogger(__name__)

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.camera_manager = CameraManager()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the settings interface."""
        self.setWindowTitle('HoloGest Settings')
        self.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout(self)
        
        # Gesture sensitivity
        sensitivity_layout = QHBoxLayout()
        sensitivity_label = QLabel('Gesture Sensitivity:')
        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setRange(1, 10)
        self.sensitivity_slider.setValue(5)
        sensitivity_layout.addWidget(sensitivity_label)
        sensitivity_layout.addWidget(self.sensitivity_slider)
        layout.addLayout(sensitivity_layout)
        
        # Camera settings
        camera_layout = QHBoxLayout()
        camera_label = QLabel('Camera Device:')
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(['Default Camera', 'External Camera'])
        camera_layout.addWidget(camera_label)
        camera_layout.addWidget(self.camera_combo)
        layout.addLayout(camera_layout)
        
        # Gesture toggles
        self.gesture_toggles = {}
        gestures = ['Swipe Left', 'Swipe Right', 'Thumbs Up', 
                   'Thumbs Down', 'Palm Open', 'Palm Closed']
        for gesture in gestures:
            toggle = QCheckBox(gesture)
            toggle.setChecked(True)
            self.gesture_toggles[gesture] = toggle
            layout.addWidget(toggle)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
    def save_settings(self):
        """Save the current settings."""
        try:
            # Save sensitivity
            sensitivity = self.sensitivity_slider.value()
            logger.info(f"Saving sensitivity setting: {sensitivity}")
            
            # Save camera selection
            camera_index = self.camera_combo.currentIndex()
            logger.info(f"Saving camera selection: {camera_index}")
            
            # Save gesture toggles
            enabled_gestures = [
                gesture for gesture, toggle in self.gesture_toggles.items()
                if toggle.isChecked()
            ]
            logger.info(f"Saving enabled gestures: {enabled_gestures}")
            
            # TODO: Implement actual settings saving
            
            QMessageBox.information(
                self,
                'Settings Saved',
                'Your settings have been saved successfully.'
            )
            self.accept()
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.critical(
                self,
                'Error',
                'Failed to save settings. Please try again.'
            ) 