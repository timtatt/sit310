#!/usr/bin/env python
import rospy as ros;

import tf_conversions as tfConversions;
import tf2_ros as tfRos;
import geometry_msgs.msg as geoMsgs;
from geometry_msgs.msg import Twist, Pose, Point, Quaternion, Vector3;
from nav_msgs.msg import Odometry;
import math;

x = 0;
y = 0;
th = 0.0;

odomPub = ros.Publisher('odom', Odometry, queue_size=50);

def handleZumoPos(velMsg):
	global x;
	global y;
	global th;

	print("x: ", x);
	print("y: ", y);
	print("t: ", th);

	vx = 0;

	if (velMsg.linear.y == 1.0):
		th += math.pi / 36;
	elif (velMsg.linear.y == -1.0):
		th -= math.pi / 36;
	elif (velMsg.linear.x == 1.0):
		vx = 0.1;
	elif (velMsg.linear.x == -1.0):
		vx = -0.1;

	deltaX = vx * math.cos(th);
	deltaY = vx * math.sin(th);

	x += deltaX;
	y += deltaY;

def publishTransform():
	global x;
	global y;
	global th;

	br = tfRos.TransformBroadcaster();

	t = geoMsgs.TransformStamped();
	t.header.stamp = ros.Time.now();
	t.header.frame_id = "odom";
	t.child_frame_id = "base_link";

	t.transform.translation.x = x;
	t.transform.translation.y = y;
	t.transform.translation.z = 0.0;

	q = tfConversions.transformations.quaternion_from_euler(0, 0, th);
	t.transform.rotation.x = q[0];
	t.transform.rotation.y = q[1];
	t.transform.rotation.z = q[2];
	t.transform.rotation.w = q[3];

	br.sendTransform(t);

def loop():
	odom = Odometry();

	q = tfConversions.transformations.quaternion_from_euler(0, 0, th);
	
	odom.header.frame_id = "odom";
	odom.pose.pose = Pose(Point(x, y, 0.0), Quaternion(*q));
	odom.child_frame_id = "base_link";
	odom.twist.twist = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0));
	
	currentTime = ros.Time.now();
	odom.header.stamp = currentTime;

	odomPub.publish(odom);
	publishTransform();

if __name__ == '__main__':
	ros.init_node('ZumoTFBroadcaster');
	ros.Subscriber('/zumo/cmd_vel', Twist, handleZumoPos);

	while not ros.core.is_shutdown():
		loop();
		ros.rostime.wallsleep(0.01);
