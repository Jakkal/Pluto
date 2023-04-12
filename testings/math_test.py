import math

thie = 110
leg = 115
height = 80

#Angles in degrees
Valpha = math.acos(((height*height)+(thie*thie)-(leg*leg))/(2*height*thie)) * (180.0 / math.pi)
Vbeta = math.acos(((leg*leg)+(thie*thie)-(height*height))/(2*leg*thie)) * (180.0 / math.pi)

#applying acos() and then converting the result in radians to degrees
#radians = 0.5
#PI = 3.14159265

print ("The value of Valpha : ", Valpha ,"Degrees")
print ("The value of Vbeta : ", Vbeta ,"Degrees")
