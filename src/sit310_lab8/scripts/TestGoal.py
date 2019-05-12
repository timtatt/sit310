#!/usr/bin/env python

import rospy as ros;

import actionlib;
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal;

def MoveBaseClient():
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction);
	client.wait_for_server();

	goal = MoveBaseGoal();
	goal.target_pose.header.frame_id = "odom";
	goal.target_pose.header.stamp = ros.Time.now();
	goal.target_pose.pose.position.x = 0;
	goal.target_pose.pose.position.y = 0;
	goal.target_pose.pose.orientation.w = 1.0;

	client.send_goal(goal);
	wait = client.wait_for_result();

	if not wait:
		ros.logerr('Action server not available');
		ros.signal_shutdown('Action server not available');
	else:
		return client.get_result();

if __name__ == '__main__':
	try:
		ros.init_node('TestGoalPy');
		result = MoveBaseClient();
		if result:
			ros.loginfo('Goal execution done');
	except ros.ROSInterruptException:
		ros.loginfo('Nav Test Finished');
