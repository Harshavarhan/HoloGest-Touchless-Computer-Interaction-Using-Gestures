from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import logging
from utils.camera_manager import CameraManager

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, gesture_detector):
        super().__init__()
        self.gesture_detector = gesture_detector
        self.camera_manager = CameraManager()
        self.init_ui()
        self.setup_camera()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('HoloGest')
        self.setGeometry(100, 100, 800, 600)
        
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
        
        # Create control buttons
        button_layout = QHBoxLayout()
        
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
        processed_frame, gesture = self.gesture_detector.detect_gestures(frame)
        
        # Update status if gesture detected
        if gesture:
            self.status_label.setText(f'Status: Detected gesture - {gesture}')
        
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