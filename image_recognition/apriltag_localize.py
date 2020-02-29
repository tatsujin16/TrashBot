! /usr/bin/env python

import rospy
import numpy as np
import math
import tf
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from apriltag_ros.msg import AprilTagDetectionArray

class Tag_listener(object):
  def __init__(self):
    self._pub_tag0 = rospy.Publisher('/tag0_info', Twist, queue_size=1)
    self._pub_tag1 = rospy.Publisher('/tag1_info', Twist, queue_size=1)
    #self._pub_localize = rospy.Publisher('/robot_position', Twist, queue_size=1)
    self._sub_tag = rospy.Subscriber('/tag_detections', AprilTagDetectionArray, self._callback_tag)
    #self._tag0_position = np.zeros(4, dtype = 'float64')
    #self._tag1_position = np.zeros(4, dtype = 'float64')
    self._tag_position = np.zeros(4, dtype = 'float64')
    self._listener = tf.TransformListener()

  def _callback_tag(self, message):
    if len(message.detections) > 0:
      angle_q = message.detections[0].pose.pose.pose.orientation
      angle_e = self._angle_conversion([angle_q.x,angle_q.y,angle_q.z,angle_q.w])
      self._tag_position[0] = message.detections[0].pose.pose.pose.position.x
      self._tag_position[1] = message.detections[0].pose.pose.pose.position.y
      self._tag_position[2] = message.detections[0].pose.pose.pose.position.z
      self._tag_position[3] = math.degrees(angle_e[2])

      #rospy.loginfo("x : %s",self._tag_position[0])
      #rospy.loginfo("y : %s",self._tag_position[1])
      #rospy.loginfo("z : %s",self._tag_position[2])
      try:
        (position,angle) = self._listener.lookupTransform('tag0', 'usb_cam', rospy.Time(0))
        print 'position:',position
        euler = self._angle_conversion([angle[0],angle[1],angle[2],angle[3]])
        roll = math.degrees(euler[0])
        pitch = math.degrees(euler[1])
        yaw = math.degrees(euler[2])
        print 'roll:',roll
        print 'pitch:',pitch
        print 'yaw:',yaw
    
        camera_angle = math.radians(90 - (180 + roll))

        camera_info = Twist()
        camera_info.angular.x = camera_angle
        camera_info.linear.z = position[2]
        self._pub_tag0.publish(camera_info)
      except: 
        pass
      try:
        (positionRobot,angleRobot) = self._listener.lookupTransform('tag1', 'usb_cam', rospy.Time(0))
        print 'positionRobot:',positionRobot
        eulerRobot = self._angle_conversion([angleRobot[0],angleRobot[1],angleRobot[2],angleRobot[3]])
        rollRobot = math.degrees(eulerRobot[0])
        pitchRobot = math.degrees(eulerRobot[1])
        yawRobot = math.degrees(eulerRobot[2])
        print 'rollRobot:',rollRobot
        print 'pitchRobot:',pitchRobot
        print 'yawRobot:',yawRobot

        rollRobot = math.radians(rollRobot)
        pitchRobot = math.radians(pitchRobot)
        yawRobot = math.radians(yawRobot)

        robot_info = Twist()
        robot_info.linear.x = positionRobot[0]
        robot_info.linear.y = positionRobot[1]
        robot_info.linear.z = positionRobot[2]
        robot_info.angular.x = rollRobot
        robot_info.angular.y = pitchRobot
        robot_info.angular.z = yawRobot
        self._pub_tag1.publish(robot_info)
      except:
        pass
    #except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        #print "error"

    else:
      print "nothing"

  def _angle_conversion(self,quaternion):
    #External parameters
    euler = tf.transformations.euler_from_quaternion(quaternion)    #change angle
    return euler

if __name__ == '__main__':
  rospy.init_node('APRILTAG_TF')
  tag_listener = Tag_listener()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    pass

