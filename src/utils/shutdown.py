import os
import platform
import subprocess
import logging

logger = logging.getLogger(__name__)

def shutdown_system():
    """
    Shutdown the system safely.
    
    Returns:
        bool: True if shutdown command was successful, False otherwise
    """
    try:
        system = platform.system().lower()
        
        if system == 'windows':
            subprocess.run(['shutdown', '/s', '/t', '0'], check=True)
        elif system == 'linux':
            subprocess.run(['shutdown', '-h', 'now'], check=True)
        elif system == 'darwin':  # macOS
            subprocess.run(['shutdown', '-h', 'now'], check=True)
        else:
            logger.error(f"Unsupported operating system: {system}")
            return False
            
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to shutdown system: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during shutdown: {e}")
        return False 