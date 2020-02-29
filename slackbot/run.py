#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import json

from std_msgs.msg import Int16
from slackbot.bot import Bot 
from slackbot.bot import default_reply

@default_reply()
def default_func(message):
  if len(message.body['text']) > 0:
    phrase = message.body['text']
  elif len(message.body['attachments'][0]['pretext']) > 0:
    phrase = message.body['attachments'][0]['pretext']

  data = datatxt_to_array()
  num_of_lines = len(open('data.txt').readlines())
  compare_phrase_to_data(data, phrase, num_of_lines)
  print phrase
  message.reply(phrase)

def compare_phrase_to_data(data, phrase, num_of_lines):
  publish_done = False
  pub = rospy.Publisher('/ignition_command', Int16, queue_size=1)
  r = rospy.Rate(5)
  r.sleep()
  encoded_phrase = phrase.encode('utf-8')
  for num0 in range(num_of_lines):
    for num1 in range(3):
      try:
        Multi_array = data[num0][num1]
        if Multi_array in encoded_phrase:
          pub.publish(num0+1)
          publish_done = True
          raise Exception
      except Exception:
        break
    if publish_done:
      break
def datatxt_to_array():
  data =[] 
  f = open('data.txt','r')
  for line in f:
    line = line.strip()
    line = line.replace('\n','')
    line = line.split(",")
    data.append(line)
  f.close()
  return data

def main():
  bot = Bot()
  bot.run()

if __name__ == "__main__":
  rospy.init_node('SLACKBOT_TEXT_JUDGE')
  print('start slackbot')
  main()

