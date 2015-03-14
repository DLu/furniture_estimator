from math import atan2, sin, cos, hypot
from furniture_estimator import *

def match_clouds(model, cloud, max_a=0.1):
    J = {}
    for pt in model:
        J[pt] = []
    J[None] = []

    D = {}
    
    for cpt in cloud:
        dmin = 1E6
        mpt = None
        for pt in model:
            d = dist(cpt, pt)
            if d < dmin:
                dmin = d
                mpt = pt
        if dmin < max_a:
            J[mpt].append(cpt)
        else:
            J[None].append(cpt)
        D[cpt] = dmin

    score = 0.0
    for pt in model:
        X = J[ pt ]
        if len(X)>0:
            Y = [D[x] for x in X]
            score += min(Y)
        else:
            dmin = d
            for cpt in J[None]:
                d = dist(cpt, pt)
                if d < dmin:
                    dmin = d
            score += dmin        
          
    return score, J

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
                    d, X = match_clouds(pts, cloud)
                    if d < best:
                        best = d
                        fp = f
                if fp!=0 and fp!=None:
                    changes+=1
                    pos[i] += delta * fp
    return pos
