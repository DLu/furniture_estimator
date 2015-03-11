import pickle
from math import atan2, sin, cos, hypot, degrees
from geometry_msgs.msg import Point

def dist(p1, p2):
    return hypot(p1.x-p2.x, p1.y-p2.y)
    
def p(p1):
    return "(%.2f, %.2f)"%(p1.x, p1.y)    

REF = [(.88, -.12), (1.12, .21), (1.33, 0.13), (1.26, -0.27)]
RX = sum([x[0] for x in REF])/len(REF)
RY = sum([x[1] for x in REF])/len(REF)
a1 = degrees(atan2( REF[1][1]-REF[0][1], REF[1][0]-REF[0][0]))
a2 = degrees(atan2( REF[-2][1]-REF[-1][1], REF[-2][0]-REF[-1][0]))
RZ = (a1+a2)/2

full_cloud = pickle.load(open('laser.data'))

SEED = Point(1.0, 0.0, 0.0)

cloud = []
for pt in full_cloud:
    print p(pt), dist(SEED, pt)
    if dist(SEED, pt) < 1.0:
        cloud.append(pt)
        
print len(full_cloud), len(cloud)        


