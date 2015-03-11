from math import atan2, sin, cos, hypot
from furniture_estimator import *

def distance(ref_pts, pts):
    D = 0
    for rpt in ref_pts:
        dmin = 1E9
        for pt in pts:
            d = dist(rpt, pt)
            if d < dmin:
                dmin = d
        D += dmin
    return D

def transform(pose, polar):
    new_pts = []
    for angle, d in polar:
        nx = pose[0] + cos(pose[2] + angle) * d
        ny = pose[1] + sin(pose[2] + angle) * d
        new_pts.append((nx,ny))
    return new_pts    

def transform_linear(pose, pts):
    return transform(pose, [(atan2(y,x), hypot(x,y)) for x,y in pts])

def find_best_transform(reference, cloud, pos):
    polar_ref = [(atan2(y,x), hypot(x,y)) for x,y in reference]
    
    deltas = [.2, .1, .05, .01, .005, .001]
    for i, delta in enumerate(deltas):
        changes = 1
        while changes > 0:
            changes = 0
            for i in range(len(pos)):
                best = 1E9
                fp = None
                for f in [-1, 0, 1]:
                    vn = [a for a in pos]
                    vn[i] += delta * f

                    pts = transform(vn, polar_ref)
                    d = distance(pts, cloud)
                    if d < best:
                        best = d
                        fp = f
                if fp!=0 and fp!=None:
                    changes+=1
                    pos[i] += delta * fp
    return pos
