from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2

class MainWindow(QMainWindow):
    def __init__(self, gesture_detector):
        super().__init__()
        self.gesture_detector = gesture_detector
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
        layout.addWidget(self.camera_label)
        
        # Create status label
        self.status_label = QLabel('Status: Ready')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Create control buttons
        self.settings_button = QPushButton('Settings')
        self.settings_button.clicked.connect(self.show_settings)
        layout.addWidget(self.settings_button)
        
        # Setup camera timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
    def setup_camera(self):
        """Initialize the camera."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.setText('Status: Camera not available')
            return
        self.timer.start(30)  # 30ms = ~33fps
        
    def update_frame(self):
        """Update the camera frame and process gestures."""
        ret, frame = self.cap.read()
        if not ret:
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
        
    def show_settings(self):
        """Show the settings window."""
        # TODO: Implement settings window
        pass
        
    def closeEvent(self, event):
        """Handle application closure."""
        self.cap.release()
        self.gesture_detector.release()
        event.accept() 