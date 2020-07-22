#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from nxt_msgs.msg import Light
from geometry_msgs.msg import Twist


light_l = 0.0
light_r = 0.0
light_tresh = 0.0


def callback_light_l(data):
    
    global light_l
    light_l = data.intensity
    
    #rostopic echo
    #rospy.loginfo("left light: %s", light_l)def callback_light_r(data):
    
    global light_r
    light_r = data.intensity
    
    #rospy.loginfo("right light: %s", light_r)


def listener():
    
    rospy.init_node('light_control', anonymous=True)
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber("/light_l", Light, callback_light_l)
    rospy.Subscriber("/light_r", Light, callback_light_r)

    # INSERT CALIBRATION ROUTINE HERE
    light_tresh = 400.0

    # spin() simply keeps python from exiting until this node is
    stopped
    # rospy.spin()
    
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():

        if light_l > light_tresh and light_r > light_tresh:
            rospy.loginfo("front")
            vel_msg.linear.x = 0.04
            vel_msg.angular.z = 0
        
        elif light_l < light_tresh:
            rospy.loginfo("counter clockwise")
            vel_msg.linear.x = 0vel_msg.angular.z = 0.5
        
        elif light_r < light_tresh:
            rospy.loginfo("clockwise")
            vel_msg.linear.x = 0
            vel_msg.angular.z = -0.5
        
        else:
            rospy.loginfo("stop")
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
        
        pub.publish(vel_msg)
        rate.sleep()


if __name__ == '__main__':
    listener()
