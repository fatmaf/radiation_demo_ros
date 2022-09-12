#!/usr/bin/env python
# displaying all locations

import math
import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray


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



class LocationMarkers(object):

    
    def __init__(self):
        rospy.init_node('location_markers')
        self.marker_pub = rospy.Publisher("visualization_marker_array",MarkerArray,queue_size=1)

    def create_loc_marker(self,point,m_id):
        marker = Marker()
        marker.header.frame_id="map"
        marker.header.stamp = rospy.Time(0)
        marker.ns = "locations"

        marker.type = Marker.SPHERE
        marker.id = m_id

        marker.action = Marker.ADD

        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2

        marker.color.r = 1.0
        marker.color.g = 0.2
        marker.color.b = 0.2
        marker.color.a = 0.75

        marker.pose.position.x = point.x
        marker.pose.position.y = point.y
        marker.pose.position.z = point.z
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0

        return marker

    def create_loc_text_marker(self,point,m_id,loc_name):
        marker = Marker()
        marker.header.frame_id="map"
        marker.header.stamp = rospy.Time(0)
        marker.ns = "location_names"

        marker.type = Marker.TEXT_VIEW_FACING
        marker.id = m_id

        marker.action = Marker.ADD

        marker.text = loc_name

        marker.scale.x = 0.5
        marker.scale.y = 0.5
        marker.scale.z = 0.5

        marker.color.r = 0.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        marker.pose.position.x = point.x
        marker.pose.position.y = point.y
        marker.pose.position.z = point.z
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0

        return marker

    
    def create_marker_array(self):
        locs = LOCATIONS
        locnum = 0
        markerArray = MarkerArray()
        
        for loc in locs:
            loc_pos = locs[loc]
            marker = self.create_loc_marker(loc_pos,locnum)
            #rospy.loginfo(marker)
            markerArray.markers.append(marker)
            marker_text = self.create_loc_text_marker(loc_pos,locnum+len(locs),loc)
            markerArray.markers.append(marker_text)
            locnum = locnum + 1

        return markerArray


    def publish_marker_array(self,markerArray):
        self.marker_pub.publish(markerArray)



    def publish_locations(self):
        markerArray = self.create_marker_array()
        #rospy.loginfo(markerArray)
        self.publish_marker_array(markerArray)


if __name__ == "__main__":

    try:
        locmarkers = LocationMarkers()
        while not rospy.is_shutdown():
            locmarkers.publish_locations()

    except rospy.ROSInterruptException:
        rospy.loginfo("shutting down")
        
        
        
            
            
            
        
        
        
