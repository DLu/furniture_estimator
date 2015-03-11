import rospy
from laser_assembler.srv import *
import sys

if len(sys.argv)<2:
    print "NEED ARG"
    exit(0)
rospy.init_node("test_client")
rospy.wait_for_service("assemble_scans")
assemble_scans = rospy.ServiceProxy('assemble_scans', AssembleScans)
resp = assemble_scans(rospy.Time(0,0), rospy.get_rostime())
print "Got cloud with %u points" % len(resp.cloud.points)
import pickle
pickle.dump(resp.cloud.points, open(sys.argv[1], 'w'))
