#!/usr/bin/env python

import rospy as ros;
from std_msgs.msg import Int8;
from geometry_msgs.msg import Twist;
import time;
import sys;
import os;

currentTopic = 1;

ros.init_node('ZumoObjectAvoid', anonymous=True);
pub = ros.Publisher('/zumo/3/cmd_vel', Twist, queue_size=10);
sensorData = {
	"frontLeft": 0,
	"frontRight": 0,
	"right": 0,
	"left": 0,
};

def turnLeft():
	velMsg = Twist();
	velMsg.linear.x = 0;
	velMsg.linear.y = 1.0;
	velMsg.linear.z = 0;
	velMsg.angular.x = 0;
	velMsg.angular.y = 0;
	velMsg.angular.z = 0;
	pub.publish(velMsg);

def turnRight():
	velMsg = Twist();
	velMsg.linear.x = 0;
	velMsg.linear.y = -1.0;
	velMsg.linear.z = 0;
	velMsg.angular.x = 0;
	velMsg.angular.y = 0;
	velMsg.angular.z = 0;
	pub.publish(velMsg);


def frontLeftSensor(wallMsg):
	global sensorData;
	sensorData['frontLeft'] = wallMsg.data;
	processSensorData();
	
def frontRightSensor(wallMsg):
	global sensorData;
	sensorData['frontRight'] = wallMsg.data;
	processSensorData();

def leftSensor(wallMsg):
	global sensorData;
	sensorData['left'] = wallMsg.data;
	processSensorData();

def rightSensor(wallMsg):
	global sensorData;
	sensorData['right'] = wallMsg.data;
	processSensorData();
	
	
def processSensorData():
	global currentTopic;
	global sensorData;
	
	if (sensorData['frontLeft'] > 6 or sensorData['frontRight'] > 6):
		if (sensorData['right'] <= 6):
			newTopic = 3;
			turnRight();
		elif (sensorData['left'] <= 6):
			newTopic = 3;
			turnLeft();
		else:
			newTopic = 2;
	else:
		newTopic = 1;
	
	if (currentTopic != newTopic):
		os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/" + str(newTopic) + "/cmd_vel");
		currentTopic = newTopic;
		
ros.Subscriber('/zumo/prox_front_left', Int8, frontRightSensor);
ros.Subscriber('/zumo/prox_front_right', Int8, frontLeftSensor);
ros.Subscriber('/zumo/prox_left', Int8, leftSensor);
ros.Subscriber('/zumo/prox_right', Int8, rightSensor);

os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel");
currentTopic = 1;
ros.spin();
