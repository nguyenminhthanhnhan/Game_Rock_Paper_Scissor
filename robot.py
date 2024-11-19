import bluetooth
import time
import cv2
import cvzone
from keras.models import load_model
import mediapipe as mp
import numpy as np
from random import choice
import pygame

# Constants for text display
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (0, 0, 255)
FONT_SCALE = 1
FONT_THICKNESS = 2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load model
model = load_model("model/robot_model1.h5")

timer = 4 #time to coutdown
stateResult = False 
startGame = False #Game sate
scores = [0, 0]  # Robot score, Player score
tie = 0

# round of game
current_round = 0
selected_round_limit = None
# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

REV_CLASS_MAP = {
    0: "rock",
    1: "paper",
    2: "scissors"
}

play_again_audio = [
    "Audio/play_again/play_again1.mp3",
    "Audio/play_again/play_again2.mp3",
    "Audio/play_again/play_again3.mp3"
]

three_turns_audio = [
    "Audio/select_turns/total_rounds/3turns/audio1.mp3",
    "Audio/select_turns/total_rounds/3turns/audio2.mp3",
    "Audio/select_turns/total_rounds/3turns/audio3.mp3"
]

five_turns_audio = [
    "Audio/select_turns/total_rounds/5turns/audio1.mp3",
    "Audio/select_turns/total_rounds/5turns/audio2.mp3",
    "Audio/select_turns/total_rounds/5turns/audio3.mp3"
]

seven_turns_audio = [
    "Audio/select_turns/total_rounds/7turns/audio1.mp3",
    "Audio/select_turns/total_rounds/7turns/audio2.mp3",
    "Audio/select_turns/total_rounds/7turns/audio3.mp3"
]

user_win_audio = [
    "Audio/result_game/user_win/user_win1.mp3",
    "Audio/result_game/user_win/user_win2.mp3",
    "Audio/result_game/user_win/user_win3.mp3"
]

robot_win_audio = [
    "Audio/result_game/robot_win/robot_win1.mp3",
    "Audio/result_game/robot_win/robot_win2.mp3",
    "Audio/result_game/robot_win/robot_win3.mp3"
]

tie_audio = [
    "Audio/result_game/tie/tie1.mp3",
    "Audio/result_game/tie/tie2.mp3",
    "Audio/result_game/tie/tie3.mp3"
]
# audio when user win the round
audio_Ruser_win_Srobot = [
    "Audio/result_rounds/user_win/rock_win_scissor/rock_win_scissor1.mp3",
    "Audio/result_rounds/user_win/rock_win_scissor/rock_win_scissor2.mp3",
    "Audio/result_rounds/user_win/rock_win_scissor/rock_win_scissor3.mp3"
]
audio_Suser_win_Probot = [
    "Audio/result_rounds/user_win/scissor_win_paper/scissor_win_paper1.mp3",
    "Audio/result_rounds/user_win/scissor_win_paper/scissor_win_paper2.mp3",
    "Audio/result_rounds/user_win/scissor_win_paper/scissor_win_paper3.mp3"
]
audio_Puser_win_Rrobot = [
    "Audio/result_rounds/user_win/paper_win_rock/paper_win_rock1.mp3",
    "Audio/result_rounds/user_win/paper_win_rock/paper_win_rock2.mp3",
    "Audio/result_rounds/user_win/paper_win_rock/paper_win_rock3.mp3"
]
# audio when robot win the round
audio_Rrobot_win_Suser = [
    "Audio/result_rounds/robot_win/rock_win_scissor/rock_win_scissor1.mp3",
    "Audio/result_rounds/robot_win/rock_win_scissor/rock_win_scissor2.mp3",
    "Audio/result_rounds/robot_win/rock_win_scissor/rock_win_scissor3.mp3"
]
audio_Srobot_win_Puser = [
    "Audio/result_rounds/robot_win/scissor_win_paper/scissor_win_paper1.mp3",
    "Audio/result_rounds/robot_win/scissor_win_paper/scissor_win_paper2.mp3",
    "Audio/result_rounds/robot_win/scissor_win_paper/scissor_win_paper3.mp3"
]
audio_Probot_win_Ruser = [
    "Audio/result_rounds/robot_win/paper_win_rock/paper_win_rock1.mp3",
    "Audio/result_rounds/robot_win/paper_win_rock/paper_win_rock2.mp3",
    "Audio/result_rounds/robot_win/paper_win_rock/paper_win_rock3.mp3"
]
# audio when the round is tie
audio_Ptie = [
    "Audio/result_rounds/tie/paper_tie/paper_tie1.mp3",
    "Audio/result_rounds/tie/paper_tie/paper_tie2.mp3",
    "Audio/result_rounds/tie/paper_tie/paper_tie3.mp3"
]
audio_Rtie = [
    "Audio/result_rounds/tie/rock_tie/rock_tie1.mp3",
    "Audio/result_rounds/tie/rock_tie/rock_tie2.mp3",
    "Audio/result_rounds/tie/rock_tie/rock_tie3.mp3"
]
audio_Stie = [
    "Audio/result_rounds/tie/scissor_tie/scissor_tie1.mp3",
    "Audio/result_rounds/tie/scissor_tie/scissor_tie2.mp3",
    "Audio/result_rounds/tie/scissor_tie/scissor_tie3.mp3"
]
# audio for current round
audio_thirdR_of_Three = [
    "Audio/select_turns/round_of_total/three_rounds/third_round/win_1round/win_1round1.mp3",
    "Audio/select_turns/round_of_total/three_rounds/third_round/win_1round/win_1round2.mp3"
]
audio_TFround_of_Five_lose = [
    "Audio/select_turns/round_of_total/five_rounds/third_fouth/lose/lose1.mp3",
    "Audio/select_turns/round_of_total/five_rounds/third_fouth/lose/lose2.mp3",
    "Audio/select_turns/round_of_total/five_rounds/third_fouth/lose/lose3.mp3"
]
audio_TFround_of_Five_win = [
    "Audio/select_turns/round_of_total/five_rounds/third_fouth/win/win1.mp3",
    "Audio/select_turns/round_of_total/five_rounds/third_fouth/win/win2.mp3",
    "Audio/select_turns/round_of_total/five_rounds/third_fouth/win/win3.mp3"
]
audio_TFround_of_Five_tie = [
    "Audio/select_turns/round_of_total/five_rounds/third_fouth/tie/tie1.mp3",
    "Audio/select_turns/round_of_total/five_rounds/third_fouth/tie/tie2.mp3",
    "Audio/select_turns/round_of_total/five_rounds/third_fouth/tie/tie3.mp3"
]
audio_FFSrounds_of_Seven_lose = [
    "Audio/select_turns/round_of_total/seven_rounds/fouth_fiveth_sixth/lose/lose1.mp3",
    "Audio/select_turns/round_of_total/seven_rounds/fouth_fiveth_sixth/lose/lose2.mp3",
    "Audio/select_turns/round_of_total/seven_rounds/fouth_fiveth_sixth/lose/lose3.mp3"
]
audio_FFSrounds_of_Seven_win = [
    "Audio/select_turns/round_of_total/seven_rounds/fouth_fiveth_sixth/win/win1.mp3",
    "Audio/select_turns/round_of_total/seven_rounds/fouth_fiveth_sixth/win/win2.mp3",
    "Audio/select_turns/round_of_total/seven_rounds/fouth_fiveth_sixth/win/win3.mp3"
]
audio_FFSrounds_of_Seven_tie = [
    "Audio/select_turns/round_of_total/seven_rounds/fouth_fiveth_sixth/tie/tie1.mp3",
    "Audio/select_turns/round_of_total/seven_rounds/fouth_fiveth_sixth/tie/tie2.mp3",
    "Audio/select_turns/round_of_total/seven_rounds/fouth_fiveth_sixth/tie/tie3.mp3"
]
audio_Frounds_of_Seven_lose = [
    "Audio/select_turns/round_of_total/seven_rounds/final/lose/lose1.mp3",
    "Audio/select_turns/round_of_total/seven_rounds/final/lose/lose2.mp3"
]
audio_Frounds_of_Seven_win = [
    "Audio/select_turns/round_of_total/seven_rounds/final/win/win1.mp3",
    "Audio/select_turns/round_of_total/seven_rounds/final/win/win2.mp3"
]
audio_Frounds_of_Seven_tie = [
    "Audio/select_turns/round_of_total/seven_rounds/final/tie/tie1.mp3",
    "Audio/select_turns/round_of_total/seven_rounds/final/tie/tie2.mp3"
]
# Information of Robot hand 
hc05_mac_address = "98:DA:60:0A:13:25"
gestures = {"scissors": "0*1*1*0*0#", "rock": "0*0*0*0*0#", "paper": "1*1*1*1*1#"}
prev_move = None

# Create Bluetooth socket once
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((hc05_mac_address, port))

# Initialize pygame mixer
pygame.mixer.init()

# Function to play sound
def play_sound(sound_file):
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy():  # Wait for the sound to finish playing
        #     pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Send gesture to HC05 by Bluetooth or display notification if error
def send_gesture(gesture):
    try:
        sock.send(gesture)
        return True
    except bluetooth.btcommon.BluetoothError as e:
        print(f"Bluetooth error: {e}")
        return False

# Choice the gesture for Robot hand
def send_robot_move(user_move_name):
    robot_move_name = choice(['rock', 'paper', 'scissors'])
    send_gesture(gestures[robot_move_name])
    return robot_move_name

# Get name of the gesture user move
def mapper(val):
    return REV_CLASS_MAP[val]

# Calculate the winner between user and Robot
def calculate_winner(user_move, robot_move):
    outcomes = {
        ("rock", "scissors"): "You win",
        ("scissors", "paper"): "You win",
        ("paper", "rock"): "You win",
    }
    if user_move == robot_move:
        return "Tie"
    return outcomes.get((user_move, robot_move), "Robot wins")

# Reset the game if play again
def reset_game():
    global current_round, scores, startGame, stateResult, selected_round_limit, tie, prev_move
    current_round = 0
    scores = [0, 0]
    tie = 0
    startGame = False  # Ensure the game state is reset
    stateResult = False  # Ensure the result state is reset
    selected_round_limit = None  # Reset the selected round limit
    prev_move = None

# The button to play again 
play_again_button = (34, 711, 171, 57)
# The button to close the game
close_button = (896, 711, 171, 57)

# Check the state when click the button
def is_button_clicked(x, y, button_position):
    x_min, y_min, width, height = button_position
    return x_min <= x <= x_min + width and y_min <= y <= y_min + height

# Click the button
def mouse_callback(event, x, y, flags, param):
    global startGame, stateResult, selected_round_limit
    if event == cv2.EVENT_LBUTTONDOWN:
        if is_button_clicked(x, y, play_again_button):
            reset_game()  # Ensure the game state is reset
            random_audio = choice(play_again_audio)  # Choose 1 in 3 audio files
            play_sound(random_audio)  # Use the new play_sound function
            print("Play Again button clicked - Game Reset")
            return  # Prevent further processing after reset
        elif is_button_clicked(x, y, close_button):
            print("Close button clicked - Exiting game")
            cap.release()
            cv2.destroyAllWindows()
            exit()
        if selected_round_limit is None:
            if is_button_clicked(x, y, (570, 175, 120, 45)):
                selected_round_limit = 3
                random_audio = choice(three_turns_audio)  # Choose 1 in 3 audio files
                play_sound(random_audio)  # Use the new play_sound function
                print("Selected 3 turns")
            elif is_button_clicked(x, y, (770, 175, 120, 45)):
                selected_round_limit = 5
                random_audio = choice(five_turns_audio)  # Choose 1 in 3 audio files
                play_sound(random_audio)  # Use the new play_sound function
                print("Selected 5 turns")
            elif is_button_clicked(x, y, (970, 175, 120, 45)):
                selected_round_limit = 7
                random_audio = choice(seven_turns_audio)  # Choose 1 in 3 audio files
                play_sound(random_audio)  # Use the new play_sound function
                print("Selected 7 turns")
                
BUTTON_COLOR = (100, 150, 255)  # Blue for 3 Turns button
# Display the rounds of game: three choices
def display_turn_selection(imgBG):
    # Draw background rectangles for each button
    cv2.rectangle(imgBG, (550, 160), (670, 210), BUTTON_COLOR, -1)  # Background for "3 Turns"
    cv2.rectangle(imgBG, (750, 160), (870, 210), BUTTON_COLOR, -1)  # Background for "5 Turns"
    cv2.rectangle(imgBG, (950, 160), (1070, 210), BUTTON_COLOR, -1) # Background for "7 Turns"

    cv2.putText(imgBG, "Select Number of Turns:", (70, 195), FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
    cv2.putText(imgBG, "3 Turns", (550, 195), FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
    cv2.putText(imgBG, "5 Turns", (750, 195), FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)
    cv2.putText(imgBG, "7 Turns", (950, 195), FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)

cv2.namedWindow("BG")
cv2.setMouseCallback("BG", mouse_callback)

# The main loop
while True:
    imgBG = cv2.imread("Resources/BG.png")
    
    if selected_round_limit is None:
        display_turn_selection(imgBG)
    else:
        if current_round > selected_round_limit:
            if scores[1] > scores[0]:
                random_audio = choice(user_win_audio)  # Choose 1 in 3 audio files
                play_sound(random_audio)  # Use the new play_sound function
                winner_message = "Congratulations! You Win!"
            elif scores[0] > scores[1]:
                random_audio = choice(robot_win_audio)  # Choose 1 in 3 audio files
                play_sound(random_audio)  # Use the new play_sound function
                winner_message = "Robot Wins! Better Luck Next Time!"
            else:
                random_audio = choice(tie_audio)  # Choose 1 in 3 audio files
                play_sound(random_audio)  # Use the new play_sound function
                winner_message = "It's a Tie!"

            # Calculate the text size and position for centering
            text_size = cv2.getTextSize(winner_message, cv2.FONT_HERSHEY_PLAIN, 3, 4)[0]
            text_x = (imgBG.shape[1] - text_size[0]) // 2
            text_y = 400  # Fixed y position
            
            cv2.putText(imgBG, winner_message, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
            cv2.putText(imgBG, f"Final Score: You {scores[1]} - {scores[0]} Robot", (200, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            cv2.imshow("BG", imgBG)

            while True:
                key = cv2.waitKey(1)
                if key != -1:  # If any key is pressed, break the loop
                    break

    success, img = cap.read()
    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # Draw the landmark on image 
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if startGame and not stateResult:
            timer = 4 - (time.time() - initialTime)
            cv2.putText(imgBG, str(int(timer)), (520, 535), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
            
            if timer <= 1:
                stateResult = True
                timer = 4
                # current_round += 1
                roi = cv2.resize(img, (224, 224))
                img_for_model = roi / 255.0
                pred = model.predict(np.expand_dims(img_for_model, axis=0))
                move_code = np.argmax(pred[0])
                user_move_name = mapper(move_code)

                cv2.putText(img, f"Gesture: {user_move_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                if prev_move != user_move_name:
                    robot_move_name = send_robot_move(user_move_name)
                    winner = calculate_winner(user_move_name, robot_move_name)
                    if winner == "You win":
                        # Play audio if user plays scissors and robot plays paper
                        if user_move_name == "scissors" and robot_move_name == "paper":
                            random_audio = choice(audio_Suser_win_Probot)  # Choose 1 in 3 audio files
                            play_sound(random_audio)  # Play the sound
                        elif user_move_name == "paper" and robot_move_name == "rock":
                            random_audio = choice(audio_Puser_win_Rrobot)  # Choose 1 in 3 audio files
                            play_sound(random_audio)  # Play the sound
                        elif user_move_name == "rock" and robot_move_name == "scissors":
                            random_audio = choice(audio_Ruser_win_Srobot)  # Choose 1 in 3 audio files
                            play_sound(random_audio)  # Play the sound
                        # increase scores of user
                        scores[1] += 1
                    elif winner == "Robot wins":
                        # Play audio if user plays paper and robot plays scissors
                        if user_move_name == "paper" and robot_move_name == "scissors":
                            random_audio = choice(audio_Srobot_win_Puser)  # Choose 1 in 3 audio files
                            play_sound(random_audio)  # Play the sound
                        elif user_move_name == "scissors" and robot_move_name == "rock":
                            random_audio = choice(audio_Rrobot_win_Suser)  # Choose 1 in 3 audio files
                            play_sound(random_audio)  # Play the sound
                        elif user_move_name == "rock" and robot_move_name == "paper":
                            random_audio = choice(audio_Probot_win_Ruser)  # Choose 1 in 3 audio files
                            play_sound(random_audio)  # Play the sound
                        # increase scores of robot
                        scores[0] += 1
                    elif winner == "Tie":
                        # Play audio if both play scissors
                        if user_move_name == "scissors" and robot_move_name == "scissors":
                            random_audio = choice(audio_Stie)  # Choose 1 in 3 audio files
                            play_sound(random_audio)  # Play the sound
                        if user_move_name == "paper" and robot_move_name == "paper":
                            random_audio = choice(audio_Ptie)  # Choose 1 in 3 audio files
                            play_sound(random_audio)  # Play the sound
                        if user_move_name == "rock" and robot_move_name == "rock":
                            random_audio = choice(audio_Rtie)  # Choose 1 in 3 audio files
                            play_sound(random_audio)  # Play the sound
                        # increase scores of tie
                        tie += 1

                    imgRB = cv2.imread(f'Resources/{robot_move_name}.png', cv2.IMREAD_UNCHANGED)
                    if imgRB.shape[2] == 3:
                        imgRB = cv2.cvtColor(imgRB, cv2.COLOR_BGR2BGRA)
                    imgBG = cvzone.overlayPNG(imgBG, imgRB, (72, 350))
                    prev_move = user_move_name
                else:
                    pygame.mixer.music.load("Audio/repeat/repeat.mp3")
                    pygame.mixer.music.play()
                    if winner == "You win":
                        scores[1] += 1
                    elif winner == 'Robot wins':
                        scores[0] += 1
                    else:
                        tie += 1

    imgScaled = cv2.resize(img, (311, 396))
    imgBG[304:700, 704:1015] = imgScaled

    # Display the rock, paper, or scissors icon of Robot hand
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgRB, (72, 350))

    cv2.putText(imgBG, str(scores[0]), (310, 296), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (950, 296), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(tie), (587, 296), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, f"Round: {current_round}/{selected_round_limit}", (10, 50), FONT, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)

    # Display the window
    cv2.imshow("BG", imgBG)

    # Press 'p' to start each round
    key = cv2.waitKey(1)
    if key == ord('p') and selected_round_limit is not None:
        if current_round <= selected_round_limit:
            current_round += 1
            print(f"Round {current_round}/{selected_round_limit}")
            stateResult = False
            startGame = False  # Reset the game state for the new round
            if selected_round_limit == 3:
                if current_round == 1:
                    pygame.mixer.music.load("Audio/select_turns/round_of_total/three_rounds/first_round/first_round.mp3")
                    pygame.mixer.music.play()
                elif current_round == 2:
                    if scores[1] == 1:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/three_rounds/second_round/win_round1/win_round1.mp3")
                        pygame.mixer.music.play()
                    elif scores[1] == 0 and scores[0] == 1:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/three_rounds/second_round/lose_round1/lose_round1.mp3")
                        pygame.mixer.music.play()
                    elif scores[1] == scores[0]:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/three_rounds/second_round/tie_round1/tie_round1.mp3")
                        pygame.mixer.music.play()
                elif current_round == 3:
                    if scores[1] == 0:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/three_rounds/third_round/win_0round/win_0round.mp3")
                        pygame.mixer.music.play()
                    elif scores[1] == 1:
                        random_audio = choice(audio_thirdR_of_Three)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
                    elif scores[1] == 2:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/three_rounds/third_round/win_2round/win_2round.mp3")
                        pygame.mixer.music.play()
            elif selected_round_limit == 5:
                if current_round == 1:
                    pygame.mixer.music.load("Audio/select_turns/round_of_total/five_rounds/first/first.mp3")
                    pygame.mixer.music.play()
                elif current_round == 2:
                    if scores[1] == 1:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/five_rounds/second/win/win.mp3")
                        pygame.mixer.music.play()
                    elif scores[0] == 1:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/five_rounds/second/lose/lose.mp3")
                        pygame.mixer.music.play()
                    elif scores[1] == scores[0]:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/five_rounds/second/tie/tie.mp3")
                        pygame.mixer.music.play()
                elif (current_round == 3) or (current_round == 4):
                    if scores[1] > scores[0]:
                        random_audio = choice(audio_TFround_of_Five_win)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
                    elif scores[1] < scores[0]:
                        random_audio = choice(audio_TFround_of_Five_lose)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
                    else:
                        random_audio = choice(audio_TFround_of_Five_tie)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
                elif current_round == 5:
                        if scores[1] > scores[0]:
                            pygame.mixer.music.load("Audio/select_turns/round_of_total/five_rounds/final/win/win.mp3")
                            pygame.mixer.music.play()
                        elif scores[1] < scores[0]:
                            pygame.mixer.music.load("Audio/select_turns/round_of_total/five_rounds/final/lose/lose.mp3")
                            pygame.mixer.music.play()
                        else:
                            pygame.mixer.music.load("Audio/select_turns/round_of_total/five_rounds/final/tie/tie.mp3")
                            pygame.mixer.music.play()
            elif selected_round_limit == 7:
                if current_round == 1:
                    pygame.mixer.music.load("Audio/select_turns/round_of_total/seven_rounds/first/first.mp3")
                    pygame.mixer.music.play()
                elif current_round == 2:
                    if scores[1] == 1:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/seven_rounds/second/win/win.mp3")
                        pygame.mixer.music.play()
                    elif scores[0] == 1:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/seven_rounds/second/lose/lose.mp3")
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/seven_rounds/second/tie/tie.mp3")
                        pygame.mixer.music.play()
                elif current_round == 3:
                    if scores[1] > scores[0]:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/seven_rounds/third/win/win.mp3")
                        pygame.mixer.music.play()
                    elif scores[1] < scores[0]:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/seven_rounds/third/lose/lose.mp3")
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load("Audio/select_turns/round_of_total/seven_rounds/third/tie/tie.mp3")
                        pygame.mixer.music.play()
                elif (current_round == 4) or (current_round == 5) or (current_round == 6):
                    if scores[1] > scores[0]:
                        random_audio = choice(audio_FFSrounds_of_Seven_win)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
                    elif scores[1] < scores[0]:
                        random_audio = choice(audio_FFSrounds_of_Seven_lose)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
                    else:
                        random_audio = choice(audio_FFSrounds_of_Seven_tie)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
                elif current_round == 7:
                    if scores[1] > scores[0]:
                        random_audio = choice(audio_Frounds_of_Seven_win)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
                    elif scores[1] < scores[0]:
                        random_audio = choice(audio_Frounds_of_Seven_lose)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
                    else:
                        random_audio = choice(audio_Frounds_of_Seven_tie)  # Choose 1 in 3 audio files
                        play_sound(random_audio)
    # Press 's' to start the countdown
    if key == ord('s') and not stateResult and not startGame:  # Ensure startGame is False
        startGame = True
        initialTime = time.time()  # Start 3-second countdown for this round
        stateResult = False
        print("Starting countdown...")
        pygame.mixer.music.load("Audio/select_turns/round_of_total/coutdown/coutdown.mp3")
        pygame.mixer.music.play()
    
    if key == ord('q'): #Press 'q' to exit
        break

sock.close()  # Close the Bluetooth socket when done
cap.release()
cv2.destroyAllWindows()
