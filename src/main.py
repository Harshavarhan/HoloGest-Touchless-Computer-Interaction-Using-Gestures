#!/usr/bin/env python3
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.gesture_recognition.gesture_detector import GestureDetector
from src.utils.helpers import setup_logging

def main():
    # Setup logging with more verbose output
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting HoloGest application")
    
    try:
        # Initialize Qt application
        logger.debug("Initializing Qt Application")
        app = QApplication(sys.argv)
        
        # Initialize gesture detector
        logger.debug("Initializing Gesture Detector")
        gesture_detector = GestureDetector()
        
        # Create and show main window
        logger.debug("Creating Main Window")
        window = MainWindow(gesture_detector)
        logger.debug("Showing Main Window")
        window.show()
        
        logger.info("Application initialized successfully. Starting event loop.")
        print("HoloGest is running. Press Ctrl+C to exit.")
        
        # Start the event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 