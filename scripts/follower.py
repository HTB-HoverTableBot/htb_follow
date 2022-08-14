#!/usr/bin/env python

import time
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from visualization_msgs.msg import Marker
from std_msgs.msg import Float32
from tf.transformations import quaternion_from_euler

#define function/functions to provide the required functionality

class Follower():
    def __init__(self):

        rospy.init_node('htb_follower_node')

        self.sub=rospy.Subscriber('scan', LaserScan, self.laser_callback)
        self.pub=rospy.Publisher('/hoverboard_velocity_controller/cmd_vel', Twist, queue_size=10)
        self.arrow_pub=rospy.Publisher('/arrow_marker', Marker, queue_size=1)
        self.yaw_pub=rospy.Publisher('/yaw', Float32, queue_size=1)
        self.index_pub=rospy.Publisher('/index', Float32, queue_size=1)

        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

        self.qx = 0.0
        self.qy = 0.0
        self.qz = 0.0
        self.qw = 0.0
        self.i_prev = 0

        time.sleep(4)

    def laser_callback(self, msg):
        range_min = 100.0
        index_min = 0
        measurements = len(msg.ranges)

        for i,data in enumerate(msg.ranges):
            if  data > 0.50 and data < range_min and (i > 1000 or i < 120):
                range_min = data
                index_min = i
        rospy.loginfo("min %6.3f at %d", range_min, index_min)
        self.index_pub.publish(index_min)

        if index_min != self.i_prev:
            self.i_prev = i
        else:
            index_min = 500


        self.yaw = index_min * 2 * 3.1415 / 1147
        self.yaw_pub.publish(float(self.yaw))

        (self.qx, self.qy, self.qz, self.qw) = quaternion_from_euler(self.roll, self.pitch, self.yaw)

        if self.yaw < 0.54:
            turn = .2 * (400-index_min)/(800)
            rospy.loginfo("Turn left")
        elif self.yaw > 5.75:
            turn = -.2 * (index_min-800)/(800)
            rospy.loginfo("Turn right")
        else:
            turn = 0
            forward = 0
            rospy.loginfo("Stop")

        if range_min < 1.0:
            forward = -0.2 * (1.0-range_min)
        else:
            forward = 0.2 * (range_min-1.0)

        twist = Twist()
        twist.linear.x = forward
        twist.angular.z = turn
        self.pub.publish(twist)

        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "my_namespace"
        marker.id = 0
        marker.type = 0
        marker.pose.position.x = 0
        marker.pose.position.y = 0
        marker.pose.position.z = 0
        marker.pose.orientation.x = self.qx
        marker.pose.orientation.y = self.qy
        marker.pose.orientation.z = self.qz
        marker.pose.orientation.w = self.qw
        marker.scale.x = 1
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0

        self.arrow_pub.publish(marker)


if __name__=='__main__':

    follower = Follower()

    rospy.spin()
