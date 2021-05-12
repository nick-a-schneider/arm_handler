#!/usr/bin/env python

import rospy
from ds4_driver.msg import Status
from arm_handler.msg import arm_msg
import math

class Arm_Goal(object):
    def __init__(self, publisher):

        self._pub = publisher
        self.joints = {
            'axis_left_x': 'L',
            'axis_left_y': 'X',
            'axis_right_x':'T',
            'axis_right_y':'P'
        }
        self.scale = {
            'axis_left_x':   0.15,
            'axis_left_y':   1,
            'axis_right_x':  1,
            'axis_right_y':  1
        }

    def callback(self, msg):
        PWM_RES = 255
        input_vals = {}
        goal = arm_msg()
        for attr in self.joints.keys():
            read_val = getattr(msg, attr)
            goal.data = (PWM_RES+1) + PWM_RES*read_val*self.scale[attr]
            goal.joint = ord(self.joints[attr])
            self._pub.publish(goal)


def main():

    rospy.init_node('dualshock_teleop')
    publisher = rospy.Publisher("arm_goal", arm_msg, queue_size=10)

    handle = Arm_Goal(publisher = publisher)

    rospy.Subscriber('status', Status, handle.callback, queue_size=10)
    rospy.spin()


if __name__ == '__main__':
    main()
