from math import sin, cos
from furniture_estimator import *

def filter_scan(scan, max_d=2.0, max_a=1.5, window=.05, plot=False):
    polar = []
    angle_sum = 0.0
    angle_c = 0
    for i,d in enumerate(scan.ranges):
        if d < max_d:
            angle = scan.angle_min + i * scan.angle_increment
            if abs(angle)>max_a:
                continue
            polar.append( (d, angle) )
            angle_sum += angle
            angle_c += 1
    
    av_angle = angle_sum/ angle_c

    ds = [None, None]
    pts = [[], []]
    
    for d,angle in sorted(polar):
        x = d * cos(angle)
        y = d * sin(angle)
        pt = (x,y)
        
        if angle>av_angle:
            i = 0
        else:
            i = 1

        if ds[i] is None or ((d-ds[i])>window and len(pts[i])<5):
            ds[i] = d
            pts[i] = []
        if d-ds[i] < window:
            pts[i].append(pt)
            
    lpt = avg(pts[0])
    rpt = avg(pts[1])
    return lpt, rpt

