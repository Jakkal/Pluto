import time
import math

from adafruit_servokit import ServoKit

#-----------[ SET PLUTOS REST POSITION, LAYING DOWN FLAT ]
#Servos numbers are:
#Left_rear_shoulder = 0  - 	94
#Left_rear_hip = 1 - 		225
#Left_rear_knee = 2 - 		35
#Right_rear_shoulder = 3 -	35
#Right_rear_hip = 4 - 		17
#Right_rear_knee = 5 - 		220

#Left_front_shoulder = 6	115
#Left_front_hip = 7		160
#Left_front_knee = 8		110
#Right_front_shoulder = 9	40
#Right_front_hip = 10		155
#Right_front_knee = 11		170
rest_pos = [94,225,35,35,17,220,115,160,110,40,155,170]

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

def Walk_at_height(height):
    #Limit height, so robot doesn't crash
    if (height > 170):
        height = 170
    if (height < 80):
        height = 80

    # Lift of each leg, and walking +-mm
    walk_lift = 20
    walk_step = 10

    # Walk gait [rl, fl, rr, fr]

    #Begin with making Pluto stand still at height
    Stand_at_height(height)

    # Calculate walking points
    hypotenusan = [
        math.sqrt(walk_step*walk_step+height*height),
        math.sqrt((walk_step*0.66)*(walk_step*0.66)+height*height),
        math.sqrt((walk_step*0.33)*(walk_step*0.33)+height*height),
        height,
        math.sqrt((walk_step*0.33)*(walk_step*0.33)+height*height),
        math.sqrt((walk_step*0.66)*(walk_step*0.66)+height*height),
        math.sqrt(walk_step*walk_step+height*height),
        math.sqrt(walk_step*walk_step+(height-walk_lift)*(height-walk_lift)),
        math.sqrt(walk_step*walk_step+(height-walk_lift)*(height-walk_lift))
    ]
    angles_hip_adjust = [
        math.atan(walk_step/height) * (180.0 / math.pi),
        math.atan((walk_step*0.66)/height) * (180.0 / math.pi),
        math.atan((walk_step*0.33)/height) * (180.0 / math.pi),
        0,
        -math.atan((walk_step*0.33)/height) * (180.0 / math.pi),
        -math.atan((walk_step*0.66)/height) * (180.0 / math.pi),
        -math.atan(walk_step/height) * (180.0 / math.pi),
        -math.atan(walk_step/(height-walk_lift)) * (180.0 / math.pi),
        math.atan(walk_step/(height-walk_lift)) * (180.0 / math.pi)
    ]

    #Set angles for first leg start
    #Valpha = math.acos(((hypotenusan[0]*hypotenusan[0])+(pluto.leg*pluto.leg)-(pluto.foot*pluto.foot))/(2*hypotenusan[0]*pluto.leg)) * (180.0 / math.pi) + angles_hip_adjust[0]
    #Vbeta = math.acos(((pluto.foot*pluto.foot)+(pluto.leg*pluto.leg)-(hypotenusan[0]*hypotenusan[0]))/(2*pluto.foot*pluto.leg)) * (180.0 / math.pi)

    # Testing one leg step-function
    i = 0
    #Gait pos 0-8
    gait = [0,4,2,6]
    legc = [1,7,4,10]
    leginv = [1,-1,1,-1]

    try:
        while True:
            #Calculate angles
            for legs in range(4):
                Valpha = math.acos(((hypotenusan[gait[legs]]*hypotenusan[gait[legs]])+(pluto.leg*pluto.leg)-(pluto.foot*pluto.foot))/(2*hypotenusan[gait[legs]]*pluto.leg)) * (180.0 / math.pi) - angles_hip_adjust[gait[legs]]
                Vbeta = math.acos(((pluto.foot*pluto.foot)+(pluto.leg*pluto.leg)-(hypotenusan[gait[legs]]*hypotenusan[gait[legs]]))/(2*pluto.foot*pluto.leg)) * (180.0 / math.pi)

                pluto.servo[legc[legs]].angle = rest_pos[legc[legs]] - (pluto.leg_fully_extended + Valpha)*leginv[legs]
                pluto.servo[legc[legs]+1].angle = rest_pos[legc[legs]+1] + (pluto.foot_fully_extended - (180-Vbeta))*leginv[legs]

                gait[legs] = gait[legs]+1
                if gait[legs] > 8:
                    gait[legs] = 0
            #pluto.servo[4].angle = rest_pos[4] + pluto.leg_fully_extended - Valpha
            #pluto.servo[5].angle = rest_pos[5] - pluto.foot_fully_extended + (180-Vbeta)

            time.sleep(0.2)
            i = i + 1
            if (i > 8):
                i = 0
    except KeyboardInterrupt:
        print('interrupted!')

#---------MAIN BELOW

pluto = ServoKit(channels=16)

#Setup the servos
Initiate_Pluto()

input("Pluto SETUP complete. Only continue if rest position is set (ENTER)...")

Servos_to_rest_pos()

input("Pluto is at rest position (ENTER)...")

Stand_at_height(150)

input("Start Walk sequence (ENTER)...")

Walk_at_height(150)



time.sleep(1)
