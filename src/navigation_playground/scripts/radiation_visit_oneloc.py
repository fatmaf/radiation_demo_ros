#!/usr/bin/env python3

# a simple visit

import rospy
from SimpleVisit import SimpleVisit



if __name__ == '__main__':

    try:
        locs = ['entrance','pipes']
        simple_visit = SimpleVisit()
        simple_visit.start(locs)

    except rospy.ROSInterruptException:
        rospy.loginfo("Node shutdown")
        
        
        

        

        
            


        


            
            
            
                
                
                
            
