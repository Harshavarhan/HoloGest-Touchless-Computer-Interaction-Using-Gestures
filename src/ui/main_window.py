from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QMessageBox, QHBoxLayout, QComboBox,
                            QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import logging
from src.utils.camera_manager import CameraManager
from src.gesture_recognition.gesture_mapping import GestureMapping

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, gesture_detector):
        super().__init__()
        self.gesture_detector = gesture_detector
        self.camera_manager = CameraManager()
        self.gesture_mapping = GestureMapping()
        self.init_ui()
        self.setup_camera()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('HoloGest - Touchless Computer Interaction')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create camera display label
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        layout.addWidget(self.camera_label)
        
        # Create status label
        self.status_label = QLabel('Status: Ready')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Create gesture info label
        self.gesture_label = QLabel('Current Gesture: None')
        self.gesture_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.gesture_label)
        
        # Create gesture help group
        gesture_help_group = QGroupBox("Gesture Controls")
        gesture_help_layout = QGridLayout()
        
        # Add gesture descriptions
        gesture_help_layout.addWidget(QLabel("Pointing Gesture:"), 0, 0)
        gesture_help_layout.addWidget(QLabel("Raise index finger to move cursor"), 0, 1)
        
        gesture_help_layout.addWidget(QLabel("Click Gesture:"), 1, 0)
        gesture_help_layout.addWidget(QLabel("Raise index and thumb fingers"), 1, 1)
        
        gesture_help_layout.addWidget(QLabel("Scroll Up:"), 2, 0)
        gesture_help_layout.addWidget(QLabel("Raise little finger (pinky)"), 2, 1)
        
        gesture_help_layout.addWidget(QLabel("Scroll Down:"), 3, 0)
        gesture_help_layout.addWidget(QLabel("Raise ring finger"), 3, 1)
        
        gesture_help_layout.addWidget(QLabel("Screenshot:"), 4, 0)
        gesture_help_layout.addWidget(QLabel("Extend all five fingers"), 4, 1)
        
        gesture_help_layout.addWidget(QLabel("Enter Key:"), 5, 0)
        gesture_help_layout.addWidget(QLabel("Extend all five fingers"), 5, 1)
        
        gesture_help_layout.addWidget(QLabel("Minimize Window:"), 6, 0)
        gesture_help_layout.addWidget(QLabel("Raise index and middle fingers"), 6, 1)
        
        gesture_help_layout.addWidget(QLabel("Open Application:"), 7, 0)
        gesture_help_layout.addWidget(QLabel("Extend index, middle, and ring fingers"), 7, 1)
        
        gesture_help_layout.addWidget(QLabel("Shutdown Options:"), 8, 0)
        gesture_help_layout.addWidget(QLabel("Extend index and little finger"), 8, 1)
        
        gesture_help_layout.addWidget(QLabel("Confirm Shutdown:"), 9, 0)
        gesture_help_layout.addWidget(QLabel("Extend thumb, index, and little finger"), 9, 1)
        
        gesture_help_group.setLayout(gesture_help_layout)
        layout.addWidget(gesture_help_group)
        
        # Create control buttons
        button_layout = QHBoxLayout()
        
        # Application selection
        self.app_combo = QComboBox()
        self.app_combo.addItems(['Notepad', 'Calculator', 'Explorer', 'Chrome'])
        button_layout.addWidget(self.app_combo)
        
        # Folder selection
        self.folder_combo = QComboBox()
        self.folder_combo.addItems(['Documents', 'Downloads', 'Desktop', 'Pictures'])
        button_layout.addWidget(self.folder_combo)
        
        # Control buttons
        self.settings_button = QPushButton('Settings')
        self.settings_button.clicked.connect(self.show_settings)
        button_layout.addWidget(self.settings_button)
        
        self.camera_button = QPushButton('Switch Camera')
        self.camera_button.clicked.connect(self.switch_camera)
        button_layout.addWidget(self.camera_button)
        
        layout.addLayout(button_layout)
        
        # Setup camera timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
    def setup_camera(self):
        """Initialize the camera."""
        if not self.camera_manager.initialize():
            QMessageBox.critical(
                self,
                'Camera Error',
                'Failed to initialize camera. Please check your camera connection and permissions.'
            )
            self.status_label.setText('Status: Camera not available')
            return
            
        self.status_label.setText('Status: Camera initialized')
        self.timer.start(30)  # 30ms = ~33fps
        
    def update_frame(self):
        """Update the camera frame and process gestures."""
        success, frame = self.camera_manager.read_frame()
        if not success:
            return
            
        # Process frame for gestures
        processed_frame, gesture_data = self.gesture_detector.detect_gestures(frame)
        
        # Update status if gesture detected
        if gesture_data:
            gesture = gesture_data.get('gesture')
            if gesture:
                self.gesture_label.setText(f'Current Gesture: {gesture}')
                
                # Execute gesture command
                self.gesture_mapping.execute_gesture(gesture_data)
                
                # Update status based on gesture type
                if gesture.startswith('cursor_'):
                    self.status_label.setText(f'Status: Controlling cursor')
                elif gesture.startswith('scroll_'):
                    self.status_label.setText(f'Status: Scrolling {gesture.split("_")[1]}')
                elif gesture == 'take_screenshot':
                    self.status_label.setText('Status: Screenshot taken')
        else:
            self.gesture_label.setText('Current Gesture: None')
            self.status_label.setText('Status: Ready')
        
        # Convert frame to QImage and display
        rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(qt_image))
        
    def switch_camera(self):
        """Switch to the next available camera."""
        self.camera_manager.release()
        self.camera_manager.camera_index = (self.camera_manager.camera_index + 1) % 2
        self.setup_camera()
        
    def show_settings(self):
        """Show the settings window."""
        # TODO: Implement settings window
        pass
        
    def closeEvent(self, event):
        """Handle application closure."""
        self.camera_manager.release()
        self.gesture_detector.release()
        event.accept()
