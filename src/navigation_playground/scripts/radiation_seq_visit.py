#!/usr/bin/env python3

# a simple visit

import rospy
from SimpleVisit import SimpleVisit



if __name__ == '__main__':

    try:
        #visit(iP1),visit(t2bottom),visit(tankset),visit(pipes)
        locs = ['IP1','t2bottom','tankset','pipes']
        simple_visit = SimpleVisit()
        simple_visit.start(locs)

    except rospy.ROSInterruptException:
        rospy.loginfo("Node shutdown")
        
        