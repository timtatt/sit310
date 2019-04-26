#!/usr/bin/env python
import rospy;
from std_msgs.msg import Int8;
from geometry_msgs.msg import Twist;

rospy.init_node('scared_robot', anonymous=True);
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10);

def frontCallback(data):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %d', data.data);
        if (data.data > 4):
                vel_msg = Twist();
                vel_msg.linear.x = -2;

                vel_msg.linear.y = 0;
                vel_msg.linear.z = 0;
                vel_msg.angular.x = 0;
                vel_msg.angular.y = 0;
                vel_msg.angular.z = 0;
                pub.publish(vel_msg);

def leftCallback(data):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %d', data.data);
        if (data.data > 4):
                vel_msg = Twist();
                vel_msg.linear.x = 0;

                vel_msg.linear.y = 0;
                vel_msg.linear.z = 0;
                vel_msg.angular.x = 0;
                vel_msg.angular.y = 0;
                vel_msg.angular.z = -2;
                pub.publish(vel_msg);

def rightCallback(data):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %d', data.data);
        if (data.data > 4):
                vel_msg = Twist();
                vel_msg.linear.x = 0;
                vel_msg.linear.y = 0;
                vel_msg.linear.z = 0;
                vel_msg.angular.x = 0;
                vel_msg.angular.y = 0;
                vel_msg.angular.z = 2;
                pub.publish(vel_msg);

def listener():
        rospy.Subscriber('frontSensor', Int8, frontCallback);
        rospy.Subscriber('leftSensor', Int8, leftCallback);
        rospy.Subscriber('rightSensor', Int8, rightCallback);
        rospy.spin();

if __name__ == '__main__':
        print("running");
        listener();
                        
