#!/usr/bin/env python

import rospy
from laser_assembler.srv import *
from furniture_estimator.match import *
import tf
import yaml
import sys
import os

class Tracer:
    def __init__(self):
        self.model = rospy.get_param('~model')
        self.name = rospy.get_param('~name')

        self.br = tf.TransformBroadcaster()
        rospy.wait_for_service("assemble_scans")
        self.assemble_scans = rospy.ServiceProxy('assemble_scans', AssembleScans)

        self.pose = rospy.get_param('~seed', [0,0,0])

    def estimate(self):
        resp = self.assemble_scans(rospy.Time(0,0), rospy.get_rostime())
        self.base_frame = resp.cloud.header.frame_id
        c2 = to_list(resp.cloud.points)

        cloud = filter_cloud(c2, self.pose)
        if cloud is None or len(cloud)==0:
            return None
        return find_best_transform(self.model, cloud, self.pose)
            
    def spin(self):
        r = rospy.Rate(20)
        while not rospy.is_shutdown():
            estimate = self.estimate()
            if estimate is not None:
                self.pose = estimate
                self.br.sendTransform((self.pose[0], self.pose[1], 0),
                             tf.transformations.quaternion_from_euler(0, 0, self.pose[2]),
                             rospy.Time.now(),
                             self.name,
                             self.base_frame)
            r.sleep()

rospy.init_node('laser_tracer')
for arg in sys.argv[1:]:
    if 'yaml' in arg:
        model = yaml.load(open(arg))
        rospy.set_param('~model', model)
        name = os.path.splitext(os.path.split(arg)[-1])[0]
        rospy.set_param('~name', name)

t = Tracer()
t.spin()
