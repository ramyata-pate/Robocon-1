#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
import math
from dynamic_reconfigure.server import Server
from final_nodes.cfg import pid_paramConfig
lastError = 0
baseRPM = 250
PWMFL_cal = baseRPM 
PWMFR_cal = baseRPM 
PWMRL_cal = baseRPM 
PWMRR_cal = baseRPM 
def callback(config, level):
    rospy.loginfo("""Reconfiugre Request: {kp}, {kd}""".format(**config))
    return config
def callb(error):
	rpm = Kp * error.data + Kd * (error.data - lastError)
	lastError = error
	finalrpm=(rpm-(-4000))*(255-(-255))/(4000-(-4000)) + (-255)
	if(error.data>=0):
		pwmFL=PWMFL_cal
		pwmFR=PWMFR_cal + abs(finalrpm)
		pwmRL=PWMRL_cal + abs(finalrpm)
		pwmRR=PWMRR_cal
	else:
		pwmFL=PWMFL_cal + abs(finalrpm)
		pwmFR=pwmFR_cal
		pwmRL=PWMRL_cal 
		pwmRR=PWMRR_cal +abs(finalrpm)
		vel=[pwmFL,pwmFR,pwmRL,pwmRR]
	pub1.publish(vel)

def func1():
	pub1=rospy.Publisher('vel_topic',Float64MultiArray,queue_size=10)
	rospy.init_node('control_node', anonymous = True)
	srv = Server(pid_paramConfig, callback)
	rospy.Subscriber('error_topic', Float64, callb)
	rospy.spin()


if __name__=='__main__':
	func1()