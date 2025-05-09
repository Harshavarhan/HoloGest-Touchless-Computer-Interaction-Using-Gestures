"""
Utility Package

This package contains helper functions and utilities.
"""

from .helpers import setup_logging
from .shutdown import shutdown_system
from .camera_manager import CameraManager

__all__ = ['setup_logging', 'shutdown_system', 'CameraManager'] 