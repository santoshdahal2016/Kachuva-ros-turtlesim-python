#!/usr/bin/env python

# Planner for autonomous vehicle Intersection navigation

# Author:
# Min CHEN

# cs6244: Robot Motion Planning

import  os  
import  sys  
import rospy 
import pygame 
from pygame.locals import * 
from geometry_msgs.msg import Twist


class teleop_kachuva:
	def __init__(self):
		self.init()

	def init(self):
		pygame.init()
		clock = pygame.time.Clock()
		screen = pygame.display.set_mode((250, 250))

		rospy.init_node('teleop_kachuva')
		self.rate = rospy.Rate(rospy.get_param('~hz', 20)) 
		self.acc = rospy.get_param('~acc', 2)
		self.yaw = rospy.get_param('~yaw', 0.5)

		self.robot_pub = rospy.Publisher('kachuva/cmd_vel', Twist, queue_size=1)

		print "Usage: \n \
				up arrow: accelerate \n \
				down arrow: decelerate \n \
				left arrow: turn left \n \
				right arrow: turn right"

	def send_highway_start(self, state):
		msg = RecordState()
		msg.state = state
		self.highway_game_start_pub.publish(msg)

	def keyboard_loop(self):
		while not rospy.is_shutdown():
			acc = 0
			yaw = 0
			pygame.event.wait()
			keys = pygame.key.get_pressed()
			for event in pygame.event.get():
				if event.type==pygame.QUIT:sys.exit()

			if(keys[pygame.K_UP]):
				acc = self.acc
				self.send_control(acc, yaw)

			elif(keys[pygame.K_DOWN]):
				acc = -self.acc
				self.send_control(acc, yaw)

			if(keys[pygame.K_LEFT]):
				self.send_control(acc, yaw)
				yaw = self.yaw

			elif(keys[pygame.K_RIGHT]):
				yaw = -self.yaw
				self.send_control(acc, yaw)


			self.rate.sleep()  


	def send_control(self, vel, yaw):
		vel_msg = Twist()
		vel_msg.linear.x = vel
		vel_msg.angular.z = yaw
		self.robot_pub.publish(vel_msg)


if __name__=='__main__':
	teleop_agent = teleop_kachuva()
	teleop_agent.keyboard_loop()	