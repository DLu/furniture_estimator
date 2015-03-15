#!/usr/bin/python
import rospy, rosbag
import sys
from pylab import *
from furniture_estimator import *
from furniture_estimator.wheelchair import *
from furniture_estimator.kalman import *

def plotp(pts, symbol='.', color='blue'):
    plot([p[0] for p in pts], [p[1] for p in pts], symbol, color=color)

bag = rosbag.Bag(sys.argv[1])
pts = []

k1 = Kalman()
k2 = Kalman()

for a,b,c in bag.read_messages():
    if a!='/base_scan':
        continue
    lpt, rpt = filter_scan(b)
    k1.update(lpt)
    k2.update(rpt)
    pts.append(lpt)
    pts.append(rpt)

    la = k1.values()
    ra = k2.values()

    #plotp(pts, color='green', symbol='.')
    plotp( [la, ra], color='red')
    #show()
show()
        
