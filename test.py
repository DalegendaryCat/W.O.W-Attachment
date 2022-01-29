from urx import Robot
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

rob = Robot("192.168.1.5")

grip = Robotiq_Two_Finger_Gripper(rob)

def movehome():
    rob.movej((0, -1.57, -1.57, -1.57, 1.57, 1.57), 0.4, 0.3)

def movehomesideways():
    rob.movej((0, -1.57, -1.57, -1.57, 1.57, 0), 0.4, 0.3)

def movearcfold(pose_a, pose_b):
    grip.close_gripper()
    rob.movec(pose_a, pose_b, 0.2, 0.2)

movehome()

value = 0.3 #input
rob.translate((0.38, 0, -0.38), 0.1, 0.1) #forward
pose_fi = rob.get_pose().pose_vector
pose_ff = rob.get_pose().pose_vector

print(rob.getl())

grip.gripper_action(128)

grip.close_gripper()
rob.movel((0.7, -0.17395463326938498, 0.3, -0.0013366219951001586, 3.1400000708539193, 0.0035162987187208157), .2, .2)
rob.movel((0.55, -0.17395463326938498, 0.15, -0.0013366219951001586, 3.1400000708539193, 0.0035162987187208157), .2, .2)
rob.movel((0.7, -0.17395463326938498, 0.3, -0.0013366219951001586, 3.1400000708539193, 0.0035162987187208157), .2, .2)
grip.open_gripper()
"""
#move fold
while pose_ff[2] < value:
    pose_ff[0] += 0.1 #finetune later
    pose_ff[2] += 0.1
    movearcfold(pose_fi, -pose_ff)

#move unfold
pose_fi = rob.get_pose().pose_vector
pose_ff = rob.get_pose().pose_vector
while pose_ff[0] != pose_fi[0]:
    pose_ff[0] -= 0.1
    pose_ff[2] -= 0.1
    movearcfold(pose_fi, pose_ff)

"""

rob.close()