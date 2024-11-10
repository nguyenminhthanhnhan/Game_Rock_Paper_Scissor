import bluetooth
import time
import cv2
import mediapipe as mp

hc05_mac_address = "98:DA:60:0A:13:25"  # Replace by the real address of HC05 device
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1  # Default gateway RFCOMM of module HC-05 is 1
sock.connect((hc05_mac_address, port))

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize MediaPipe Hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize camera
cap = cv2.VideoCapture(0)

def get_hand_state(landmarks):
    # Check the state of fingers 
    finger_states = []  # Initialize an empty list
    wrist_x = landmarks[0].x
    left_hand = wrist_x > landmarks[4].x
    right_hand = wrist_x < landmarks[4].x
    for finger_tip in [4, 8, 12, 16, 20]:  # Thumb finger, Index finger, Middle finger, Ring finger, Pinky finger
        if finger_tip == 4:
            if left_hand:
                state = '1' if landmarks[finger_tip].x < landmarks[finger_tip - 1].x else '0'
            elif right_hand:
                state = '1' if landmarks[finger_tip].x > landmarks[finger_tip - 1].x else '0'
        else:
            state = '1' if landmarks[finger_tip].y < landmarks[finger_tip - 2].y else '0'
        finger_states.append(state)  # Append the state to the list
    return '*'.join(finger_states) + '#'

try:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Convert the image to RGB
        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        # Process the image with MediaPipe Hands
        results = hands.process(rgb_frame)
    
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get hand state and then send by Bluetooth
            hand_state = get_hand_state(results.multi_hand_landmarks[0].landmark)
            sock.send(hand_state.encode())
            print(f"Sent: {hand_state}")
        else:
            # Display notification "No hand detected"
            cv2.putText(image, "No hand detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the image
        cv2.imshow('Hand Tracking', image)
        
        key = cv2.waitKey(1)
        if key == ord('q'): #Press 'q' to exit
            break

        time.sleep(0.1)  

finally:
    cap.release()
    hands.close()
    sock.close()
