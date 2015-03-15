#!/usr/bin/python
import rospy, rosbag
import sys
from pylab import *
from furniture_estimator import *
from furniture_estimator.wheelchair import *
from math import degrees

def plotp(pts, symbol='.', color='blue'):
    plot([p[0] for p in pts], [p[1] for p in pts], symbol, color=color)

bag = rosbag.Bag(sys.argv[1])
pts = []
wf = WheelchairFilter()

for a,b,c in bag.read_messages():
    if a!='/base_scan':
        continue

    wf.update(b)
    x = wf.get_pose()
    print x[0:2], degrees(x[2])

    #plotp(pts, color='green', symbol='.')
    #plotp( [la, ra], color='red')
    #show()
plotp(wf.get_points())
plotp( [wf.get_pose()] )
xlim(0,1)
ylim(-0.5, 0.5)
show()
        
