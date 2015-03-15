#!/usr/bin/python
import rospy, rosbag
import sys
from pylab import *
from furniture_estimator import *
from furniture_estimator.wheelchair import *

def plotp(pts, symbol='.', color='blue'):
    plot([p[0] for p in pts], [p[1] for p in pts], symbol, color=color)

bag = rosbag.Bag(sys.argv[1])
pts = []

for a,b,c in bag.read_messages():
    if a!='/base_scan':
        continue
    lpt, rpt = filter_scan(b)    
    pts.append(lpt)
    pts.append(rpt)

plotp(pts, color='green', symbol='o')
show()
        
