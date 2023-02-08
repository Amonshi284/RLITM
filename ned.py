# Imports
from pyniryo import *


workspace_name = "tictactoe"  # "ITM-Test"  # Robot's Workspace Name
robot_ip_address = "10.10.10.10"  # "192.168.0.228"

robot = NiryoRobot(robot_ip_address)
robot.calibrate_auto()

observation_pose = PoseObject(
    x=0.006, y=0.16, z=0.35,
    roll=0.25, pitch=1.57, yaw=1.6,
)

#Rampe
pick_pose = PoseObject(
    x=-0.168, y=0.124, z=0.167,
    roll=-0.021, pitch=1.184, yaw=1.697,
)
# Place pose
place_pose = PoseObject(
    x=0.0, y=-0.2, z=0.085,
    roll=0.0, pitch=1.57, yaw=-1.57
)


positions = [
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.07, y_rel=0.2, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.55, y_rel=0.2, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=1.0, y_rel=0.2, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.07, y_rel=0.45, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.55, y_rel=0.5, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=1.0, y_rel=0.45, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.05, y_rel=0.715, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.53, y_rel=0.715, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=1.0, y_rel=0.715, yaw_rel=0)
]


def tictactoe_place(index):
    preposition = PoseObject(x=-0.168, y=0.124, z=0.257, roll=-0.014, pitch=1.183, yaw=1.716,)
    pos = positions[index-1]
    robot.release_with_tool()
    robot.move_pose(preposition)
    robot.move_pose(pick_pose)
    robot.wait(0.1)
    robot.grasp_with_tool()
    robot.move_pose(preposition)
    #robot.vision_pick("ITM-Test", height_offset=0.005)
    robot.move_pose(observation_pose)
    robot.place_from_pose(pos)
    robot.move_pose(observation_pose)
