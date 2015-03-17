from math import sin, cos, atan2, pi
from furniture_estimator import *
from furniture_estimator.kalman import *

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

class WheelchairFilter:
    def __init__(self):
        self.l_kalman = Kalman()
        self.r_kalman = Kalman()

    def update(self, scan):
        lpt, rpt = filter_scan(scan)
        self.l_kalman.update(lpt)
        self.r_kalman.update(rpt)

    def get_points(self):
        return [self.l_kalman.values(), self.r_kalman.values()]    

    def get_pose(self):
        lpt, rpt = self.get_points()
        if lpt is None:
            return None
        pt = avg([lpt, rpt])
        dx = lpt[0]-rpt[0]
        dy = lpt[1]-rpt[1]
        angle = atan2(dy,dx)

        return pt[0], pt[1], angle-pi/2
        
