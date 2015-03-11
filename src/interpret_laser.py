#!/usr/bin/env python
import roslib; roslib.load_manifest('laser_assembler')
import rospy; from laser_assembler.srv import *

rospy.init_node("test_client")
rospy.wait_for_service("assemble_scans")
try:
    assemble_scans = rospy.ServiceProxy('assemble_scans', AssembleScans)
    resp = assemble_scans(rospy.Time(0,0), rospy.get_rostime())
    print "Got cloud with %u points" % len(resp.cloud.points)
    import pickle
    pickle.dump(resp.cloud.points, open('laser.data', 'w'))
    
    
except rospy.ServiceException, e:
    print "Service call failed: %s"%e
