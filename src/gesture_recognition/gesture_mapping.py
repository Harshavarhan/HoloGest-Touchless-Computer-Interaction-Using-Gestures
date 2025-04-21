import logging
from typing import Dict, Any, Optional
from ..utils.application_controller import ApplicationController
import win32gui
import win32con
import pyautogui
import time
import os

logger = logging.getLogger(__name__)

class GestureMapping:
    def __init__(self):
        """Initialize gesture mapping with application controller."""
        self.app_controller = ApplicationController()
        self.gesture_actions = {
            'cursor_move': self._handle_cursor_move,
            'cursor_click': self._handle_cursor_click,
            'scroll_up': self._handle_scroll_up,
            'scroll_down': self._handle_scroll_down,
            'take_screenshot': self._handle_screenshot,
            'minimize_window': self._handle_minimize_window,
            'open_application': self._handle_open_application,
            'show_shutdown_options': self._handle_show_shutdown_options,
            'confirm_shutdown': self._handle_confirm_shutdown,
            'press_enter': self._handle_press_enter
        }
        self._last_enter_press = 0
        self._last_screenshot = 0
        logger.info("Gesture mapping initialized with updated gesture controls")

    def execute_gesture(self, gesture_data: Dict[str, Any]) -> None:
        """Execute the appropriate action based on the detected gesture."""
        try:
            if not gesture_data:
                logger.debug("No gesture data received")
                return
                
            gesture = gesture_data.get('gesture')
            cursor_pos = gesture_data.get('cursor_pos')
            
            if gesture in self.gesture_actions:
                logger.debug(f"Executing action for gesture: {gesture}")
                self.gesture_actions[gesture](gesture_data)
            else:
                logger.debug(f"Unknown gesture: {gesture}")
        except Exception as e:
            logger.error(f"Error executing gesture: {str(e)}")

    def _handle_cursor_move(self, gesture_data: Dict[str, Any]) -> None:
        """Handle cursor movement gesture."""
        try:
            cursor_pos = gesture_data.get('cursor_pos', {})
            if isinstance(cursor_pos, dict) and 'x' in cursor_pos and 'y' in cursor_pos:
                logger.debug(f"Processing cursor movement to position: {cursor_pos}")
                self.app_controller.control_cursor(cursor_pos, 'move')
            else:
                logger.warning(f"Invalid cursor position data: {cursor_pos}")
        except Exception as e:
            logger.error(f"Error handling cursor move: {str(e)}")

    def _handle_cursor_click(self, gesture_data: Dict[str, Any]) -> None:
        """Handle cursor click gesture."""
        try:
            cursor_pos = gesture_data.get('cursor_pos', {})
            if isinstance(cursor_pos, dict) and 'x' in cursor_pos and 'y' in cursor_pos:
                self.app_controller.control_cursor(cursor_pos, 'click')
            else:
                logger.warning(f"Invalid cursor position data: {cursor_pos}")
        except Exception as e:
            logger.error(f"Error handling cursor click: {str(e)}")

    def _handle_scroll_up(self, gesture_data: Dict[str, Any]) -> None:
        """Handle scroll up gesture."""
        try:
            self.app_controller.scroll_page('up')
        except Exception as e:
            logger.error(f"Error handling scroll up: {str(e)}")

    def _handle_scroll_down(self, gesture_data: Dict[str, Any]) -> None:
        """Handle scroll down gesture."""
        try:
            self.app_controller.scroll_page('down')
        except Exception as e:
            logger.error(f"Error handling scroll down: {str(e)}")

    def _handle_screenshot(self, gesture_data: Dict[str, Any]) -> None:
        """Handle screenshot gesture."""
        try:
            # Add a small delay to prevent multiple rapid screenshots
            current_time = time.time()
            if hasattr(self, '_last_screenshot') and current_time - self._last_screenshot < 2.0:
                logger.debug("Screenshot throttled")
                return
                
            # Create screenshots directory if it doesn't exist
            screenshots_dir = "screenshots"
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)
                logger.info(f"Created screenshots directory: {screenshots_dir}")
            
            # Take full screen screenshot using pyautogui
            screenshot = pyautogui.screenshot()
            
            # Save screenshot with timestamp in screenshots directory
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")
            screenshot.save(filename)
            
            logger.info(f"Screenshot saved as {filename}")
            self._last_screenshot = current_time
            
        except Exception as e:
            logger.error(f"Error taking screenshot: {str(e)}")
            logger.error(f"Error details: {str(e)}", exc_info=True)

    def _handle_minimize_window(self, gesture_data: Dict[str, Any]) -> None:
        """Handle minimize window gesture."""
        try:
            # Get the current active window
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                # Minimize the window
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                logger.info("Minimized active window")
            else:
                logger.warning("No active window found to minimize")
        except Exception as e:
            logger.error(f"Error minimizing window: {str(e)}")

    def _handle_open_application(self, gesture_data: Dict[str, Any]) -> None:
        """Handle open application gesture."""
        try:
            # TODO: Implement application opening logic
            logger.info("Open application gesture detected")
        except Exception as e:
            logger.error(f"Error handling open application: {str(e)}")

    def _handle_show_shutdown_options(self, gesture_data: Dict[str, Any]) -> None:
        """Handle show shutdown options gesture."""
        try:
            # TODO: Implement shutdown options display
            logger.info("Show shutdown options gesture detected")
        except Exception as e:
            logger.error(f"Error handling show shutdown options: {str(e)}")

    def _handle_confirm_shutdown(self, gesture_data: Dict[str, Any]) -> None:
        """Handle confirm shutdown gesture."""
        try:
            # TODO: Implement shutdown confirmation
            logger.info("Confirm shutdown gesture detected")
        except Exception as e:
            logger.error(f"Error handling confirm shutdown: {str(e)}")

    def _handle_press_enter(self, gesture_data: Dict[str, Any]) -> None:
        """Press the Enter key."""
        try:
            # Add a small delay to prevent multiple rapid presses
            current_time = time.time()
            if current_time - self._last_enter_press < 1.0:
                logger.debug("Enter key press throttled")
                return
                
            # Press Enter key
            pyautogui.press('enter')
            logger.info("Enter key pressed")
            self._last_enter_press = current_time
            
        except Exception as e:
            logger.error(f"Error pressing Enter key: {str(e)}")
            logger.error(f"Error details: {str(e)}", exc_info=True)

    def get_gesture_instructions(self) -> Dict[str, str]:
        """Get human-readable instructions for each gesture."""
        return {
            'cursor_move': 'Point with index finger to move cursor',
            'cursor_click': 'Quickly extend all fingers once for single click, twice for double click',
            'scroll_up': 'Raise index and middle fingers to scroll up',
            'scroll_down': 'Lower index and middle fingers to scroll down',
            'press_enter': 'Touch index and middle fingers to thumb to press Enter',
            'minimize_window': 'Raise index and middle fingers with hover to minimize',
            'open_application': 'Raise index, middle, and ring fingers to open app',
            'show_shutdown_options': 'Raise index, middle, ring, and pinky fingers to show shutdown options',
            'confirm_shutdown': 'Make a fist with hover to confirm shutdown',
            'take_screenshot': 'Extend index, middle, and ring fingers (others closed) to take screenshot'
        } 