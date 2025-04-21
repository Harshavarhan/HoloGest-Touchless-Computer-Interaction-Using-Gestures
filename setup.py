from setuptools import setup, find_packages

setup(
    name="hologest",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'opencv-python>=4.5.0',
        'mediapipe>=0.8.9',
        'PyQt5>=5.15.0',
        'numpy>=1.19.0',
        'pytest>=6.0.0',
        'pytest-qt>=4.0.0',
        'typing-extensions>=4.0.0',
        'pyautogui>=0.9.50',
        'pywin32>=300'
    ],
) 