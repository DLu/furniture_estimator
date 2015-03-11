from math import atan2, sin, cos, hypot

def distance(ref_pts, pts):
    D = 0
    for x,y in ref_pts:
        dmin = 1E9
        for pt in pts:
            d = hypot(x-pt[0],y-pt[1])
            if d < dmin:
                dmin = d
        D += dmin
    return D

def transform(pose, cloud):
    new_pts = []
    for x,y in cloud:
        angle = atan2(y,x)
        d = hypot(x,y)
        nx = pose[0] + cos(pose[2] + angle) * d
        ny = pose[1] + sin(pose[2] + angle) * d
        new_pts.append((nx,ny))
    return new_pts    

def find_best_transform(reference, cloud, pos):
    deltas = [.2, .1, .05, .01, .005, .001]
    for i, delta in enumerate(deltas):
        changes = 1
        while changes > 0:
            changes = 0
            for i in range(len(pos)):
                best = None
                fp = None
                for f in [-1, 0, 1]:
                    vn = [a for a in pos]
                    vn[i] += delta * f

                    pts = transform(vn, reference)
                    d = distance(pts, cloud)
                    if best is None or d < best:
                        best = d
                        fp = f
                if fp!=0:
                    changes+=1
                    pos[i] += delta * fp
    return pos
