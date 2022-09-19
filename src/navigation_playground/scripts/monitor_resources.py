#!/usr/bin/env python3

# this file has all the monitor resources 
# because I dont want to worry about launch files etc 
# this is obviously not the best way to do it 
# but I think it works 

import rospy
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseWithCovarianceStamped
from gazebo_radiation_plugins.msgs import Simulated_Radiation_Msg
from std_msgs.msg import String
from shared_python_code.GenerateAtNear import GenerateAtNear

class MonitorSub:
    
    def __init__(self):
        self.rad_sub = rospy.Subscriber("/radiation_sensor_plugin/sensor_0",Simulated_Radiation_Msg,self.rad_callback)
        self.pose_sub = rospy.Subscriber("amcl_pose",PoseWithCovarianceStamped,self.pose_callback)
        self.rad_status_pub = rospy.Publisher("radiation_status",String,queue_size= 10)
        self.pos_loc_pub = rospy.Publisher("at_location",String,queue_size=10)
        self.pos_loc_near_pub = rospy.Publisher("near_location",String,queue_size=10)
        self.radiation_value = None
        self.rad_status = None 
        
        self.start_node()
    
    def start_node(self):
        rospy.init_node("useful_topics_to_predicates")
        rospy.loginfo("Started node that converts radiation levels to status and pose information to at, near")
        self.rate = rospy.Rate(10)
        
    def rad_callback(self,data):
        if(self.radiation_value is None):
            self.radiation_value = data.value
        else:
            self.radiation_value = (self.radiation_value+data.value)/2
        if(self.radiation_value>=120):
            self.rad_status = "red";
        elif self.radiation_value >=90:
            self.rad_status = "orange"
        else:
            self.rad_status = "green"
            
    def pose_callback(self,data):
        x = data.pose.pose.position.x
        y = data.pose.pose.position.y 
        z = data.pose.pose.position.z
        
            
            
           
class PosePub:
    def __init__(self):
        self.pose = Vector3()
        self.sub = rospy.Subscriber("amcl_pose",PoseWithCovarianceStamped,self.get_pose)
        self.pub = rospy.Publisher("current_pose", Vector3, queue_size=10)
        rospy.init_node("pub_current_pose",anonymous=True)
        rospy.loginfo("Started pose node")
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)
        
    def get_pose(self,data):
        rospy.loginfo(data)
        self.pose = Vector3()
        self.pose.x = data.pose.pose.position.x
        self.pose.y = data.pose.pose.position.y
        self.pose.z = data.pose.pose.position.z
        rospy.loginfo("pose")
        rospy.loginfo(self.pose)
        rospy.loginfo("callback finished")
        
    def run(self):
        
        while not rospy.is_shutdown():
            self.pub.publish(self.pose)
            rospy.loginfo(self.pose)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        pp = PosePub()
        pp.run()
            
        
    except rospy.ROSInterruptException:
        pass
