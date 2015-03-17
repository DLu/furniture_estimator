#!/usr/bin/python
import rospy
from furniture_estimator import *
from furniture_estimator.wheelchair import *
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseStamped
import tf

class WheelchairNode:
    def __init__(self):
        rospy.init_node('wheelchair_monitor')
        self.wf = WheelchairFilter()
        self.br = tf.TransformBroadcaster()
        self.tf = tf.TransformListener()
        self.sub = rospy.Subscriber('/base_scan', LaserScan, self.laser_cb)
        self.frame = None
        self.broadcast_frame = '/odom_combined'

    def laser_cb(self, msg):
        self.frame = msg.header.frame_id
        self.wf.update(msg)

    def spin(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            r.sleep()
            pose = self.wf.get_pose()
            if not pose:
                continue  
                
            ps = PoseStamped()
            ps.header.frame_id = self.frame
            ps.pose.position.x = pose[0]
            ps.pose.position.y = pose[1]
            q = tf.transformations.quaternion_from_euler(0, 0, pose[2])
            ps.pose.orientation.x = q[0]
            ps.pose.orientation.y = q[1]
            ps.pose.orientation.z = q[2]
            ps.pose.orientation.w = q[3]

            try:
                np = self.tf.transformPose(self.broadcast_frame, ps)
            except:
                continue

            pos = np.pose.position
            q = np.pose.orientation    
            self.br.sendTransform((pos.x, pos.y, pos.z),
                         (q.x, q.y, q.z, q.w),
                         rospy.Time.now(),
                         '/wheelchair',
                         np.header.frame_id)

if __name__ == '__main__':
    n = WheelchairNode()
    n.spin()
