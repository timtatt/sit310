#!/usr/bin/env python

import rospy as ros;
import tf_conversions;
import tf2_ros as tf;
import geometry_msgs.msg;
from geometry_msgs.msg import Twist;
import math;

velPub = ros.Publisher('/zumo/cmd_vel', Twist, queue_size=10);

def handleGoalPos(velMsg):
	if velMsg.linear.x != 0:
		velMsg.linear.x = 1.0 * (1 if velMsg.linear.x > 0 else -1);
	if velMsg.angular.z != 0:
		velMsg.linear.y = 1.0 * (1 if velMsg.angular.z > 0 else -1);
		velMsg.angular.z = 0;

	velPub.publish(velMsg);

if __name__ == '__main__':
	ros.init_node('ZumoUseGoal');
	ros.Subscriber('/cmd_vel', Twist, handleGoalPos);
	ros.spin();
	