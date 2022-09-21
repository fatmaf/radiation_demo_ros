#! /usr/bin/env python3

import rospy
import actionlib

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Vector3

import sys
import getpass
current_user = getpass.getuser()
pointlib_path = "/home/{0}/work/code/ros/ros1/rad_ws/shared_python".format(current_user)
sys.path.insert(0,pointlib_path)
from Point import CPoint
from Point import LOCATIONS


class movebase_client:
    def __init__(self,x,y,z,done_cb):
        self.client = self.init_client_and_send_to_movebase(x,y,z,done_cb)
        
        
    def init_client_and_send_to_movebase(self,x,y,z,done_cb):
        client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        wait = client.wait_for_server()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            rospy.loginfo("Action server available")           

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.position.z = z
        goal.target_pose.pose.orientation.w = 1.0

        client.send_goal(goal,done_cb)
        rospy.loginfo("Goal sent")
        return client
    
    def cancel_goal(self):
        if self.client is not None:
            self.client.cancel_goal()
            rospy.loginfo("Cancelled goal!")
            
    
class test_movebase_cancel:
    
    def __init__(self):
        self.mbclient = None 
        self.movebase_client()
    
    
    def is_stop_goal(self,data):
        
        if(data.x==0 and data.y==0 and data.z == 0):
            return True
        return False
    
     
    def done_callback(self,status,result):
        if status == GoalStatus.PREEMPTED:
            rospy.loginfo("Goal received a cancel request after it started execution")
            
        elif status == GoalStatus.SUCCEEDED:
            rospy.loginfo("Goal reached")
    
            

        elif status == GoalStatus.ABORTED:
            rospy.loginfo("Goal aborted")


        elif status == GoalStatus.REJECTED:
            rospy.loginfo("Goal rejected")


        elif status == GoalStatus.RECALLED:
            rospy.loginfo("Goal received a cancel request before execution. Cancelled!")
        self.mbclient = None
     
    def goal_movebase(self,data):
    	
        try:
            self.mbclient = movebase_client(data.x,data.y,data.z,self.done_callback)

        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")    
    
    def movebase_client(self):
        
        rospy.init_node('test_movebase_cancel_py', anonymous=True)
        locstring = ""
        for l in LOCATIONS:
            locstring+=l+", "
            
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            #keep asking the user if they want to cancel 
            #or choose a location 
            user_input = input("Press c to cancel current goal, g to choose new goal, control c to exit")
            if(user_input == "g" and self.mbclient is None):
                loc_input = input("Type in location from list: "+locstring)
                if loc_input in LOCATIONS:
                    data = LOCATIONS[loc_input]
                    self.goal_movebase(data)
                    print("Sent goal")
            elif (user_input=="g" and self.mbclient is not None):
                print("still executing a previous goal")
            elif (user_input =="c" and self.mbclient is not None):
                self.mbclient.cancel_goal()
                print("sent cancel request")
            elif (user_input == "c" and self.mbclient is None):
                print("no current goal")
                    
            rate.sleep()
    	

if __name__ == '__main__':
    test_movebase_cancel()
