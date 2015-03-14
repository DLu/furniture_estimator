import pickle
from math import atan2, sin, cos, hypot, degrees, radians

from furniture_estimator import *
from furniture_estimator.match import *

import sys
import yaml

model = yaml.load(open(sys.argv[1]))
data = to_list(pickle.load(open(sys.argv[2])))
should_plot = '-p' in sys.argv

#SEED = [-2.5, 5.6, -0.4]

SEED = [1.172, -0.042, -radians(30)]

model = transform_linear(SEED, model)

cloud = filter_cloud(data, SEED, 1.0)

if False:
    J = {}
    for pt in model:
        J[tuple(pt)] = []
    J[tuple(model[0])] = cloud    
else:
    score, J = match_clouds(model, cloud)
    print score
from pylab import *


def plotp(pts, symbol='o', color='blue'):
    plot([p[0] for p in pts], [p[1] for p in pts], symbol, color=color)

COLORS = ['red', 'green', 'blue', 'yellow', 'orange']
ci = 0
    
for pt, pts in J.iteritems():
    c = COLORS[ci % len(COLORS)]
    if pt is not None:
        plotp([pt], color= c)
    plotp(pts, symbol='.', color=c)

    ci +=1 
    
show()    
