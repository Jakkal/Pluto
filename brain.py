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
    pluto.foot_fully_extended = 140 #140 degrees from it's rest position! IMPORTANT!
    pluto.leg_fully_extended = 90

def Servos_to_rest_pos():
    for i in range(12):
        pluto.servo[i].angle = rest_pos[i]

def Stand_at_height(height):
    #Limit height, so robot doesn't crash
    if (height > 170):
        height = 170
    if (height < 70):
        height = 70
    #Set angles
    Valpha = math.acos(((height*height)+(pluto.leg*pluto.leg)-(pluto.foot*pluto.foot))/(2*height*pluto.leg)) * (180.0 / math.pi)
    Vbeta = math.acos(((pluto.foot*pluto.foot)+(pluto.leg*pluto.leg)-(height*height))/(2*pluto.foot*pluto.leg)) * (180.0 / math.pi)
    print("Alpha")
    print(Valpha)
    print("Beta")
    print(Vbeta)
    #Left rear leg
    pluto.servo[1].angle = rest_pos[1] - pluto.leg_fully_extended + Valpha
    pluto.servo[2].angle = rest_pos[2] + pluto.foot_fully_extended - (180-Vbeta)
    #Right rear leg
    pluto.servo[4].angle = rest_pos[4] + pluto.leg_fully_extended - Valpha
    pluto.servo[5].angle = rest_pos[5] - pluto.foot_fully_extended + (180-Vbeta)
    #Left front leg
    pluto.servo[7].angle = rest_pos[7] - pluto.leg_fully_extended + Valpha
    pluto.servo[8].angle = rest_pos[8] + pluto.foot_fully_extended - (180-Vbeta)
    #Right front leg
    pluto.servo[10].angle = rest_pos[10] + pluto.leg_fully_extended - Valpha
    pluto.servo[11].angle = rest_pos[11] - pluto.foot_fully_extended + (180-Vbeta)

#---------MAIN BELOW

pluto = ServoKit(channels=16)

#Setup the servos
Initiate_Pluto()

input("Pluto SETUP complete. Only continue if rest position is set (ENTER)...")

Servos_to_rest_pos()

input("Plut is at rest position (ENTER)...")

Stand_at_height(100)

time.sleep(1)
