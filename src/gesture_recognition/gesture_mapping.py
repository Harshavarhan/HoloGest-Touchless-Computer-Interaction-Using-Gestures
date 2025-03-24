class GestureMapping:
    def __init__(self):
        self.gesture_commands = {
            'swipe_left': 'navigate_back',
            'swipe_right': 'navigate_forward',
            'thumbs_up': 'confirm',
            'thumbs_down': 'cancel',
            'palm_open': 'show_menu',
            'palm_closed': 'hide_menu'
        }

    def get_command(self, gesture):
        """
        Map a detected gesture to a system command.
        
        Args:
            gesture: str, detected gesture name
            
        Returns:
            str: corresponding system command or None
        """
        return self.gesture_commands.get(gesture)

    def add_mapping(self, gesture, command):
        """
        Add a new gesture-to-command mapping.
        
        Args:
            gesture: str, gesture name
            command: str, system command
        """
        self.gesture_commands[gesture] = command

    def remove_mapping(self, gesture):
        """
        Remove a gesture-to-command mapping.
        
        Args:
            gesture: str, gesture name
        """
        if gesture in self.gesture_commands:
            del self.gesture_commands[gesture] 