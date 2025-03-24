import pytest
from src.gesture_recognition.gesture_mapping import GestureMapping

@pytest.fixture
def gesture_mapping():
    return GestureMapping()

def test_gesture_mapping_initialization(gesture_mapping):
    """Test if gesture mapping initializes with default mappings."""
    assert gesture_mapping is not None
    assert len(gesture_mapping.gesture_commands) > 0

def test_get_command_existing(gesture_mapping):
    """Test getting command for existing gesture."""
    command = gesture_mapping.get_command('thumbs_up')
    assert command == 'confirm'

def test_get_command_nonexistent(gesture_mapping):
    """Test getting command for nonexistent gesture."""
    command = gesture_mapping.get_command('nonexistent_gesture')
    assert command is None

def test_add_mapping(gesture_mapping):
    """Test adding new gesture mapping."""
    gesture_mapping.add_mapping('new_gesture', 'new_command')
    assert gesture_mapping.get_command('new_gesture') == 'new_command'

def test_remove_mapping(gesture_mapping):
    """Test removing gesture mapping."""
    gesture_mapping.remove_mapping('thumbs_up')
    assert gesture_mapping.get_command('thumbs_up') is None 