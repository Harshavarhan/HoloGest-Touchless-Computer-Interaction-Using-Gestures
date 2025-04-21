import os
import pyautogui
import webbrowser
import logging
import subprocess
import time
import math
import numpy as np
from typing import List, Dict, Optional, Any, Tuple
import win32gui
import win32con
import win32api

logger = logging.getLogger(__name__)

class ApplicationController:
    def __init__(self):
        """Initialize the application controller with cursor control parameters."""
        self.applications: Dict[str, str] = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'explorer': 'explorer.exe',
            'chrome': 'chrome.exe',
            'edge': 'msedge.exe'
        }
        self.folders: Dict[str, str] = {
            'documents': os.path.expanduser('~\\Documents'),
            'downloads': os.path.expanduser('~\\Downloads'),
            'desktop': os.path.expanduser('~\\Desktop'),
            'pictures': os.path.expanduser('~\\Pictures')
        }
        self.screen_width, self.screen_height = pyautogui.size()
        self.cursor_control = {
            'deadzone': 0.1,  # Deadzone to prevent small movements
            'acceleration': 0.3,  # Medium acceleration
            'max_speed': 3,  # Medium maximum speed
            'smoothing_factor': 0.4  # Medium smoothing
        }
        self.sensitivity = 1.0  # Normal sensitivity
        # Set PyAutoGUI failsafe
        pyautogui.FAILSAFE = False
        # Set cursor movement speed
        pyautogui.PAUSE = 0.01  # Medium pause time
        self.last_position = None
        # Gesture timing parameters
        self.click_hold_time = 0.5
        self.double_click_interval = 0.3
        self.last_click_time = 0
        self.hold_start_time = 0
        self.is_holding = False
        # Drag and drop parameters
        self.is_dragging = False
        self.drag_start_position = None
        self.drag_threshold = 10
        # Velocity tracking
        self.velocity_history = []
        self.max_velocity_history = 5
        # Motion prediction
        self.prediction_window = 3  # Number of frames to predict ahead
        self.position_buffer: List[Tuple[float, float, float]] = []  # (x, y, timestamp)
        self.max_buffer_size = 10  # Maximum size of position buffer
        # Error handling
        self.error_count = 0
        self.max_errors = 5
        self.error_reset_time = 5.0  # Time in seconds to reset error count
        self.last_error_time = 0
        # Hover detection
        self.hover_start_time = None
        self.hover_threshold = 2.0  # 2 seconds hover threshold
        self.last_hover_position = None
        self.shutdown_options_shown = False
        logger.info("Application controller initialized with updated cursor control parameters")

    def update_sensitivity(self, base: float = 1.0, vertical: float = 1.0, horizontal: float = 1.0) -> None:
        """
        Update cursor movement sensitivity settings.
        
        Args:
            base: Base sensitivity multiplier
            vertical: Vertical movement sensitivity
            horizontal: Horizontal movement sensitivity
        """
        self.sensitivity = max(0.1, min(base, 3.0))
        logger.info(f"Updated sensitivity settings: base={self.sensitivity}")

    def _calculate_velocity(self, current_x: float, current_y: float) -> Tuple[float, float]:
        """
        Calculate cursor velocity based on position history.
        
        Args:
            current_x: Current x position
            current_y: Current y position
            
        Returns:
            Tuple of (x_velocity, y_velocity)
        """
        current_time = time.time()
        self.velocity_history.append((current_x, current_y, current_time))
        
        # Keep only recent history
        if len(self.velocity_history) > self.max_velocity_history:
            self.velocity_history.pop(0)
        
        if len(self.velocity_history) < 2:
            return 0.0, 0.0
            
        # Calculate velocity from position changes
        total_dx = 0.0
        total_dy = 0.0
        total_dt = 0.0
        
        for i in range(1, len(self.velocity_history)):
            prev_x, prev_y, prev_time = self.velocity_history[i-1]
            curr_x, curr_y, curr_time = self.velocity_history[i]
            dt = curr_time - prev_time
            
            if dt > 0:
                total_dx += (curr_x - prev_x) / dt
                total_dy += (curr_y - prev_y) / dt
                total_dt += dt
        
        if total_dt > 0:
            return total_dx / total_dt, total_dy / total_dt
        return 0.0, 0.0

    def open_application(self, app_name: str) -> bool:
        """Open a desktop application."""
        try:
            if app_name.lower() in self.applications:
                os.system(f'start {self.applications[app_name.lower()]}')
                logger.info(f"Opened application: {app_name}")
                return True
            logger.warning(f"Application not found: {app_name}")
            return False
        except Exception as e:
            logger.error(f"Error opening application: {e}")
            return False

    def open_folder(self, folder_name: str) -> bool:
        """Open a predefined folder."""
        try:
            if folder_name.lower() in self.folders:
                os.startfile(self.folders[folder_name.lower()])
                logger.info(f"Opened folder: {folder_name}")
                return True
            logger.warning(f"Folder not found: {folder_name}")
            return False
        except Exception as e:
            logger.error(f"Error opening folder: {e}")
            return False

    def take_screenshot(self) -> bool:
        """Take a screenshot of the current screen."""
        try:
            screenshot = pyautogui.screenshot()
            screenshots_dir = os.path.join(os.path.expanduser('~\\Pictures'), 'Screenshots')
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f'screenshot_{pyautogui.time.time()}.png')
            screenshot.save(screenshot_path)
            logger.info(f"Screenshot taken and saved to: {screenshot_path}")
            return True
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return False

    def _predict_position(self, current_x: float, current_y: float) -> Tuple[float, float]:
        """
        Predict future cursor position based on recent movement.
        
        Args:
            current_x: Current x position
            current_y: Current y position
            
        Returns:
            Tuple of (predicted_x, predicted_y)
        """
        current_time = time.time()
        self.position_buffer.append((current_x, current_y, current_time))
        
        # Keep buffer size limited
        if len(self.position_buffer) > self.max_buffer_size:
            self.position_buffer.pop(0)
        
        if len(self.position_buffer) < 3:
            return current_x, current_y
            
        # Calculate velocity and acceleration
        positions = np.array([(x, y) for x, y, _ in self.position_buffer])
        times = np.array([t for _, _, t in self.position_buffer])
        
        # Calculate derivatives
        dt = np.diff(times)
        dx = np.diff(positions[:, 0])
        dy = np.diff(positions[:, 1])
        
        if len(dt) > 0 and np.all(dt > 0):
            velocity_x = dx[-1] / dt[-1]
            velocity_y = dy[-1] / dt[-1]
            
            if len(dt) > 1:
                acceleration_x = (dx[-1]/dt[-1] - dx[-2]/dt[-2]) / (dt[-1] + dt[-2])/2
                acceleration_y = (dy[-1]/dt[-1] - dy[-2]/dt[-2]) / (dt[-1] + dt[-2])/2
            else:
                acceleration_x = acceleration_y = 0
                
            # Predict future position
            prediction_time = self.prediction_window * pyautogui.PAUSE
            predicted_x = current_x + velocity_x * prediction_time + 0.5 * acceleration_x * prediction_time**2
            predicted_y = current_y + velocity_y * prediction_time + 0.5 * acceleration_y * prediction_time**2
            
            return predicted_x, predicted_y
            
        return current_x, current_y

    def _handle_error(self, error: Exception) -> None:
        """
        Handle errors with exponential backoff and recovery.
        
        Args:
            error: The exception that occurred
        """
        current_time = time.time()
        
        # Reset error count if enough time has passed
        if current_time - self.last_error_time > self.error_reset_time:
            self.error_count = 0
            
        self.error_count += 1
        self.last_error_time = current_time
        
        if self.error_count >= self.max_errors:
            logger.error(f"Maximum error count reached. Resetting states.")
            self._reset_states()
            self.error_count = 0
        else:
            logger.error(f"Error occurred (count: {self.error_count}): {str(error)}")
            
        # Implement exponential backoff
        backoff_time = min(2 ** self.error_count, 10)  # Cap at 10 seconds
        time.sleep(backoff_time)

    def _reset_states(self) -> None:
        """Reset all internal states to default values."""
        self.last_position = None
        self.is_holding = False
        self.is_dragging = False
        self.drag_start_position = None
        self.last_click_time = 0
        self.velocity_history.clear()
        self.position_buffer.clear()
        self.error_count = 0
        logger.info("All states reset to default values")

    def control_cursor(self, cursor_pos: Dict[str, float], action: str = 'move') -> None:
        """
        Control the cursor based on hand position with hover detection.
        
        Args:
            cursor_pos: Dictionary containing x and y coordinates (0-1 range)
            action: Type of cursor action ('move' or 'click')
        """
        try:
            if not cursor_pos or 'x' not in cursor_pos or 'y' not in cursor_pos:
                logger.warning("Invalid cursor position data")
                return

            # Get normalized coordinates (0-1 range)
            x, y = cursor_pos['x'], cursor_pos['y']
            
            # Calculate center-relative position (-1 to 1 range)
            rel_x = (x - 0.5) * 2
            rel_y = (y - 0.5) * 2
            
            # Apply deadzone
            if abs(rel_x) < self.cursor_control['deadzone']:
                rel_x = 0
            if abs(rel_y) < self.cursor_control['deadzone']:
                rel_y = 0
            
            # Calculate movement speed with acceleration
            speed_x = rel_x * self.cursor_control['acceleration'] * self.sensitivity
            speed_y = rel_y * self.cursor_control['acceleration'] * self.sensitivity
            
            # Limit maximum speed
            speed_x = max(min(speed_x, self.cursor_control['max_speed']), -self.cursor_control['max_speed'])
            speed_y = max(min(speed_y, self.cursor_control['max_speed']), -self.cursor_control['max_speed'])
            
            # Get current cursor position
            current_x, current_y = pyautogui.position()
            
            # Calculate new position with smoothing
            new_x = current_x + (speed_x * self.screen_width * self.cursor_control['smoothing_factor'])
            new_y = current_y + (speed_y * self.screen_height * self.cursor_control['smoothing_factor'])
            
            # Ensure cursor stays within screen bounds
            new_x = max(0, min(new_x, self.screen_width))
            new_y = max(0, min(new_y, self.screen_height))
            
            # Check for hover
            current_time = time.time()
            if self.last_hover_position and abs(new_x - self.last_hover_position[0]) < 5 and abs(new_y - self.last_hover_position[1]) < 5:
                if self.hover_start_time is None:
                    self.hover_start_time = current_time
                elif current_time - self.hover_start_time >= self.hover_threshold:
                    # Hover detected, perform click
                    if action == 'move':
                        pyautogui.click(new_x, new_y)
                        logger.info("Hover click performed")
                        self.hover_start_time = None
            else:
                self.hover_start_time = None
                self.last_hover_position = (new_x, new_y)
            
            logger.debug(f"Moving cursor from ({current_x}, {current_y}) to ({new_x}, {new_y})")
            
            if action == 'move':
                pyautogui.moveTo(new_x, new_y, duration=0.15)  # Medium duration for smooth movement
            elif action == 'click':
                pyautogui.click(new_x, new_y)
                
        except Exception as e:
            logger.error(f"Error controlling cursor: {str(e)}")

    def scroll_page(self, direction: str = 'down', amount: int = 1) -> bool:
        """Scroll web page or document."""
        try:
            if direction.lower() == 'down':
                pyautogui.scroll(-amount * 100)
            else:
                pyautogui.scroll(amount * 100)
            logger.info(f"Scrolled {direction} by {amount} units")
            return True
        except Exception as e:
            logger.error(f"Error scrolling: {e}")
            return False

    def handle_gesture(self, gesture_data: Dict[str, Any]) -> None:
        """Handle the detected gesture."""
        try:
            gesture = gesture_data.get('gesture')
            cursor_pos = gesture_data.get('cursor_pos', {})
            
            if gesture == 'cursor_move':
                self._move_cursor(cursor_pos)
            elif gesture == 'cursor_click':
                self._click()
            elif gesture == 'scroll_up':
                self._scroll_up()
            elif gesture == 'scroll_down':
                self._scroll_down()
            elif gesture == 'take_screenshot':
                self._take_screenshot()
            elif gesture == 'minimize_window':
                self._minimize_window()
            elif gesture == 'open_application':
                self._open_application(cursor_pos)
            elif gesture == 'show_shutdown_options':
                self._show_shutdown_options()
            elif gesture == 'confirm_shutdown':
                self._confirm_shutdown()
                
        except Exception as e:
            logger.error(f"Error handling gesture: {e}")

    def _move_cursor(self, cursor_pos: Dict[str, float]) -> None:
        """Move cursor to the specified position."""
        try:
            screen_width, screen_height = pyautogui.size()
            x = int(cursor_pos['x'] * screen_width)
            y = int(cursor_pos['y'] * screen_height)
            pyautogui.moveTo(x, y, duration=0.1)
        except Exception as e:
            logger.error(f"Error moving cursor: {e}")

    def _click(self) -> None:
        """Perform a mouse click."""
        try:
            pyautogui.click()
        except Exception as e:
            logger.error(f"Error performing click: {e}")

    def _scroll_up(self) -> None:
        """Scroll up."""
        try:
            pyautogui.scroll(100)
        except Exception as e:
            logger.error(f"Error scrolling up: {e}")

    def _scroll_down(self) -> None:
        """Scroll down."""
        try:
            pyautogui.scroll(-100)
        except Exception as e:
            logger.error(f"Error scrolling down: {e}")

    def _take_screenshot(self) -> None:
        """Take a screenshot."""
        try:
            screenshot = pyautogui.screenshot()
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            screenshot.save(filename)
            logger.info(f"Screenshot saved as {filename}")
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")

    def _minimize_window(self) -> None:
        """Minimize the current window."""
        try:
            pyautogui.hotkey('win', 'down')
            logger.info("Window minimized")
        except Exception as e:
            logger.error(f"Error minimizing window: {e}")

    def _open_application(self, cursor_pos: Dict[str, float]) -> None:
        """Open application at cursor position."""
        try:
            # Double click to open application
            pyautogui.doubleClick()
            logger.info("Attempting to open application at cursor position")
        except Exception as e:
            logger.error(f"Error opening application: {e}")

    def _show_shutdown_options(self) -> None:
        """Show shutdown options."""
        try:
            if not self.shutdown_options_shown:
                pyautogui.hotkey('win', 'x')
                time.sleep(0.5)
                pyautogui.press('u')
                self.shutdown_options_shown = True
                logger.info("Shutdown options shown")
        except Exception as e:
            logger.error(f"Error showing shutdown options: {e}")

    def _confirm_shutdown(self) -> None:
        """Confirm system shutdown."""
        try:
            if self.shutdown_options_shown:
                pyautogui.press('s')  # Select shutdown
                self.shutdown_options_shown = False
                logger.info("Shutdown confirmed")
        except Exception as e:
            logger.error(f"Error confirming shutdown: {e}") 