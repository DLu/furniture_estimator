#!/usr/bin/python
import rospy
from furniture_estimator import *
from furniture_estimator.wheelchair import *
from sensor_msgs.msg import LaserScan
import tf

class WheelchairNode:
    def __init__(self):
        rospy.init_node('wheelchair_monitor')
        self.wf = WheelchairFilter()
        self.br = tf.TransformBroadcaster()
        self.sub = rospy.Subscriber('/base_scan', LaserScan, self.laser_cb)
        self.frame = None

    def laser_cb(self, msg):
        self.frame = msg.header.frame_id
        self.wf.update(msg)

    def spin(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            pose = self.wf.get_pose()
            if pose:
                self.br.sendTransform((pose[0], pose[1], 0),
                             tf.transformations.quaternion_from_euler(0, 0, pose[2]),
                             rospy.Time.now(),
                             '/wheelchair',
                             self.frame)
            r.sleep()                 

if __name__ == '__main__':
    n = WheelchairNode()
    n.spin()
