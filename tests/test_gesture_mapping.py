import pytest
from src.gesture_recognition.gesture_mapping import GestureMapping

@pytest.fixture
def gesture_mapping():
    return GestureMapping()

def test_gesture_mapping_initialization(gesture_mapping):
    """Test if gesture mapping initializes with default mappings."""
    assert gesture_mapping is not None
    assert len(gesture_mapping.gesture_commands) > 0
    assert 'thumbs_up' in gesture_mapping.gesture_commands
    assert 'swipe_left' in gesture_mapping.gesture_commands

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
    success = gesture_mapping.add_mapping('new_gesture', 'new_command')
    assert success
    assert gesture_mapping.get_command('new_gesture') == 'new_command'

def test_remove_mapping(gesture_mapping):
    """Test removing gesture mapping."""
    success = gesture_mapping.remove_mapping('thumbs_up')
    assert success
    assert gesture_mapping.get_command('thumbs_up') is None

def test_remove_nonexistent_mapping(gesture_mapping):
    """Test removing nonexistent gesture mapping."""
    success = gesture_mapping.remove_mapping('nonexistent_gesture')
    assert not success 