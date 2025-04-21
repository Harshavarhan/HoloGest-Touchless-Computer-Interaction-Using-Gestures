# test_gesture_detector.py
import cv2
from gesture_detector import GestureDetector

detector = GestureDetector()
cap = cv2.VideoCapture(0)  # Open webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame, gesture = detector.detect_gestures(frame)

    if gesture:
        print(f"Gesture Detected: {gesture}")

    cv2.imshow("Gesture Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
detector.release()
cv2.destroyAllWindows()
