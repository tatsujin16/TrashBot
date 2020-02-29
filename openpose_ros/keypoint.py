#! /usr/bin/env python

import rospy
import math
import numpy as np
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
from openpose_ros_msgs.msg import OpenPoseHumanList

class ros_openpose(object):
  def __init__(self):
    self._pub_keypoint = rospy.Publisher('/keypoint_position', Twist, queue_size=1)
    self._sub_skeleton = rospy.Subscriber('/openpose_ros/human_list', OpenPoseHumanList, self._callback)
    self._sub_slackbot = rospy.Subscriber('/ignition_command', Int16, self._callback_slackbot)
    self._sub_tag0 = rospy.Subscriber('/tag0_info', Twist, self._callback_tag0)
    self._cam_height = 0
    self._cam_angle = 0
    self._flagHanding = False
    self._flagThrowing = False
    self._radiusHanding = 0.4688
    self._radiusThrowing = 1.5467
    #self._count = 0
    #self._prev = 0

  def _callback_slackbot(self, message):
    slack_command = message.data
    if slack_command == 1:
      self._flagHanding = True
    elif slack_command == 2:
      self._flagThrowing = True

  def _callback(self, message):
    #human = message.human_list[0].body_key_points_with_prob
    R_BigToe_y = message.human_list[0].body_key_points_with_prob[22].y
    R_Heel_y = message.human_list[0].body_key_points_with_prob[24].y
    L_BigToe_y = message.human_list[0].body_key_points_with_prob[19].y
    L_Heel_y = message.human_list[0].body_key_points_with_prob[21].y
    MidHip_x = message.human_list[0].body_key_points_with_prob[8].x
    #MidHip_y = message.human_list[0].body_key_points_with_prob[8].y
    #R_Shoulder_x = message.human_list[0].body_key_points_with_prob[2].x
    #R_Shoulder_y = message.human_list[0].body_key_points_with_prob[2].y
    #R_Elbow_x = message.human_list[0].body_key_points_with_prob[3].x
    #R_Elbow_y = message.human_list[0].body_key_points_with_prob[3].y
    #R_Wrist_x = message.human_list[0].body_key_points_with_prob[4].x
    #R_Wrist_y = message.human_list[0].body_key_points_with_prob[4].y

    #angle = self.arm_angle(R_Elbow_x, R_Elbow_y, R_Wrist_x, R_Wrist_y, R_Shoulder_x, R_Shoulder_y)
    #print 'arm_angle',angle  
    #diff = self.raise_hand_diff(MidHip_y, R_Wrist_y)
    #print 'diff',diff

    centerHuman_x = MidHip_x
    centerHumanR_y1 = R_BigToe_y
    centerHumanR_y2 = R_Heel_y
    centerHumanL_y1 = L_BigToe_y
    centerHumanL_y2 = L_Heel_y
    centerHumanR_y = (centerHumanR_y1 + centerHumanR_y2) / 2
    centerHumanL_y = (centerHumanL_y1 + centerHumanL_y2) / 2
    centerHuman_y = (centerHumanR_y + centerHumanL_y) / 2

    if self._flagHanding:
      image_x, image_y = self.screen_xy_conversion(centerHuman_x, centerHuman_y)
      field_x, field_y = self.camera_xy_conversion(image_x, image_y)
      print 'centerHuman_x',field_x, 'centerHuman_y',field_y
      centerHuman = Twist()
      centerHuman.linear.x = field_x
      centerHuman.linear.y = field_y
      centerHuman.linear.z = self._radiusHanding
      self._pub_keypoint.publish(centerHuman)
      self._flagHanding = False

    if self._flagThrowing:
      centerHuman_x = MidHip_x
      centerHuman_y1 = R_BigToe_y
      centerHuman_y2 = R_Heel_y
      centerHuman_y = (centerHuman_y1 + centerHuman_y2) / 2
      image_x, image_y = self.screen_xy_conversion(centerHuman_x, centerHuman_y)
      field_x, field_y = self.camera_xy_conversion(image_x, image_y)
      print 'centerHuman_x',field_x, 'centerHuman_y',field_y
      centerHuman = Twist()
      centerHuman.linear.x = field_x
      centerHuman.linear.y = field_y
      centerHuman.linear.z = self._radiusThrowing
      self._pub_keypoint.publish(centerHuman)
      self._flagThrowing = False

  def _callback_tag0(self, message):
    self._cam_height = message.linear.z
    self._cam_angle = message.angular.x

  def screen_xy_conversion(self, x, y):
    screen_width = 640
    screen_height = 480
    # direction_y is reversed 
    x_reverse = x
    y_reverse = screen_height - y
    # starting_point_o is shifted
    x_shift = x_reverse - (screen_width / 2)
    y_shift = y_reverse - (screen_height / 2)
    return x_shift, y_shift

  def camera_xy_conversion(self, x, y):
    # fx = 663.057681
    fy = 660.562556
    f = fy
    h = self._cam_height + 0.04
    cam_theta = self._cam_angle
    xi = abs(x)
    yi = abs(y)
    delta_theta = math.atan2(yi, f)

    if(y <= 0.0):
      theta = cam_theta + delta_theta
    elif(y > 0.0):
      theta = cam_theta - delta_thet
      
    yt = h / np.tan(theta)
    f_dash = np.sqrt(f*f + yi*yi)
    xt = (xi * np.sqrt(yt*yt + h*h)) / f_dash
    if(x < 0.0):
      xt = xt * (-1)
    return xt, yt

  #def arm_angle(self, x0, y0, x1, y1, x2, y2):
    #a1 = x1 - x0
    #a2 = y1 - y0
    #b1 = x2 - x0
    #b2 = y2 - y0
    #cos = (a1*b1 + a2*b2) / ((np.sqrt(a1*a1 + a2*a2)) * (np.sqrt(b1*b1 + b2*b2)))
    #return cos

  #def raise_hand_diff(self, y0, y1): 
    #diff = y0 - y1
    #self._count = self._count + 1
    #if self._count % 11 == 1:
      #self._prev = diff
    #if self._count % 11 == 0:
      #if self._prev < diff - 30:
        #print 'hand is raised!'
    #return diff

if __name__ == '__main__':
  rospy.init_node('OPENPOSE_KEY')
  ros_openpose = ros_openpose()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    pass
