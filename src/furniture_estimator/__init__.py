from math import hypot

def dist(p1,p2):
    return hypot(p1[0]-p2[0], p1[1]-p2[1])

def filter_cloud(cloud, seed, MAX_D=1.0):
    cloud2 = []
    for pt in cloud:
        if dist(seed, pt) < MAX_D:
            cloud2.append(pt)
    return cloud2        

def to_list(cloud):
    return [(pt.x, pt.y) for pt in cloud]
