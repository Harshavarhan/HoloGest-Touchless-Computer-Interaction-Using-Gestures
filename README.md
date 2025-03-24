# HoloGest - Touchless Computer Interaction Using Gestures

A sophisticated system enabling touchless interaction with computers through specific hand gestures for designated operations. This project provides a natural and intuitive way to control your computer without physical contact.

## Overview

HoloGest is a Python-based application that uses computer vision and machine learning to detect and interpret hand gestures, translating them into computer commands. The system is designed to be user-friendly while providing powerful functionality for touchless computer interaction.

## Project Structure

```
HoloGest/
│
├── docs/
│   ├── user_manual.md          # User manual for the application
│   ├── technical_specifications.md # Technical specifications and requirements
│   └── design_document.md       # Design document outlining the architecture and components
│
├── src/
│   ├── main.py                 # Main application file
│   ├── gesture_recognition/    # Core gesture recognition functionality
│   ├── ui/                     # User interface components
│   ├── utils/                  # Utility functions and helpers
│   └── scripts/                # System scripts and batch files
│
├── tests/                      # Unit tests for all components
├── requirements.txt            # Project dependencies
└── LICENSE                     # Project license
```

## Features

- Real-time hand gesture recognition
- Customizable gesture mapping
- User-friendly interface
- System control commands (e.g., shutdown)
- Comprehensive documentation
- Extensive test coverage

## Prerequisites

- Python 3.8 or higher
- OpenCV
- MediaPipe
- PyQt5 (for the user interface)
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/HoloGest-Touchless-Computer-Interaction-Using-Gestures.git
cd HoloGest-Touchless-Computer-Interaction-Using-Gestures
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python src/main.py
```

2. Follow the on-screen instructions to calibrate your camera and set up gesture recognition.

3. Use the predefined gestures to interact with your computer:
   - Swipe left/right for navigation
   - Thumbs up for confirmation
   - Thumbs down for cancellation
   - (Additional gestures documented in user_manual.md)

## Documentation

- [User Manual](docs/user_manual.md) - Detailed instructions for using the application
- [Technical Specifications](docs/technical_specifications.md) - System requirements and technical details
- [Design Document](docs/design_document.md) - Architecture and component design

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV for computer vision capabilities
- MediaPipe for hand tracking
- PyQt5 for the user interface
- All contributors and maintainers

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
