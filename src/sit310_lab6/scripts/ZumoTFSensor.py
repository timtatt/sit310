#!/usr/bin/env python

import sys;
import rospy as ros;
import math;
from time import sleep;
import tf;

import tf2_ros as tfRos;
import tf2_msgs.msg as tfMsgs;
import tf_conversions as tfConvert;

from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud as doTransformCloud;
from sensor_msgs.msg import PointCloud2;
import std_msgs.msg as stdMsg;
from std_msgs.msg import Int8;
import sensor_msgs.point_cloud2 as pcl2;
import geometry_msgs.msg as geoMsg;

wallLeft, wallRight, wallFrontLeft, wallFrontRight = 0, 0, 0, 0;

transX, transY, transZ = 0, 0, 0;
rotX, rotY, rotZ, rotW = 0, 0, 0, 0;

def publishWalls():
	cloudPoints = [];
	
	#if (wallLeft > 0):
		#cloudPoints.append([0.5, -13.0 / wallLeft, 0.5]);
		#print("Object on Left");
		
	#if (wallRight > 0):
		#cloudPoints.append([0.5, 13.0 / wallRight, 0.5]);
		#print("Object on Right");
		
	if (wallFrontLeft > 0):
		cloudPoints.append([13.0 / wallFrontLeft, 0.5, 0.5]);
		#print("Object at Front");
	
	if (wallFrontRight > 0):
		cloudPoints.append([13.0 / wallFrontRight, -0.5, 0.5]);
		#print("Object at Front");
		
	header = stdMsg.Header();
	header.stamp = ros.Time.now();
	header.frame_id = 'world';
	
	myPointCloud = pcl2.create_cloud_xyz32(header, cloudPoints);
	
	t = geoMsg.TransformStamped();
	t.header.stamp = ros.Time.now();
	t.header.frame_id = 'world';
	t.child_frame_id = 'zumo';
	t.transform.translation.x = transX;
	t.transform.translation.y = transY;
	t.transform.translation.z = transZ;
	t.transform.rotation.x = rotX;
	t.transform.rotation.y = rotY;
	t.transform.rotation.z = rotZ;
	t.transform.rotation.w = rotW;
	
	cloudOut = doTransformCloud(myPointCloud, t);
	pclPub.publish(cloudOut);

def handleZumoLeft(wallMsg):
	global wallLeft;
	wallLeft = wallMsg.data;
	publishWalls();
	
def handleZumoRight(wallMsg):
	global wallRight;
	wallRight = wallMsg.data;
	publishWalls();
	
def handleZumoFrontLeft(wallMsg):
	global wallFrontLeft;
	wallFrontLeft = wallMsg.data;
	publishWalls();
	
def handleZumoFrontRight(wallMsg):
	global wallFrontRight;
	wallFrontRight = wallMsg.data;
	publishWalls();
	
if __name__ == '__main__':
	pclPub = ros.Publisher("/zumo/objectcloud", PointCloud2, queue_size=10);
	ros.init_node('objectdetect_node');
	listener = tf.TransformListener();
	ros.sleep(1.0);
	ros.Subscriber('/zumo/prox_left', Int8, handleZumoLeft);
	ros.Subscriber('/zumo/prox_right', Int8, handleZumoRight);
	ros.Subscriber('/zumo/prox_front_left', Int8, handleZumoFrontLeft);
	ros.Subscriber('/zumo/prox_front_right', Int8, handleZumoFrontRight);
	rate = ros.Rate(10.0);
	
	while not ros.is_shutdown():
		try:
			(trans, rot) = listener.lookupTransform('/world', '/zumo', ros.Time(0));
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			continue;
		
		[transX, transY, transZ] = trans;
		[rotX, rotY, rotZ, rotW] = rot;
		
	ros.spin();
