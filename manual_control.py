import sys
import bluetooth
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage  # Updated import statement
import cv2

class RobotHandControl(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Control Robot Hand by manual')  # Updated window title
        self.sliders = []  # Initialize sliders list
        self.init_ui()  # Initialize UI
        self.init_bluetooth()  # Initialize Bluetooth
        self.set_all_fingers_to_stretch()  # Set fingers to stretch

    def init_ui(self):
        main_layout = QHBoxLayout()  # Main layout for splitting the interface

        # Left half for camera frame
        self.camera_frame = QLabel("Camera Frame Placeholder")  # Placeholder for camera
        self.camera_frame.setStyleSheet("border: 2px solid black;")  # Add a border to the frame
        main_layout.addWidget(self.camera_frame, 1)  # Add camera frame to the left

        # Right half for robot hand control
        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        finger_layout = QVBoxLayout()  # Use a single layout for fingers

        for finger in finger_names:
            label = QLabel(finger)
            label.setAlignment(Qt.AlignCenter)
            
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(0)
            slider.setMaximum(1)
            slider.setValue(1)  # Default to extended
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setTickInterval(1)
            slider.valueChanged.connect(self.update_hand_state)
            
            self.sliders.append(slider)
            
            finger_layout.addWidget(QLabel('1'))
            finger_layout.addWidget(slider)
            finger_layout.addWidget(QLabel('0'))
            finger_layout.addWidget(label)
        
        main_layout.addLayout(finger_layout)  # Add the single finger layout

        # Create and configure the Exit button
        exit_button = QPushButton("EXIT")  # Create the Exit button
        exit_button.setStyleSheet("background-color: red;")  # Change the button color to light gray
        exit_button.clicked.connect(self.close)  # Connect the button to the close method
        
        # Add the Exit button to the layout
        main_layout.addWidget(exit_button, alignment=Qt.AlignBottom | Qt.AlignRight)  # Place it at the bottom right

        self.setLayout(main_layout)

        # Check if all sliders are in extended mode, if not set them to 1
        if any(slider.value() == 0 for slider in self.sliders):
            for slider in self.sliders:
                slider.setValue(1)  # Set all sliders to extended mode

        self.capture = cv2.VideoCapture(0)  # Open the default camera
        self.timer = QTimer(self)  # Create a timer to update the camera feed
        self.timer.timeout.connect(self.update_camera_feed)  # Connect the timer to the update function
        self.timer.start(30)  # Update the feed every 30 ms

    def init_bluetooth(self):
        try:
            hc05_mac_address = "98:DA:60:0A:13:25"  # Replace with the actual MAC address
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            port = 1  # Default RFCOMM port for HC-05 module is 1
            self.sock.connect((hc05_mac_address, port))
        except bluetooth.btcommon.BluetoothError as e:
            print(f"Bluetooth connection failed: {e}")

    def update_hand_state(self):
        # Update only the changed slider and set others accordingly
        for index, slider in enumerate(self.sliders):
            if slider.value() == 1:
                slider.setValue(1)  # Set the current slider to 1 (extension)
            else:
                slider.setValue(0)  # Set all other sliders to 0 (contraction)

        hand_state = '*'.join([str(slider.value()) for slider in self.sliders]) + '#'
        self.sock.send(hand_state.encode())
        print(f"Sent: {hand_state}")

    def update_camera_feed(self):
        if self.isVisible():  # Only update if the window is visible
            ret, frame = self.capture.read()  # Read a frame from the camera
            if ret:
                # Convert the frame to RGB format and display it
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.camera_frame.setPixmap(QPixmap.fromImage(q_img))  # Update the QLabel with the new image

    def closeEvent(self, event):
        self.capture.release()  # Release the camera when closing the application
        self.sock.close()
        event.accept()

    def set_all_fingers_to_stretch(self):
        for slider in self.sliders:
            slider.setValue(1)  # Set all sliders to extended mode
        self.update_hand_state()  # Update the hand state to send the new values

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotHandControl()
    window.show()
    sys.exit(app.exec_())
