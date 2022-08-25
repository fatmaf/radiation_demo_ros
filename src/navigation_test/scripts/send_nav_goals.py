#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Vector3




class Point(object):
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
        return Point(x,y,z)

    def __sub__(self,other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Point(x,y,z)

    def distance(self,other):
        dist = self-other
        squaredsum = dist.x*dist.x + dist.y*dist.y + dist.z*dist.z
        actualdist = math.sqrt(squaredsum)
        return actualdist

locations = {'door':Point(-8.18,-3.16,0.0), 'bigtankfront': Point(-4.07,-7.24,0.0), 'bigtankside':Point(-7.25,-5.26,0.0), 'tank1top': Point(-0.49,-3.51,0.0), 'tank1right': Point(2.30,-1.93,0.0), 'tank1bottom': Point(5.48,-3.48,0.0), 'tank2top': Point(-0.47,-6.52,0.0), 'tank2left': Point(1.98,-7.88,0.0), 'tank2bottom': Point(5.36,-6.31,0.0), 'tankset': Point(6.80,-5.69,0.0), 'pipes': Point(7.79,-2.67,0.0), 'dangerroom': Point(1.30,2.20,0.0), 'stairs': Point(2.94,8.56,0.0)}

class GoalPub:
    def __init__(self):
        self.pub = rospy.Publisher("nav_goals_test", Vector3, queue_size=10)
        rospy.init_node("nav_goals_pub",anonymous=True)
        rospy.loginfo("Started goal node")

    def send_goal(self,loc):
        goal = Vector3()
        goal.x =loc.x
        goal.y = loc.y
        goal.z = loc.z
        rospy.loginfo(goal)
        self.pub.publish(goal)

    def send_goals(self):
        locs = ['door','tank1top']
        for loc in locs:
            self.send_goal(locations[loc])
            

    def is_ready(self):
        try:
            rate = rospy.Rate(10)
            while not rospy.is_shutdown():
                connections = self.pub.get_num_connections()
                rospy.loginfo('Connections: %d', connections)
                if connections > 0:
                    return True
                rate.sleep()
        except rospy.ROSInterruptException as e:
            raise e
    
    


if __name__ == '__main__':
    try:
        gp = GoalPub()
        if gp.is_ready():
            gp.send_goals()
            
        
    except rospy.ROSInterruptException:
        pass

