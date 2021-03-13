#!/usr/bin/env python

import rospy
from ds4_driver.msg import Status
from arm_handler.msg import arm_msg
import math

class Arm_Goal(object):
    def __init__(self, publisher):

        self._pub = publisher
        self._goal_pose = {'L':0,'X':0,'T':0,'P':0}
        self.remap = {
            'axis_left_x':'L',
            'axis_left_y':'X',
            'axis_right_x':'T',
            'axis_right_y':'P'
        }

    def callback(self, msg):
        CUI_RES = 4096
        SCALE = 1
        input_vals = {}
        goal = arm_msg()
        for attr in self.remap.keys():
            read_val = getattr(msg, attr)

            tmp = self._goal_pose[self.remap[attr]] + SCALE*CUI_RES*read_val
            tmp = tmp   + CUI_RES/2
            tmp = math.floor(tmp%CUI_RES)

            goal.data = tmp
            goal.joint = ord(self.remap[attr])
            
            self._goal_pose[goal.joint] = tmp
            self._pub.publish(goal)


def main():

    rospy.init_node('dualshock_teleop')
    publisher = rospy.Publisher("arm_goal", arm_msg, queue_size=10)

    handle = Arm_Goal(publisher = publisher)

    rospy.Subscriber('status', Status, handle.callback, queue_size=10)
    rospy.spin()


if __name__ == '__main__':
    main()
