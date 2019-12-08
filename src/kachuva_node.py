#!/usr/bin/env python
# Ros related import
import rospy
import rospkg
from geometry_msgs.msg import Twist

# GUI related import
import pygame

# Time calculation
import time

# Math function for calculating trajectory
from math import *

# Color RGB Values
red = (200, 0, 0)
blue = (0, 0, 255)
green = (0, 155, 0)
yellow = (155, 155, 0)
white = (255, 255, 255)
black = (0, 0, 0) 



# Variable for storing Linear , angular and last command time(Command are runned for 1 Second)
lin_vel = 0.0
ang_vel = 0.0
last_command_time_ = time.time()

# Variable for storing robot position and orientation
robot_x = 320
robot_y = 240
robot_orient = 0


# pygames initialization and settings
pygame.init()
pygame.display.set_caption("kachuva")
robot = pygame.image.load(rospkg.RosPack().get_path('kachuva')+ "/images/car60_40.png")
screen = pygame.display.set_mode((640,480))



def kachuva_node():
	rospy.init_node('kachuva', anonymous=False)
	rate = rospy.Rate(10) # 10hz
	rospy.Subscriber("kachuva/cmd_vel", Twist,velocityCallback)


	while not rospy.is_shutdown():
		screen.fill(white)
		update()
		pygame.display.flip()
		rate.sleep()


def velocityCallback(vel):
	global lin_vel, ang_vel ,last_command_time_
	last_command_time_ = time.time()
	lin_vel = vel.linear.x
	ang_vel = vel.angular.z

def update():
	global robot_x , robot_y,lin_vel,ang_vel,robot_orient
	if (time.time() - last_command_time_ > 1):
		lin_vel = 0.0
		ang_vel = 0.0
	robot_x = robot_x + lin_vel*cos(robot_orient*pi/180)
	robot_orient = robot_orient + ang_vel
	#sin value 0degree->0 , 90degree->1, 180degree->0
	#we must pass degree in radian
	robot_y = robot_y - lin_vel*sin(robot_orient*pi/180)
	img = pygame.transform.rotate(robot, robot_orient)

	screen.blit(img,(robot_x,robot_y))


if __name__ == '__main__':
	try:
		kachuva_node()
	except rospy.ROSInterruptException:
		pass