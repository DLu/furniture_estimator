#!/usr/bin/env python

import rospy
from laser_assembler.srv import *
from furniture_estimator.match import *
import tf
import yaml
from math import degrees

class Tracer:
    def __init__(self, model, name):
        self.model = model
        self.name = name

        self.br = tf.TransformBroadcaster()
        rospy.wait_for_service("assemble_scans")
        self.assemble_scans = rospy.ServiceProxy('assemble_scans', AssembleScans)

        self.pose = [1.0, 0.0, 0.4]

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
            
model = yaml.load(open('data/chair.yaml'))
rospy.init_node("test_client")
t = Tracer(model, 'chair')
t.spin()
