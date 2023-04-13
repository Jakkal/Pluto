import time
import math

from adafruit_servokit import ServoKit

#-----------[ SET PLUTOS REST POSITION, LAYING DOWN FLAT ]
#Servos numbers are:
#Left_rear_shoulder = 0  - 	94
#Left_rear_hip = 1 - 		225
#Left_rear_knee = 2 - 		30
#Right_rear_shoulder = 3 -	35
#Right_rear_hip = 4 - 		17
#Right_rear_knee = 5 - 		235

#Left_front_shoulder = 6	115
#Left_front_hip = 7		160
#Left_front_knee = 8		110
#Right_front_shoulder = 9	40
#Right_front_hip = 10		155
#Right_front_knee = 11		170
rest_pos = [94,225,30,35,17,235,115,160,110,40,155,170]

def Initiate_Pluto():
    #Setup the servos range, and pulse
    for i in range(16):
        #change actuation_range for all servos
        pluto.servo[i].actuation_range = 270
        pluto.servo[i].set_pulse_width_range(500,2500)
    #Special care for hip servos:
    pluto.servo[1].actuation_range = 290
    pluto.servo[4].actuation_range = 290
    pluto.servo[7].actuation_range = 290
    pluto.servo[10].actuation_range = 290
    pluto.foot = 115 #Length of foot
    pluto.leg = 110 #Length of leg

def Servos_to_rest_pos():
    for i in range(12):
        pluto.servo[i].angle = rest_pos[i]

pluto = ServoKit(channels=16)

#Setup the servos
Initiate_Pluto()

input("Pluto SETUP complete. Only continue if rest position is set (ENTER)...")

Servos_to_rest_pos()

input("Plut is at rest position (ENTER)...")


time.sleep(1)
