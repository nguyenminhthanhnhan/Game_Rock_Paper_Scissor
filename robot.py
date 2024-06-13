import bluetooth
import time
import cv2
import numpy as np
from random import choice
from keras.models import load_model

REV_CLASS_MAP = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "nothing"
}

def mapper(val):
    return REV_CLASS_MAP[val]

def calculate_winner(user_move, robot_move):
    if user_move == robot_move:
        return "Tie"
    elif user_move == "rock" and robot_move == "scissors":
        return "You win"
    elif user_move == "scissors" and robot_move == "paper":
        return "You win"
    elif user_move == "paper" and robot_move == "rock":
        return "You win"
    else:
        return "Robot wins"

def send_gesture(gesture):
    try:
        port = 1
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((hc05_mac_address, port))
        sock.send(gesture)
        sock.close()
        return True
    except:
        return False

model = load_model("game-model.h5")

# Địa chỉ MAC của thiết bị HC-05
hc05_mac_address = "00:18:E4:00:1C:4E"

# Hình thức của bàn tay robot: 1 - co, 0 - duỗi
gestures = {"scissors": "1*0*0*1*1#", "rock": "1*1*1*1*1#", "paper": "0*0*0*0*0#", "nothing": "0*1*1*0*1#"}

cap = cv2.VideoCapture(0)

prev_move = None

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.rectangle(frame, (10, 70), (300, 340), (0, 255, 0), 2)

    roi = frame[70:300, 10:340]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (227, 227))

    pred = model.predict(np.array([img]))
    move_code = np.argmax(pred[0])
    user_move_name = mapper(move_code)

    if prev_move != user_move_name:
        if user_move_name != "nothing":
            robot_move_name = choice(['rock', 'paper', 'scissors'])
            send_gesture(gestures[robot_move_name])
            winner = calculate_winner(user_move_name, robot_move_name)
        else:
            robot_move_name = "nothing"
            winner = "Waiting..."
    prev_move = user_move_name

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Move: " + user_move_name,
                (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Robot's Move: " + robot_move_name,
                (330, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Winner: " + winner,
                (100, 450), font, 2, (0, 255, 0), 4, cv2.LINE_AA)

    cv2.imshow("Rock Paper Scissors", frame)

    k = cv2.waitKey(10)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
