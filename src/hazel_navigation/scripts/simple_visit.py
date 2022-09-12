#!/usr/bin/env python

# a simple visit


import rospy
import math

import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler


class CPoint(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "[x:{0},y:{1},z:{2}]".format(self.x,self.y,self.z)

    def __add__(self,other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return CPoint(x,y,z)

    def __sub__(self,other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return CPoint(x,y,z)

    def distance(self,other):
        dist = self-other
        squaredsum = dist.x*dist.x + dist.y*dist.y + dist.z*dist.z
        actualdist = math.sqrt(squaredsum)
        return actualdist


LOCATIONS = {'Door':CPoint(-8.18,-3.16,0.0), 'Tank1': CPoint(-4.07,-7.24,0.0),
              'TankSet North': CPoint((-0.49+-0.47)/2,(-3.51+-6.52)/2,0.0),
             'TankSet East': CPoint(2.30,-1.93,0.0), 'TankSet South': CPoint((5.48+5.36)/2,(-3.48+-6.31)/2,0.0),
             'TankSet West': CPoint(1.98,-7.88,0.0),
             'Pipes': CPoint(7.79,-2.67,0.0), 'Drum Room': CPoint(1.30,2.20,0.0),
          
             'Entrance':CPoint(-7.825369834899902, -0.5725803375244141, 0.02588939666748047)
             }





class SimpleVisit():

    def __init__(self):

        self.current_goal_pose = None
        self.goal_list = None
        self.goal_locations = None
        self.locations_reached = []
        self.current_goal = None
        self.goal_number = -1
        
        rospy.init_node('simple_visit')
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        rospy.loginfo("Waiting for move_base action server...")
        wait = self.client.wait_for_server(rospy.Duration(5.0))
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
            return

        rospy.loginfo("Connected to move base server")


    def active_callback(self):
        rospy.loginfo("Processing "+str(self.current_goal_pose))


    def feedback_callback(self,feedback):
        #rospy.loginfo("Feedback for "+str(self.current_goal_pose)+":"+str(feedback))
        #rospy.loginfo("Feedback received for "+str(self.current_goal_pose))
        pass

    def create_goal(self,current_goal_pose):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = current_goal_pose.x
        goal.target_pose.pose.position.y = current_goal_pose.y
        goal.target_pose.pose.position.z = current_goal_pose.z
        goal.target_pose.pose.orientation.w = 1.0
        return goal

    def send_next_goal(self):
        result = False
        
        if len(self.goal_list) > 0:
            self.goal_number = self.goal_number + 1
            self.current_goal = self.goal_locations[self.goal_number]
            
            self.current_goal_pose = self.goal_list.pop(0)
            goal = self.create_goal(self.current_goal_pose)
            self.client.send_goal(goal,self.done_callback,self.active_callback,self.feedback_callback)
            result = True

        rospy.loginfo("Goals executed")
        rospy.loginfo(self.locations_reached)
        
        return result
        
        

    def done_callback(self,status,result):
        if status == GoalStatus.PREEMPTED:
            rospy.loginfo("Goal "+str(self.current_goal_pose)+" received a cancel request after it started execution")
            
        elif status == GoalStatus.SUCCEEDED:
            rospy.loginfo("Goal "+str(self.current_goal_pose)+" reached")
            self.locations_reached.append(self.current_goal)
            if not self.send_next_goal():
                rospy.loginfo("Visited all locations")
                rospy.signal_shutdown("Shutting down simple visit")
                return 

        elif status == GoalStatus.ABORTED:
            rospy.loginfo("Goal "+str(self.current_goal_pose)+" aborted")
            rospy.signal_shutdown("Shutting down simple visit")
            return 

        elif status == GoalStatus.REJECTED:
            rospy.loginfo("Goal "+str(self.current_goal_pose)+" rejected")
            rospy.signal_shutdown("Shutting down simple visit")
            return 

        elif status == GoalStatus.RECALLED:
            rospy.loginfo("Goal "+str(self.current_goal_pose)+" received a cancel request before execution. Cancelled!")

            
    def start(self,locs):
        
        
        self.goal_locations = locs
        self.goal_list = []
        for loc in locs:
            self.goal_list.append(LOCATIONS[loc])

        rospy.loginfo("Prepared goals list")
        rospy.loginfo(self.goal_list)


        self.send_next_goal()

        rospy.spin()


if __name__ == '__main__':

    try:
        locs = ['Entrance', 'Tank1', 'TankSet North', 'TankSet West', 'TankSet South', 'TankSet West','TankSet North','Entrance','Door']
        simple_visit = SimpleVisit()
        simple_visit.start(locs)

    except rospy.ROSInterruptException:
        rospy.loginfo("Node shutdown")
        
        
        

        

        
            


        


            
            
            
                
                
                
            
