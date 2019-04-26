#!/usr/bin/env python

import rospy as ros;
import tf_conversions;
import tf2_ros as tf;
import geometry_msgs.msg;
from geometry_msgs.msg import Twist;
import math;

x = 0;
y = 0;
th = 0.0;

def degToRad(deg):
	return math.pi * deg / 180;

def radToDeg(rad):
	return 180 * rad / math.pi;
		
def handleZumoPos(velMsg):
	global x;
	global y;
	global th;
	
	br = tf.TransformBroadcaster();
	t = geometry_msgs.msg.TransformStamped();
	
	vx = 0;
	if (velMsg.linear.y == 1.0):
		th += degToRad(5);
	elif (velMsg.linear.y == -1.0):
		th -= degToRad(5);
	elif (velMsg.linear.x == 1.0):
		vx = 0.1;
	elif (velMsg.linear.x == -1.0):
		vx = -0.1;
		
	deltaX = vx * math.cos(th);
	deltaY = vx * math.sin(th);
	deltaTh = 0;
		
	x += deltaX;
	y += deltaY;
	th += deltaTh;
	
	print("x:" + str(x));
	print("y:" + str(y));
	print("th:" + str(radToDeg(th)));
	
	t.header.stamp = ros.Time.now();
	t.header.frame_id = "world";
	t.child_frame_id = "zumo";
	
	t.transform.translation.x = x;
	t.transform.translation.y = y;
	t.transform.translation.z = 0.0;
	
	q = tf_conversions.transformations.quaternion_from_euler(0, 0, th);
	t.transform.rotation.x = q[0];
	t.transform.rotation.y = q[1];
	t.transform.rotation.z = q[2];
	t.transform.rotation.w = q[3];
	
	br.sendTransform(t);
	
if __name__ == '__main__':
	ros.init_node('ZumoTFBroadcaster');
	ros.Subscriber('/zumo/cmd_vel', Twist, handleZumoPos);
	ros.spin();
	
	
