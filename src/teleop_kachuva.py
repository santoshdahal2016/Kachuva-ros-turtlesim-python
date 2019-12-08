#!/usr/bin/env python

from __future__ import print_function

import rospy

from geometry_msgs.msg import Twist

# termios : Low-level terminal control interface.

import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
        i     
   j    k    l


anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""

moveBindings = {
		'i':(1,0,0,0),
		'l':(0,0,0,1),
		'j':(0,0,0,-1),
		'k':(-1,0,0,0),
	}

speedBindings={
		'q':(1.1,1.1),
		'z':(.9,.9),
		'w':(1.1,1),
		'x':(.9,1),
		'e':(1,1.1),
		'c':(1,.9),
	}

def getKey():
	# Change the mode of the file descriptor fd to raw.
	# The tty module defines functions for putting the tty into cbreak and raw modes.
	# tty.setraw set stdin to raw mode
	# File descriptor is a low-level concept, it's an integer that represents an open file. Each open file is given a unique file descriptor.
	# sys.stdin.fileno() => 0
	tty.setraw(sys.stdin.fileno())

	# select.select(rlist, wlist, xlist[, timeout])
	# Select stdin for getting input
	select.select([sys.stdin], [], [], 0)

	# read 1 byte from STDIN
	key = sys.stdin.read(1)

	# tcsetattr(int fildes, int optional_actions,const struct termios *termios_p)
	# If optional_actions is TCSANOW, the change shall occur immediately.
	# If optional_actions is TCSADRAIN, the change shall occur after all output written to fildes is transmitted. This function should be used when changing parameters that affect output.
	# If optional_actions is TCSAFLUSH, the change shall occur after all output written to fildes is transmitted, and all input so far received but not read shall be discarded before the change is made.
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
	return key


def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
	old_settings = termios.tcgetattr(sys.stdin)

	pub = rospy.Publisher('kachuva/cmd_vel', Twist, queue_size = 1)
	rospy.init_node('teleop_kachuva')

	speed = rospy.get_param("~speed", 0.5)
	turn = rospy.get_param("~turn", 1.0)
	x = 0
	y = 0
	z = 0
	th = 0
	status = 0

	try:
		print(msg)
		print(vels(speed,turn))
		while(1):
			key = getKey()
			
			# if key == 27:
			# 	exit()
			if key in moveBindings.keys():
				x = moveBindings[key][0]
				y = moveBindings[key][1]
				z = moveBindings[key][2]
				th = moveBindings[key][3]
			elif key in speedBindings.keys():
				speed = speed * speedBindings[key][0]
				turn = turn * speedBindings[key][1]

				print(vels(speed,turn))
				if (status == 14):
					print(msg)
				status = (status + 1) % 15
			else:
				x = 0
				y = 0
				z = 0
				th = 0
				if (key == '\x03'):
					break

			twist = Twist()
			twist.linear.x = x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th*turn
			pub.publish(twist)

	except Exception as e:
		print(e)

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)