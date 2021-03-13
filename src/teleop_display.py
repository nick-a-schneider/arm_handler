#!/usr/bin/env python
import sys
import time
import rospy
from arm_handler.msg import arm_msg

class reprint_subscriber:
    def __init__(self):
        self.pose = {'L':0,'X':0,'T':0,'P':0}

    def calback(self,msg):    
        self.pose[chr(msg.joint)] = msg.data    
        self.state_print()

    def state_print(self):
        waist = str(self.pose['L'])
        shoulder = str(self.pose['X'])
        elbow = str(self.pose['P'])
        wrist = str(self.pose['T'])
        joint_states =(
            " "*(19-len(waist))+waist+
            " "*(26-len(shoulder))+shoulder+
            " "*(26-len(elbow))+elbow+
            " "*(26-len(wrist))+wrist
        )
        sys.stdout.write("\r")
        sys.stdout.write(joint_states)
        sys.stdout.flush()     
len

def preamble():
    message = '''
    ===============================================================================

    UNC Asheville Lunabotics 2021 

    Dualshock4 ISO Excavator Teleoperation Node: 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


                Shoulder Down                              Elbow Out
                     ^                                         ^
                     |                                         |
                     |                                         |
      Waist <------- L -------> Waist           Wrist <------- R -------> Wrist
      Left           |          Right           Close          |          Open
                     |                                         |
                     v                                         v
                Shoulder Up                                 Elbow In


    ===============================================================================


    '''
    sys.stdout.write(message)
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    header = (
        " "*15+"waist:"+ 
        " "*20+"shoulder:"+ 
        " "*17+"elbow:"+
        " "*20+"wrist:"
    )
    sys.stdout.write(header)
    sys.stdout.write("\n")
    sys.stdout.flush()
    hbar = (
        (" "*15+"-"*10+" ")*4
    )
    sys.stdout.write(hbar)
    sys.stdout.write("\n")
    sys.stdout.flush()

def main():

    display = reprint_subscriber()
    preamble()
    rospy.init_node('teleop_display', anonymous=False)
    rospy.Subscriber('arm_goal', arm_msg, callback=display.calback)
    rospy.spin()
    sys.stdout.write("\n")
    sys.stdout.flush()


    
if __name__ == '__main__':
    main()
