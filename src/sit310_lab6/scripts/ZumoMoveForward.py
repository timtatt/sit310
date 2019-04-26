#!/usr/bin/env python

import rospy as ros;
from std_msgs.msg import Int8;
from geometry_msgs.msg import Twist;
import time;
import sys;

ros.init_node('ZumoMoveForward', anonymous=True);
pub = ros.Publisher('/zumo/1/cmd_vel', Twist, queue_size=10);

def moveForward(msg):
	velMsg = Twist();
	velMsg.linear.x = 1;
	velMsg.linear.y = 0;
	velMsg.linear.z = 0;
	velMsg.angular.x = 0;
	velMsg.angular.y = 0;
	velMsg.angular.z = 0;
	pub.publish(velMsg);
	time.sleep(0.1);

ros.Subscriber('/zumo/prox_front_left', Int8, moveForward);
ros.spin();
	
