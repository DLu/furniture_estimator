import tf
import math
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import PointStamped

def get_best_transform(tfman, msg, base_frame):
    xyz, quat = tfman.lookupTransform(base_frame, msg.header.frame_id, msg.header.stamp)
    rpy = tf.transformations.euler_from_quaternion(quat)
    pos = [xyz[0],xyz[1],rpy[2]]
    if msg.header.frame_id in refs:
        pos = get_best_helper(pos, msg)
    return get_transform(pos, '/map', msg.header.frame_id, msg.header.stamp)

def get_point(msg, i, tfman, base_frame):
    d = msg.ranges[i]
    if d > msg.range_max or d < msg.range_min:
        return None
    angle = msg.angle_min + msg.angle_increment * i

    pt = PointStamped()
    pt.header.frame_id = msg.header.frame_id
    pt.header.stamp = msg.header.stamp
    pt.point.x = math.cos(angle) * d
    pt.point.y = math.sin(angle) * d
    pt2 = tfman.transformPoint(base_frame, pt)
    return pt2.point

def get_transform(pos, parent, child, stamp):
    transform = TransformStamped()
    transform.header.frame_id = parent
    transform.header.stamp = stamp
    transform.child_frame_id = child
    transform.transform.translation.x = pos[0]
    transform.transform.translation.y = pos[1]
    transform.transform.translation.z = .099
    quat = tf.transformations.quaternion_from_euler(0,0,pos[2])
    transform.transform.rotation.x = quat[0]
    transform.transform.rotation.y = quat[1]
    transform.transform.rotation.z = quat[2]
    transform.transform.rotation.w = quat[3]
    return transform

def get_points(msg, tfman, parent='/map'):
    pts = []
    for i in range(len(msg.ranges)):
        pt = get_point(msg,i,tfman, parent) 
        if pt is not None:
            pts.append(pt)
    return pts

def get_pts(pos, msg, parent='/map'):
    tfman = tf.TransformerROS()
    tfman.setTransform(get_transform(pos, parent, msg.header.frame_id, msg.header.stamp))
    return get_points(msg, tfman, parent=parent)
