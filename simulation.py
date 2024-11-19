import bluetooth
import time
import cv2
import mediapipe as mp
import pygame  # Add this import for audio playback

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

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Load the audio file
audio_file_path = "Audio/simulation/simulation.mp3"  # Replace with your actual audio file path
pygame.mixer.music.load(audio_file_path)

last_played_time = 0  # Initialize a variable to track the last play time

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

            # Determine which hand is detected
            wrist_x = results.multi_hand_landmarks[0].landmark[0].x
            hand_label = "Left hand" if wrist_x > results.multi_hand_landmarks[0].landmark[4].x else "Right hand"
            cv2.putText(image, hand_label, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Get hand state and then send by Bluetooth
            hand_state = get_hand_state(results.multi_hand_landmarks[0].landmark)
            # Record the start time before sending
            start_time = time.time()
            sock.send(hand_state.encode())
            print(f"Sent: {hand_state}")

            # Record the completion time
            # Calculate the time taken to send the command
            completion_time = time.time() - start_time  # Time taken to send
            print(f"Command sent in: {completion_time:.6f} seconds")

        else:
            current_time = time.time()  # Get the current time
            if current_time - last_played_time >= 7:  # Check if 7 seconds have passed
                pygame.mixer.music.play()  # Play the audio if a finger is missing or blurred
                last_played_time = current_time  # Update the last played time
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

    