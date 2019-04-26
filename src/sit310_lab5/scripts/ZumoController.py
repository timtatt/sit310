#!/usr/bin/env python

import rospy as ros;
from std_msgs.msg import Int8;
from geometry_msgs.msg import Twist;
from pynput import keyboard;
import getpass;

ros.init_node('ZumoController', anonymous=True);
pub = ros.Publisher('/zumo/cmd_vel', Twist, queue_size=10);

keyboardControlsEnabled = True;

def onRelease(key):
	# Ability to toggle keyboard listening
	if (not keyboardControlsEnabled):
		if (key == keyboard.Key.alt_l):
			raise StopException;
		return;

	vel_msg = Twist();
	vel_msg.linear.x = 0;
	vel_msg.linear.y = 0;
	vel_msg.linear.z = 0;
	vel_msg.angular.x = 0;
	vel_msg.angular.y = 0;
	vel_msg.angular.z = 0;
	
	if (key == keyboard.Key.up):
		print("Up");
		vel_msg.linear.x = 1;
	elif (key == keyboard.Key.down):
		print("Down");
		vel_msg.linear.x = -1;
	elif (key == keyboard.Key.left):
		print("Left");
		vel_msg.linear.y = 1;
	elif (key == keyboard.Key.right):
		print("Right");
		vel_msg.linear.y = -1;	
	pub.publish(vel_msg);

def onPress(key):
	global keyboardControlsEnabled;
	if (key == keyboard.Key.alt_r):
		keyboardControlsEnabled ^= True;


with keyboard.Listener(on_release=onRelease, on_press=onPress) as listener:
	listener.join();
	listener.start();
