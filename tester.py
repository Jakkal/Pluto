import time
from adafruit_pca9685 import PCA9685

# Set the minimum and maximum pulse widths for a 270 degree servo
servo_min = 500
servo_max = 2500

#Servos numbers are:
#Left_rear_shoulder = 0
#Left_rear_hip = 1
#Left_rear_knee = 2
#Right_rear_shoulder = 3
#Right_rear_hip = 4
#Right_rear_knee = 5

#Left_front_shoulder = 6
#Left_front_hip = 7
#Left_front_knee = 8
#Right_front_shoulder = 9
#Right_front_hip = 10
#Right_front_knee = 11

class Servo:
    def __init__(self, pca, channel):
        self._pca = pca
        self._channel = channel
        #self._angle = 0

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if value < 0:
            value = 0
        elif value > 270:
            value = 270
        pulse_width = int(servo_min + (servo_max - servo_min) * value / 270.0)
        self._pca.channels[self._channel].duty_cycle = pulse_width
        self._angle = value

# Initialize the PCA9685 board
pca = PCA9685()
pca.frequency = 50

# Create a list of servos
servos = [Servo(pca, i) for i in range(16)]

# Loop to set the angle of the servo
while True:
    # Prompt the user for an angle
    angle_str = input("Enter an angle between 0 and 270 degrees (or q to quit): ")
    if angle_str == 'q':
        break
    try:
        angle = int(angle_str)
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 270 degrees.")
        continue
    if angle < 0 or angle > 270:
        print("Invalid input. Please enter a number between 0 and 270 degrees.")
        continue
    # Set the angle of the servo
    servos[0].angle = angle

# Wait for 1 second
time.sleep(1)
