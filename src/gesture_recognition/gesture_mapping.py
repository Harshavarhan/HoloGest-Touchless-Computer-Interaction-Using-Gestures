import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class GestureMapping:
    def __init__(self):
        """Initialize gesture to command mapping."""
        self.gesture_commands: Dict[str, str] = {
            'swipe_left': 'navigate_back',
            'swipe_right': 'navigate_forward',
            'thumbs_up': 'confirm',
            'thumbs_down': 'cancel',
            'palm_open': 'show_menu',
            'palm_closed': 'hide_menu'
        }
        logger.info("Gesture mapping initialized")

    def get_command(self, gesture: str) -> Optional[str]:
        """
        Map a detected gesture to a system command.
        
        Args:
            gesture: str, detected gesture name
            
        Returns:
            str: corresponding system command or None
        """
        try:
            command = self.gesture_commands.get(gesture)
            if command:
                logger.debug(f"Mapping gesture '{gesture}' to command '{command}'")
            return command
        except Exception as e:
            logger.error(f"Error in gesture mapping: {e}")
            return None

    def add_mapping(self, gesture: str, command: str) -> bool:
        """
        Add a new gesture-to-command mapping.
        
        Args:
            gesture: str, gesture name
            command: str, system command
            
        Returns:
            bool: True if mapping was added successfully
        """
        try:
            self.gesture_commands[gesture] = command
            logger.info(f"Added new mapping: '{gesture}' -> '{command}'")
            return True
        except Exception as e:
            logger.error(f"Error adding gesture mapping: {e}")
            return False

    def remove_mapping(self, gesture: str) -> bool:
        """
        Remove a gesture-to-command mapping.
        
        Args:
            gesture: str, gesture name
            
        Returns:
            bool: True if mapping was removed successfully
        """
        try:
            if gesture in self.gesture_commands:
                del self.gesture_commands[gesture]
                logger.info(f"Removed mapping for gesture: '{gesture}'")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing gesture mapping: {e}")
            return False 