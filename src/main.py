#!/usr/bin/env python3
import sys
import logging
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from gesture_recognition.gesture_detector import GestureDetector
from utils.helpers import setup_logging

def main():
    # Setup logging
    logger = setup_logging()
    logger.info("Starting HoloGest application")
    
    try:
        # Initialize Qt application
        app = QApplication(sys.argv)
        
        # Initialize gesture detector
        gesture_detector = GestureDetector()
        
        # Create and show main window
        window = MainWindow(gesture_detector)
        window.show()
        
        # Start the event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 