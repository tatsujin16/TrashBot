#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
import numpy as np
import math

class ros_trashbot(object):
  def __init__(self):
    self._pub_trashbot = rospy.Publisher('/trashbot_command', Twist, queue_size=1)
    self._sub_keypoint = rospy.Subscriber('/keypoint_position', Twist, self._callback_keypoint)
    self._sub_tag = rospy.Subscriber('/tag1_info', Twist, self._callback_tag1)
    self._robot = np.zeros(3, dtype = 'float64')
    #self._robot_yaw = 0
    self._posture = np.zeros(3, dtype = 'float64')  
    self._radius = 0 

  def _callback_keypoint(self, message):
    self._keypoint_x = message.linear.x
    self._keypoint_y = message.linear.y
    self._radius = message.linear.z * 100 
    rospy.loginfo("keypoint : %s",self._keypoint_x)
    rospy.loginfo("keypoint : %s",self._keypoint_y)
    x, y = self.transform(self._keypoint_x, self._keypoint_y)
    print 'x:', x
    print 'y:', y
    theta = math.degrees(math.atan2(x, y)) 
    print 'theta',theta
    distance = np.sqrt(x*x + y*y)
    distance = distance * 100 - self._radius
    print 'L:',distance
    if distance >= 400:
      distance = 0 
    trashbot = Twist()
    trashbot.linear.x = distance
    trashbot.angular.z = theta
    self._pub_trashbot.publish(trashbot)
    
  def _callback_tag1(self, message):
    self._robot[0] = message.linear.x
    self._robot[1] = message.linear.y
    self._robot[2] = message.linear.z
    self._posture[0] = message.angular.x
    self._posture[1] = message.angular.y
    self._posture[2] = message.angular.z
    #print 'yaw_tag1',math.degrees(self._robot_yaw)
  
  def rotation_matrix(self, angle, robot_x, robot_y):
    rot = [[np.cos(angle),np.sin(angle),robot_x],[(-1)*np.sin(angle),np.cos(angle),robot_y]]
    rot = np.matrix(rot)
    return rot 

  def transform(self, kx, ky):
    angle = (-1) * self._posture[2]
    robot_x = self._robot[0]
    robot_y = self._robot[1]
    world_keypoint =  np.array([kx, ky,1])
    rot = self.rotation_matrix(angle, robot_x, robot_y)
    local_keypoint = np.dot(rot, world_keypoint.reshape(3,1))
    local_kx, local_ky = local_keypoint[0, 0], local_keypoint[1, 0]   
    return local_kx ,local_ky
  
if __name__ == '__main__':
  rospy.init_node('ROUTE_OF_ROBOT')
  ros_trashbot = ros_trashbot()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    pass
