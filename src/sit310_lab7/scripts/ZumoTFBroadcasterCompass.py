#!/usr/bin/env python
import rospy as ros;
import tf_conversions as tfConversions;
import tf2_ros as tfRos;
import geometry_msgs.msg as geoMsg;
from geometry_msgs.msg import Twist;
from std_msgs.msg import Int16;
import math;

x = 0;
y = 0;
th = 0.0;

def handleZumoHeading(headingMsg):
	global th;
	print(headingMsg.data);
	th = headingMsg.data * math.pi / 180;
	print(th);

def handleZumoPos(velMsg):
	global x;
	global y;
	global th;
	br = tfRos.TransformBroadcaster()
	t = geoMsg.TransformStamped();

	print("x: ", x);
	print("y: ", y);
	print("t: ", th);

	vx = 0;

	if (velMsg.linear.x == 1.0):
		vx = 0.1;
	elif (velMsg.linear.x == 1.0):
		vx = -0.1;

	deltaX = vx * math.cos(th);
	deltaY = vx * math.sin(th);
	deltaTh = 0;

	x += deltaX;
	y += deltaY;
	th += deltaTh;

	t.header.stamp = ros.Time.now();
	t.header.frame_id = "world";
	t.child_frame_id = "zumo";

	t.transform.translation.x = x;
	t.transform.translation.y = y;
	t.transform.translation.z = 0.0;

	q = tfConversions.transformations.quaternion_from_euler(0, 0, th);
	t.transform.rotation.x = q[0];
	t.transform.rotation.y = q[1];
	t.transform.rotation.z = q[2];
	t.transform.rotation.w = q[3];

	br.sendTransform(t);

if __name__ == '__main__':
	ros.init_node('ZumoTFBroadcaster');
	ros.Subscriber('/zumo/cmd_vel', Twist, handleZumoPos);
	ros.Subscriber('/zumo/heading', Int16, handleZumoHeading);
	ros.spin();

