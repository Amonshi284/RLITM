# Imports
from pyniryo import *
import numpy as np

workspace_name = "ITM_TEST"  # "ITM-Test"  # Robot's Workspace Name
robot_ip_address = "192.168.0.228"  # "192.168.0.228"

robot = NiryoRobot(robot_ip_address)
robot.calibrate_auto()
robot.update_tool()
# Getting camera calibration
mtx, dist = robot.get_camera_intrinsics()

observation_pose = PoseObject(
    x=0.174, y=0, z=0.321,
    roll=2.985, pitch=1.408, yaw=2.975
)

#Rampe
pick_pose = PoseObject(
    x=0.153, y=0.21, z=0.166,
    roll=-0.125, pitch=1.185, yaw=-0.024,
)
# Place pose
place_pose = PoseObject(
    x=0.0, y=-0.2, z=0.085,
    roll=0.0, pitch=1.57, yaw=-1.57
)


positions = [
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.2, y_rel=0.2, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.5, y_rel=0.2, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.8, y_rel=0.2, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.2, y_rel=0.5, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.5, y_rel=0.5, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.8, y_rel=0.5, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.2, y_rel=0.8, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.5, y_rel=0.8, yaw_rel=0),
    robot.get_target_pose_from_rel(workspace_name, height_offset=0.005, x_rel=0.8, y_rel=0.8, yaw_rel=0)
]


def findstones(color, img_start):
    if str(color).casefold() == "red":
        img_threshold = threshold_hsv(img_start, *ColorHSV.RED.value)
    elif str(color).casefold() == "blue":
        img_threshold = threshold_hsv(img_start, *ColorHSV.BLUE.value)
    elif str(color).casefold() == "green":
        img_threshold = threshold_hsv(img_start, *ColorHSV.GREEN.value)
    else:
        img_threshold = threshold_hsv(img_start, *ColorHSV.ANY.value)

    img_open = morphological_transformations(img_threshold, morpho_type=MorphoType.OPEN,
                                             kernel_shape=(11, 11), kernel_type=KernelType.ELLIPSE)

    cnts = biggest_contours_finder(img_open, 9)

    img_contours = draw_contours(img_open, cnts)
    img_bary = img_contours
    stones = []
    barycenter = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, len(cnts)):
        barycenter[i] = get_contour_barycenter(cnts[i])
        img_bary = draw_barycenter(img_bary, barycenter[i][0], barycenter[i][1])
        stones.append((barycenter[i][0], barycenter[i][1]))

    return img_bary, stones


def checkspaces(stones, img, spcs):
    spcsizex = img.shape[0] / 3
    spcsizey = img.shape[1] / 3

    for stone in stones:
        if stone[0] < spcsizex:
            if stone[1] < spcsizey:
                spcs.append((0, 0))
            elif spcsizey <= stone[1] < spcsizey * 2:
                spcs.append((1, 0))
            elif spcsizey * 2 <= stone[1]:
                spcs.append((2, 0))
        elif spcsizex <= stone[0] < spcsizex * 2:
            if stone[1] < spcsizey:
                spcs.append((0, 1))
            elif spcsizey <= stone[1] < spcsizey * 2:
                spcs.append((1, 1))
            elif spcsizey * 2 <= stone[1]:
                spcs.append((2, 1))
        elif spcsizex * 2 <= stone[0]:
            if stone[1] < spcsizey:
                spcs.append((0, 2))
            elif spcsizey <= stone[1] < spcsizey * 2:
                spcs.append((1, 2))
            elif spcsizey * 2 <= stone[1]:
                spcs.append((2, 2))

    return spcs


def tictactoe_place(index):
    preposition = PoseObject(x=0.153, y=0.141, z=0.306, roll=-0.077, pitch=1.188, yaw=0.016,)
    pos = positions[index-1]
    robot.release_with_tool()
    robot.move_pose(preposition)
    robot.move_pose(pick_pose)
    robot.wait(0.1)
    robot.grasp_with_tool()
    robot.move_pose(preposition)
    # robot.vision_pick("ITM-Test", height_offset=0.005)
    robot.move_pose(observation_pose)
    robot.place_from_pose(pos)
    robot.move_pose(observation_pose)


def find_new_pos(pos):
    robot.move_pose(observation_pose)
    input("When done press enter")
    # Getting image
    img_compressed = robot.get_img_compressed()
    # Uncompressing image
    img_raw = uncompress_image(img_compressed)
    # Undistiorting image
    img_undistorted = undistort_image(img_raw, mtx, dist)
    workspace_found, res_img_markers = debug_markers(img_undistorted)
    if workspace_found:
        img_workspace = extract_img_workspace(img_undistorted, workspace_ratio=1.0)
    else:
        img_workspace = None

    img_stones, stones = findstones("any", img_workspace)
    spaces = []
    spaces = checkspaces(stones, img_workspace, spaces)
    newpos = []
    poscnt = 0
    for p in pos:
        for s in spaces:
            if p == s:
                newpos.append(p)
                poscnt += 1

    if poscnt == 1:
        return newpos[0]
    else:
        print("Too many or too few stones")
        return find_new_pos(pos)