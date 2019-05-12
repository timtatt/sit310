#!/usr/bin/env python

import rospy as ros;
from std_msgs.msg import Int8;
from geometry_msgs.msg import Twist;
import time;
import sys;
import os;

currentTopic = 1;

ros.init_node('ZumoObjectDetect', anonymous=True);
pub = ros.Publisher('/zumo/2/cmd_vel', Twist, queue_size=10);

def stop():
	velMsg = Twist();
	velMsg.linear.x = 0;
	velMsg.linear.y = 0;
	velMsg.linear.z = 0;
	velMsg.angular.x = 0;
	velMsg.angular.y = 0;
	velMsg.angular.z = 0;
	pub.publish(velMsg);

def handleZumoSensor(wallMsg):
	global currentTopic;
	
	if (wallMsg.data > 6):
		stop();

		
ros.Subscriber('/zumo/prox_front_left', Int8, handleZumoSensor);
ros.Subscriber('/zumo/prox_front_right', Int8, handleZumoSensor);

os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel");
currentTopic = 1;
ros.spin();
