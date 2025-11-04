# Hand Calculator

The Hand Calculator is an interactive Python application that allows users to perform basic arithmetic operations using hand gestures captured via a webcam. It leverages computer vision techniques to detect and count fingers for inputting numbers (0-5) and recognizes specific hand gestures to select mathematical operations (addition, subtraction, multiplication, division). This project demonstrates the integration of OpenCV for video processing and MediaPipe for real-time hand landmark detection.

The application runs in a loop, guiding the user through stages: capturing the first number, capturing the second number, selecting an operation via gesture or keyboard, and displaying the result. It includes features like gesture debouncing, averaging finger counts for stability, and visual feedback on the screen.

## Features

- **Real-time Hand Detection**: Uses MediaPipe's Hands solution to detect and track hand landmarks in real-time.
- **Finger Counting**: Accurately counts fingers (0-5) based on landmark positions, accounting for left/right hand orientation.
- **Gesture Recognition**: Recognizes specific gestures for operations:
  - Thumbs up: Addition (+)
  - plam down (flat hand): Subtraction (-)
  - Peace sign: Multiplication (*)
  - Open palm: Division (/)
- **Keyboard Fallback**: Allows manual selection of operations using keyboard keys (+, -, *, /).
- **Visual Feedback**: Displays detected fingers, current stage, captured numbers, selected operation, and results on the video feed.
- **Gesture Debouncing**: Implements a hold-time mechanism to confirm gestures and prevent accidental selections.
- **Averaging for Stability**: Uses a deque to average recent finger counts for smoother detection.
- **Bounding Box**: Draws a bounding box around the detected hand for better visualization.
- **Reset and Quit Options**: Easy controls to reset the process or exit the application.
- **Flipped Camera View**: Handles selfie-mode camera flipping for natural interaction.

## Screenshots

### Starting
<p align="center">
  <img width="400" alt="Starting Screen" src="https://github.com/user-attachments/assets/df31bc4f-9b2d-41e2-82b2-789dafe7b09b" />
</p>

---

### ➕ Addition
<p align="center">
  <img width="280" alt="Addition - First Number" src="https://github.com/user-attachments/assets/9fcb399c-4f5d-4328-af0c-a97fcf5e4b8e" />
  <img width="280" alt="Addition - Second Number" src="https://github.com/user-attachments/assets/382aefb0-6903-43b3-a3cb-f7bf7e0a95e3" />
  <img width="280" alt="Addition - Result" src="https://github.com/user-attachments/assets/bffff7b0-8e4d-4bd6-8a2c-5e20f48545bc" />
</p>

---

### ➖ Subtraction
<p align="center">
  <img width="280" alt="Subtraction Step 1" src="https://github.com/user-attachments/assets/25faea46-e668-495e-922b-821c1c1da4ae" />
  <img width="280" alt="Subtraction Step 2" src="https://github.com/user-attachments/assets/6546535e-2870-4650-956f-b56b3b558eb0" />
  <img width="280" alt="Subtraction Result" src="https://github.com/user-attachments/assets/0657954b-9822-40cb-8375-bdede8b66566" />
</p>

---

### ✖️ Multiplication
<p align="center">
  <img width="280" alt="Multiplication Step 1" src="https://github.com/user-attachments/assets/66f1b8ee-0407-47b7-a0c4-134e03be9e2f" />
  <img width="280" alt="Multiplication Step 2" src="https://github.com/user-attachments/assets/97d48555-4d23-450f-8d67-c7a1ee118c08" />
  <img width="280" alt="Multiplication Result" src="https://github.com/user-attachments/assets/094dbb3e-aacd-47f7-bff1-581b90863957" />
</p>

---

### ➗ Division
<p align="center">
  <img width="280" alt="Division Step 1" src="https://github.com/user-attachments/assets/ff07ca39-7784-413a-bc51-e6450e29714f" />
  <img width="280" alt="Division Step 2" src="https://github.com/user-attachments/assets/3bd64cb7-fe49-4c8e-93b2-20465557e1e7" />
  <img width="280" alt="Division Result" src="https://github.com/user-attachments/assets/4f2915c4-9220-46a2-a0e3-24f323074bcb" />
</p>

---

> 🧭 **Controls:**  
> Press `q` → Quit the calculator  
> Press `r` → Restart the operation 

## Requirements

### Hardware
- A webcam (built-in or external) capable of capturing video at reasonable resolution.

### Software
- **Python 3.7+**: The application is written in Python.
- **OpenCV (cv2)**: For video capture, image processing, and display.
- **MediaPipe**: For hand detection and landmark extraction.
- **NumPy**: Implicitly used by MediaPipe and OpenCV.
- **Collections (deque)**: Standard library module for averaging.

### Dependencies
Install the required packages using pip:
```
pip install opencv-python mediapipe
```

## Installation

1. **Clone or Download the Repository**:
   - Ensure you have the `main.py` file in your project directory.

2. **Install Python**:
   - Download and install Python from [python.org](https://www.python.org/) if not already installed.

3. **Install Dependencies**:
   - Open a terminal or command prompt.
   - Navigate to the project directory (e.g., `cd c:/Users/Abhishek Kumar Roy/PycharmProjects/opencv_calculator`).
   - Run the following command:
     ```
     pip install opencv-python mediapipe
     ```

4. **Verify Installation**:
   - Run the script to ensure everything is set up correctly:
     ```
     python main.py
     ```
   - If the webcam feed opens without errors, the installation is successful.

## Usage

1. **Run the Application**:
   - Execute the script:
     ```
     python main.py
     ```
   - The application will start, open a window titled "Finger Calculator", and begin capturing video from your webcam.

2. **Follow On-Screen Instructions**:
   - The application guides you through stages displayed at the bottom of the video feed.

3. **Input Numbers**:
   - Show 0-5 fingers to the camera.
   - Press the SPACE key to capture the first number, then the second number.

4. **Select Operation**:
   - Use hand gestures or press keyboard keys (+, -, *, /) to choose the operation.

5. **View Result**:
   - The result of the calculation will be displayed on the screen.

6. **Reset or Quit**:
   - Press 'r' to reset and start over.
   - Press 'q' to quit the application.

## Controls

### Keyboard Controls
- **SPACE**: Capture the current finger count as a number (first, then second).
- **+**: Select addition.
- **-**: Select subtraction.
- *** (asterisk)**: Select multiplication.
- **/**: Select division.
- **r**: Reset the process (clear numbers and operation).
- **q**: Quit the application.

### Gesture Controls
- **Thumbs Up (👍)**: Addition (+). Thumb extended, other fingers folded.
- **Plam Down (🫲)**: Subtraction (-). All fingers folded (flat hand).
- **Peace Sign (✌️)**: Multiplication (*). Index and middle fingers extended, others folded.
- **Open Palm (🖐️)**: Division (/). All fingers extended.

### Gesture Requirements
- Gestures must be held for approximately 0.6 seconds to be confirmed (debouncing).
- The application detects the dominant hand (left or right) and adjusts thumb detection accordingly.

## How It Works

### Finger Counting Algorithm
- **Thumb**: Compares the x-coordinate of the thumb tip and IP joint. For right hand, tip > IP means open; for left hand, tip < IP.
- **Other Fingers**: Compares y-coordinates of finger tips and PIP joints. Tip above PIP means open.

### Gesture Detection
- Specific combinations of finger states are checked against predefined patterns.

### Stages
1. **Stage 0**: Capture first number.
2. **Stage 1**: Capture second number.
3. **Stage 1.5**: Confirmation step (press SPACE again).
4. **Stage 2**: Select operation.
5. **Stage 3**: Display result.

### Averaging
- Maintains a deque of the last 5 finger counts and averages them for stability.

### Error Handling
- Handles division by zero by displaying "Inf".
- Catches exceptions during calculation and displays error messages.

## Troubleshooting

- **No Hand Detected**: Ensure good lighting, bring hand closer to the camera, and avoid occlusions.
- **Inaccurate Finger Counting**: Adjust camera angle, ensure fingers are clearly visible, and check for hand orientation.
- **Gesture Not Recognized**: Hold gestures steady for the debounce time, ensure correct finger positions.
- **Camera Issues**: Check webcam permissions, try a different camera index in `cv2.VideoCapture(0)`.
- **Performance**: Lower `model_complexity` in MediaPipe Hands if running on low-end hardware.
