import pickle
from math import atan2, sin, cos, hypot, degrees

from furniture_estimator import *
from furniture_estimator.match import *

import sys
import yaml

model = yaml.load(open(sys.argv[1]))
data = to_list(pickle.load(open(sys.argv[2])))
should_plot = '-p' in sys.argv

SEED = [-2.0, 5.0, 0.4]

cloud = filter_cloud(data, SEED, 1.0)
x,y,theta= find_best_transform(model, cloud, SEED)
print x,y,degrees(theta)

if should_plot:

    from pylab import *

    def plotp(pts, color='blue'):
        plot([p[0] for p in pts], [p[1] for p in pts], 'o', color=color)

    plotp(cloud)
    plotp(transform_linear((x,y,theta),model), color='red')
    show()    
