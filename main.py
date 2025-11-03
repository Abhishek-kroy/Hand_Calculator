import cv2
import time
import mediapipe as mp
from collections import deque

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# ------------------- COUNT FINGERS FUNCTION -------------------
def count_fingers(hand_landmarks, handedness_label):
    """
    Robust and simple finger counting using Mediapipe landmarks.
    Works with flipped (selfie) camera view.
    """
    fingers = []

    # === Thumb ===
    if handedness_label == "Right":
        thumb_is_open = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > \
                        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    else:
        thumb_is_open = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < \
                        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x

    fingers.append(1 if thumb_is_open else 0)

    # === Other 4 Fingers (Index → Pinky) ===
    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP,
    ]
    finger_dips = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP,
    ]

    for tip, pip in zip(finger_tips, finger_dips):
        fingers.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y else 0)

    return sum(fingers), fingers


# ------------------- GESTURE HELPERS -------------------
def is_thumb_up(f, h): return f[0] == 1 and sum(f[1:]) == 0
def is_flat(f, h): return sum(f) == 0
def is_peace_sign(f, h): return f[1] == 1 and f[2] == 1 and f[0] == f[3] == f[4] == 0
def is_open_palm(f, h): return sum(f) >= 4


# ------------------- MAIN -------------------
def main():
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        model_complexity=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )

    stage = 0  # 0=first number, 1=second number, 2=select op, 3=result
    selected_op = None
    first_num = None
    second_num = None
    op_text = ""
    gesture_start_time = 0
    stable_gesture = None
    GESTURE_HOLD_TIME = 0.6
    recent_counts = deque(maxlen=5)

    print("\n=== Finger Calculator Controls ===")
    print("- Show 0–5 fingers to input numbers")
    print("- Press SPACE to capture number (first, then second)")
    print("- Show gesture to choose operation:")
    print("  👍 : Add | 👎 : Subtract | ✌️ : Multiply | 🖐️ : Divide")
    print("- Press '+', '-', '*', '/' on keyboard to choose manually")
    print("- Press 'r' to reset or 'q' to quit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        display_count = None
        gesture_hint = ""

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

            hand = results.multi_hand_landmarks[0]
            handedness_label = results.multi_handedness[0].classification[0].label if results.multi_handedness else "Right"

            cnt, fingers_arr = count_fingers(hand, handedness_label)
            recent_counts.append(cnt)
            display_count = round(sum(recent_counts) / len(recent_counts))

            # Draw bounding box
            x_coords = [lm.x for lm in hand.landmark]
            y_coords = [lm.y for lm in hand.landmark]
            xmin, xmax = min(x_coords), max(x_coords)
            ymin, ymax = min(y_coords), max(y_coords)
            cv2.rectangle(frame,
                          (int(xmin * w) - 20, int(ymin * h) - 20),
                          (int(xmax * w) + 20, int(ymax * h) + 20),
                          (0, 255, 255), 2)

            # ------------------- Gesture Detection -------------------
            if stage == 2:
                detected_gesture = None
                if is_thumb_up(fingers_arr, hand):
                    detected_gesture = "+"
                    op_text = "ADD (thumbs up)"
                elif is_flat(fingers_arr, hand):
                    detected_gesture = "-"
                    op_text = "SUBTRACT (thumbs down)"
                elif is_peace_sign(fingers_arr, hand):
                    detected_gesture = "*"
                    op_text = "MULTIPLY (peace)"
                elif is_open_palm(fingers_arr, hand):
                    detected_gesture = "/"
                    op_text = "DIVIDE (open palm)"
                else:
                    gesture_hint = "Gesture: 👍 Add | 👎 Sub | ✌️ Mul | 🖐️ Div"

                # Debounce gesture
                if detected_gesture:
                    if stable_gesture != detected_gesture:
                        stable_gesture = detected_gesture
                        gesture_start_time = time.time()
                    elif time.time() - gesture_start_time > GESTURE_HOLD_TIME:
                        selected_op = detected_gesture
                        stage = 3
                        print("Gesture confirmed:", selected_op)
                else:
                    stable_gesture = None

        else:
            cv2.putText(frame, "No hand detected. Bring hand in view!", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # ------------------- On-screen Info -------------------
        cv2.putText(frame, f"Stage: {stage} | First: {first_num} | Second: {second_num} | Op: {selected_op or '?'}",
                    (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        if display_count is not None:
            cv2.putText(frame, f"Detected Fingers: {display_count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # ------------------- Stage Prompts -------------------
        if stage == 0:
            cv2.putText(frame, "Stage 1: Show FIRST number (0–5) and press SPACE", (10, h - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        elif stage == 1:
            cv2.putText(frame, f"Stage 2: Show SECOND number (0–5) and press SPACE", (10, h - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"First number: {first_num}", (10, h - 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 0), 2)
        elif stage == 2:
            cv2.putText(frame, "Stage 3: Choose operation (gesture or keyboard)", (10, h - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
            if gesture_hint:
                cv2.putText(frame, gesture_hint, (10, h - 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 2)
            if op_text:
                cv2.putText(frame, f"Selected: {op_text}", (10, h - 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        elif stage == 3:
            # calculate the result
            try:
                if selected_op == "+": res = first_num + second_num
                elif selected_op == "-": res = first_num - second_num
                elif selected_op == "*": res = first_num * second_num
                elif selected_op == "/": res = first_num / second_num if second_num != 0 else "Inf"
                else: res = "No op"
            except Exception as e:
                res = f"Error: {e}"

            cv2.putText(frame, f"{first_num} {selected_op} {second_num} = {res}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
            cv2.putText(frame, "Press 'r' to restart or 'q' to quit", (10, h - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow("Finger Calculator", frame)

        # ------------------- Key Controls -------------------
        key = cv2.waitKey(10) & 0xFF
        if key == 32:  # Space
            if display_count is None:
                print("No hand to capture.")
            else:
                if stage == 0:
                    first_num = display_count
                    stage = 1
                    print("First number saved:", first_num)
                    time.sleep(0.4)
                elif stage == 1:
                    second_num = display_count
                    stage = 1.5
                    print("Second number saved:", second_num)
                elif stage == 1.5:
                    stage = 2
                    print("Proceeding to operation selection...")

        # Handle the temporary "1.5" waiting stage
        if stage == 1.5:
            cv2.putText(frame, "Press SPACE again to choose operation (Stage 3)", (10, h - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        if key in (ord('+'), ord('-'), ord('*'), ord('/')):
            if stage == 2:
                selected_op = chr(key)
                stage = 3
                print("Operator chosen (keyboard):", selected_op)
                time.sleep(2)

        if key == ord('r'):
            stage = 0
            first_num = second_num = selected_op = None
            op_text = ""
            print("Reset.\n")

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()   