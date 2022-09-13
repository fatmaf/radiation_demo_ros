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
    def __init__(self,x,y,z,wz,ww):
        self.x = x
        self.y = y
        self.z = z
        self.wz = wz 
        self.ww = ww 

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


LOCATIONS = {'Door':CPoint(-8.18,-3.16,0.0,0.0,1.0),
             'Entrance':CPoint( -7.74,-0.82, 0.0, 0.14731291262509252,0.9890899381623047),
             'Tank1':CPoint(-3.85, -6.91,0.0, -0.8553221401678269,0.5180965513673375),
             'TankSet West Fwd': CPoint(  1.45, -8.08, 0.0, 0.16241024344707755,0.986723321313255),
             'TankSet South': CPoint( 5.75,-5.65,0.0, 0.8635580966167641,0.5042493567349705),
             'Decision Point': CPoint( 6.45, -3.90, 0.0,0.45383837088914697, 0.8910840213519066),
             'TankSet West Back':CPoint(1.71, -7.92, 0.0, -0.9947942926135805, 0.10190346109650017),
             'Door Back':CPoint( -7.97, -2.81, 0.0, -0.9374338259535748,0.3481634988881556),
             'Entrance End':CPoint( -7.48, -0.60, 0.0,-0.884241318990104,0.46703028787289697),
             
             # 'Tank1': CPoint(-4.07,-7.24,0.0),
            #  'TankSet North': CPoint((-0.49+-0.47)/2,(-3.51+-6.52)/2,0.0),
             #'TankSet East': CPoint(2.30,-1.93,0.0), 'TankSet South': CPoint((5.48+5.36)/2,(-3.48+-6.31)/2,0.0),
             #'TankSet West': CPoint(1.98,-7.88,0.0),
            'Pipes': CPoint(7.79,-2.67,0.0,0.0,1.0),
             'Drum Room': CPoint(1.30,2.20,0.0,0.0,1.0),
             'Ghost Point': CPoint(0.48, 5.13, 0.0,0.0,1.0)
          
             #'Entrance':CPoint(-7.825369834899902, -0.5725803375244141, 0.02588939666748047)
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
        goal.target_pose.pose.orientation.z = current_goal_pose.wz
        goal.target_pose.pose.orientation.w = current_goal_pose.ww
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
            if not self.send_next_goal():
                rospy.loginfo("Visited all locations")
            #rospy.signal_shutdown("Shutting down simple visit")
            #return 

        elif status == GoalStatus.REJECTED:
            rospy.loginfo("Goal "+str(self.current_goal_pose)+" rejected")
           # rospy.signal_shutdown("Shutting down simple visit")
            #return 

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
        locs = ['Entrance', 'Pipes',  'Drum Room', 'Ghost Point', 'Tank1','Entrance End','Door Back']
        simple_visit = SimpleVisit()
        simple_visit.start(locs)
        rospy.loginfo("All done!")

    except rospy.ROSInterruptException:
        rospy.loginfo("Node shutdown")
        
        
        

        

        
            


        


            
            
            
                
                
                
            
