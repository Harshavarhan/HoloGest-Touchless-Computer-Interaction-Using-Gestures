import cv2
import mediapipe as mp
import numpy as np
import logging
from typing import Tuple, Optional, Dict, Any
import pyautogui
import time

logger = logging.getLogger(__name__)

class GestureDetector:
    def __init__(self):
        """Initialize the gesture detector with updated parameters."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.gesture_data = self._load_gesture_data()
        # Set PyAutoGUI failsafe
        pyautogui.FAILSAFE = False
        # Set cursor movement speed
        pyautogui.PAUSE = 0.01
        # Initialize click tracking
        self._last_click_time = 0
        self._click_count = 0
        self._click_threshold = 0.5  # seconds between clicks for double-click
        logger.info("Gesture detector initialized with updated parameters")

    def detect_gestures(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[Dict]]:
        """
        Detect hand gestures in the given frame.
        
        Args:
            frame: numpy.ndarray, BGR image frame
            
        Returns:
            tuple: (processed_frame, gesture_data)
            gesture_data: dict containing gesture name and parameters
        """
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = self.hands.process(rgb_frame)
            
            # Draw hand landmarks and detect gestures
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2)
                    )
                    
                    # Analyze gesture
                    gesture_data = self._analyze_gesture(hand_landmarks)
                    if gesture_data and gesture_data.get('gesture'):
                        # Draw gesture name on frame
                        gesture_name = self.gesture_data[gesture_data['gesture']]['name']
                        cv2.putText(frame, f"Gesture: {gesture_name}", (10, 30),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # Draw cursor position
                        if 'cursor_pos' in gesture_data:
                            x, y = gesture_data['cursor_pos']['x'], gesture_data['cursor_pos']['y']
                            h, w = frame.shape[:2]
                            screen_x, screen_y = int(x * w), int(y * h)
                            cv2.circle(frame, (screen_x, screen_y), 5, (255, 0, 0), -1)
                            
                        return frame, gesture_data
                    
            return frame, None
            
        except Exception as e:
            logger.error(f"Error in gesture detection: {e}")
            return frame, None

    def _calculate_finger_angle(self, tip, pip, mcp):
        """Calculate the angle between finger segments."""
        try:
            # Convert landmarks to numpy arrays
            tip = np.array([tip.x, tip.y, tip.z])
            pip = np.array([pip.x, pip.y, pip.z])
            mcp = np.array([mcp.x, mcp.y, mcp.z])
            
            # Calculate vectors
            v1 = pip - mcp
            v2 = tip - pip
            
            # Calculate angle
            angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
            return np.degrees(angle)
        except Exception as e:
            logger.error(f"Error calculating finger angle: {str(e)}")
            return 0

    def _is_pointing_gesture(self, landmarks) -> bool:
        """Check if the hand is making a pointing gesture."""
        try:
            # Check if index finger is extended (tip is above pip)
            index_extended = landmarks['index']['tip'].y < landmarks['index']['pip'].y

            # Check if other fingers are folded (tips are below index pip)
            others_folded = all([
                landmarks['middle']['tip'].y > landmarks['index']['pip'].y,
                landmarks['ring']['tip'].y > landmarks['index']['pip'].y,
                landmarks['pinky']['tip'].y > landmarks['index']['pip'].y
            ])

            is_pointing = index_extended and others_folded
            if is_pointing:
                logger.debug("Pointing gesture detected")
                logger.debug(f"Index tip Y: {landmarks['index']['tip'].y:.3f}, Index PIP Y: {landmarks['index']['pip'].y:.3f}")
                logger.debug("Other fingers Y: {:.3f}, {:.3f}, {:.3f}".format(
                    landmarks['middle']['tip'].y, landmarks['ring']['tip'].y, landmarks['pinky']['tip'].y
                ))

            return is_pointing

        except Exception as e:
            logger.error(f"Error in pointing gesture detection: {str(e)}")
            return False

    def _is_click_gesture(self, landmarks) -> bool:
        """Check if hand is in click gesture (quick finger extension)."""
        try:
            # Check if all fingers are extended
            all_fingers_extended = all([
                landmarks['thumb']['tip'].y < landmarks['thumb']['mcp'].y,
                landmarks['index']['tip'].y < landmarks['index']['pip'].y,
                landmarks['middle']['tip'].y < landmarks['middle']['pip'].y,
                landmarks['ring']['tip'].y < landmarks['ring']['pip'].y,
                landmarks['pinky']['tip'].y < landmarks['pinky']['pip'].y
            ])
            
            if all_fingers_extended:
                current_time = time.time()
                time_since_last_click = current_time - self._last_click_time
                
                if time_since_last_click < self._click_threshold:
                    self._click_count += 1
                    if self._click_count == 2:
                        logger.debug("Double click gesture detected")
                        self._click_count = 0
                        return True
                else:
                    self._click_count = 1
                    logger.debug("Single click gesture detected")
                
                self._last_click_time = current_time
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error in click gesture detection: {str(e)}")
            return False

    def _is_scroll_up_gesture(self, landmarks) -> bool:
        """Check if hand is in scroll up gesture."""
        try:
            pinky_tip = landmarks['pinky']['tip']
            index_tip = landmarks['index']['tip']
            return pinky_tip.y < index_tip.y - 0.1
        except Exception as e:
            logger.error(f"Error in scroll up gesture detection: {str(e)}")
            return False

    def _is_scroll_down_gesture(self, landmarks) -> bool:
        """Check if hand is in scroll down gesture."""
        try:
            ring_tip = landmarks['ring']['tip']
            index_tip = landmarks['index']['tip']
            return ring_tip.y < index_tip.y - 0.1
        except Exception as e:
            logger.error(f"Error in scroll down gesture detection: {str(e)}")
            return False

    def _is_screenshot_gesture(self, landmarks) -> bool:
        """Check if hand is in screenshot gesture (index, middle, and ring fingers extended)."""
        try:
            # Check if index, middle, and ring fingers are extended
            index_extended = landmarks['index']['tip'].y < landmarks['index']['pip'].y
            middle_extended = landmarks['middle']['tip'].y < landmarks['middle']['pip'].y
            ring_extended = landmarks['ring']['tip'].y < landmarks['ring']['pip'].y
            
            # Check if thumb and pinky are folded
            thumb_folded = landmarks['thumb']['tip'].y > landmarks['thumb']['mcp'].y
            pinky_folded = landmarks['pinky']['tip'].y > landmarks['pinky']['pip'].y
            
            is_screenshot = all([
                index_extended,
                middle_extended,
                ring_extended,
                thumb_folded,
                pinky_folded
            ])
            
            if is_screenshot:
                logger.debug("Screenshot gesture detected (index, middle, ring extended)")
                logger.debug(f"Index extended: {index_extended}, Middle extended: {middle_extended}, Ring extended: {ring_extended}")
                logger.debug(f"Thumb folded: {thumb_folded}, Pinky folded: {pinky_folded}")
            
            return is_screenshot
            
        except Exception as e:
            logger.error(f"Error in screenshot gesture detection: {str(e)}")
            return False

    def _is_minimize_gesture(self, landmarks) -> bool:
        """Check if hand is in minimize gesture (both index and middle fingers raised)."""
        try:
            # Check if index and middle fingers are extended
            index_extended = landmarks['index']['tip'].y < landmarks['index']['pip'].y
            middle_extended = landmarks['middle']['tip'].y < landmarks['middle']['pip'].y
            
            # Check if other fingers are folded
            others_folded = all([
                landmarks['ring']['tip'].y > landmarks['middle']['pip'].y,
                landmarks['pinky']['tip'].y > landmarks['middle']['pip'].y
            ])
            
            is_minimize = index_extended and middle_extended and others_folded
            if is_minimize:
                logger.debug("Minimize gesture detected")
                logger.debug(f"Index extended: {index_extended}, Middle extended: {middle_extended}")
                logger.debug(f"Other fingers folded: {others_folded}")
            
            return is_minimize
            
        except Exception as e:
            logger.error(f"Error in minimize gesture detection: {str(e)}")
            return False

    def _is_open_app_gesture(self, landmarks) -> bool:
        """Check if hand is in open application gesture (index, middle, ring fingers extended)."""
        try:
            # Check if index, middle, and ring fingers are extended
            # and thumb and pinky are folded
            is_open_app = all([
                landmarks['index']['tip'].y < landmarks['index']['pip'].y,
                landmarks['middle']['tip'].y < landmarks['middle']['pip'].y,
                landmarks['ring']['tip'].y < landmarks['ring']['pip'].y,
                landmarks['thumb']['tip'].y > landmarks['thumb']['mcp'].y,
                landmarks['pinky']['tip'].y > landmarks['pinky']['pip'].y
            ])
            
            if is_open_app:
                logger.debug("Open application gesture detected")
            
            return is_open_app
            
        except Exception as e:
            logger.error(f"Error in open app gesture detection: {str(e)}")
            return False

    def _is_shutdown_option_gesture(self, landmarks) -> bool:
        """Check if hand is in shutdown option gesture (index and pinky fingers extended)."""
        try:
            # Check if index and pinky fingers are extended
            # and other fingers are folded
            is_shutdown_option = all([
                landmarks['index']['tip'].y < landmarks['index']['pip'].y,
                landmarks['pinky']['tip'].y < landmarks['pinky']['pip'].y,
                landmarks['thumb']['tip'].y > landmarks['thumb']['mcp'].y,
                landmarks['middle']['tip'].y > landmarks['middle']['pip'].y,
                landmarks['ring']['tip'].y > landmarks['ring']['pip'].y
            ])
            
            if is_shutdown_option:
                logger.debug("Shutdown option gesture detected")
            
            return is_shutdown_option
            
        except Exception as e:
            logger.error(f"Error in shutdown option gesture detection: {str(e)}")
            return False

    def _is_confirm_shutdown_gesture(self, landmarks) -> bool:
        """Check if hand is in confirm shutdown gesture (thumb, index, and pinky fingers extended)."""
        try:
            # Check if thumb, index, and pinky fingers are extended
            # and middle and ring fingers are folded
            is_confirm_shutdown = all([
                landmarks['thumb']['tip'].y < landmarks['thumb']['mcp'].y,
                landmarks['index']['tip'].y < landmarks['index']['pip'].y,
                landmarks['pinky']['tip'].y < landmarks['pinky']['pip'].y,
                landmarks['middle']['tip'].y > landmarks['middle']['pip'].y,
                landmarks['ring']['tip'].y > landmarks['ring']['pip'].y
            ])
            
            if is_confirm_shutdown:
                logger.debug("Confirm shutdown gesture detected")
            
            return is_confirm_shutdown
            
        except Exception as e:
            logger.error(f"Error in confirm shutdown gesture detection: {str(e)}")
            return False

    def _is_enter_gesture(self, landmarks) -> bool:
        """Check if hand is in enter gesture (index and middle fingers touching thumb)."""
        try:
            # Get the positions of the finger tips
            thumb_tip = np.array([landmarks['thumb']['tip'].x, landmarks['thumb']['tip'].y])
            index_tip = np.array([landmarks['index']['tip'].x, landmarks['index']['tip'].y])
            middle_tip = np.array([landmarks['middle']['tip'].x, landmarks['middle']['tip'].y])
            
            # Calculate distances between thumb and other fingers
            thumb_index_dist = np.linalg.norm(thumb_tip - index_tip)
            thumb_middle_dist = np.linalg.norm(thumb_tip - middle_tip)
            
            # Check if fingers are touching thumb (within a small threshold)
            is_touching = all([
                thumb_index_dist < 0.1,  # Threshold for touching
                thumb_middle_dist < 0.1
            ])
            
            if is_touching:
                logger.debug("Enter gesture detected (index and middle touching thumb)")
                logger.debug(f"Thumb-Index distance: {thumb_index_dist:.3f}, Thumb-Middle distance: {thumb_middle_dist:.3f}")
            
            return is_touching
            
        except Exception as e:
            logger.error(f"Error in enter gesture detection: {str(e)}")
            return False

    def _analyze_gesture(self, hand_landmarks) -> Dict[str, Any]:
        """Analyze hand landmarks to detect gestures."""
        try:
            # Cache frequently used landmarks
            landmarks = {
                'thumb': {
                    'tip': hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP],
                    'mcp': hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_MCP]
                },
                'index': {
                    'tip': hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP],
                    'pip': hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
                },
                'middle': {
                    'tip': hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                    'pip': hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
                },
                'ring': {
                    'tip': hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP],
                    'pip': hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP]
                },
                'pinky': {
                    'tip': hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP],
                    'pip': hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP]
                }
            }
            
            # Get index finger tip coordinates for cursor control
            cursor_pos = {
                'x': 1 - landmarks['index']['tip'].x,  # Flip x-coordinate
                'y': landmarks['index']['tip'].y
            }
            
            # Check gestures in order of most common to least common
            if self._is_pointing_gesture(landmarks):
                gesture = 'cursor_move'
            elif self._is_click_gesture(landmarks):
                gesture = 'cursor_click'
            elif self._is_scroll_up_gesture(landmarks):
                gesture = 'scroll_up'
            elif self._is_scroll_down_gesture(landmarks):
                gesture = 'scroll_down'
            elif self._is_enter_gesture(landmarks):
                gesture = 'press_enter'
            elif self._is_minimize_gesture(landmarks):
                gesture = 'minimize_window'
            elif self._is_open_app_gesture(landmarks):
                gesture = 'open_application'
            elif self._is_shutdown_option_gesture(landmarks):
                gesture = 'show_shutdown_options'
            elif self._is_confirm_shutdown_gesture(landmarks):
                gesture = 'confirm_shutdown'
            elif self._is_screenshot_gesture(landmarks):
                gesture = 'take_screenshot'
            else:
                gesture = None
                
            if gesture:
                logger.debug(f"Detected gesture: {gesture}")
                return {
                    'gesture': gesture,
                    'cursor_pos': cursor_pos
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"Error analyzing gesture: {str(e)}")
            return {}

    def release(self):
        """Release resources."""
        self.hands.close()
        logger.info("Gesture detector resources released")
        print("Gesture Detector Started")

    def _load_gesture_data(self) -> Dict:
        """Load gesture data from configuration."""
        return {
            'cursor_move': {
                'name': 'Move Cursor',
                'description': 'Point with index finger'
            },
            'cursor_click': {
                'name': 'Click',
                'description': 'Raise index and thumb fingers'
            },
            'scroll_up': {
                'name': 'Scroll Up',
                'description': 'Raise pinky finger'
            },
            'scroll_down': {
                'name': 'Scroll Down',
                'description': 'Raise ring finger'
            },
            'take_screenshot': {
                'name': 'Screenshot',
                'description': 'Extend all five fingers'
            },
            'minimize_window': {
                'name': 'Minimize Window',
                'description': 'Both index and middle fingers raised'
            },
            'open_application': {
                'name': 'Open Application',
                'description': 'Extend index, middle, and ring fingers'
            },
            'show_shutdown_options': {
                'name': 'Show Shutdown Options',
                'description': 'Extend index and little finger'
            },
            'confirm_shutdown': {
                'name': 'Confirm Shutdown',
                'description': 'Extend thumb, index, and little finger'
            },
            'press_enter': {
                'name': 'Press Enter',
                'description': 'All fingers extended'
            }
        }
