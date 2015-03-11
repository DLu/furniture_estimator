import pickle
from math import atan2, sin, cos, hypot, degrees

from furniture_estimator import *
from furniture_estimator.match import *

REF = [(.88, -.12), (1.12, .21), (1.33, 0.13), (1.26, -0.27)]
RX = sum([x[0] for x in REF])/len(REF)
RY = sum([x[1] for x in REF])/len(REF)
a1 = atan2( REF[1][1]-REF[0][1], REF[1][0]-REF[0][0])
a2 = atan2( REF[-2][1]-REF[-1][1], REF[-2][0]-REF[-1][0])
RZ = (a1+a2)/2

print RX,RY,degrees(RZ)

REF3 = [(-.2, .2), (.2, .11), (.2, -.11), (-.2, -.2)]

full_cloud = to_list(pickle.load(open('laser.data')))

SEED = [1.0, 0.0, 0.4]

cloud = filter_cloud(full_cloud, SEED, 1.0)
x,y,theta= find_best_transform(REF3, cloud, SEED)
print x,y,degrees(theta)


