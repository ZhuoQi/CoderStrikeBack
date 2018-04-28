import sys
import math
import numpy as np

class HoverCraftStatus:
    def __init__(self, x=0, y=0, next_x=0, next_y=0,
                 chkpt_dist=0, chkpt_angle=0, used_boost=False):
        self.update_status(x, y, next_x, next_y, chkpt_dist, chkpt_angle, used_boost)

    def update_status(self, x, y, next_x, next_y, chkpt_dist, chkpt_angle, used_boost=None):
        self.x = x
        self.y = y
        self.next_x = next_x
        self.next_y = next_y
        self.chkpt_dist = chkpt_dist
        self.chkpt_angle = chkpt_angle
        if used_boost is not None:
            self.used_boost = used_boost

# angle and distance based discount of thrust for optimum path
angle_dist_thres = 4000.0
def compute_thrust(angle, distance):
    dist_multiplier = min(1.0, distance/angle_dist_thres)
    angle_based_discount = float(angle)/90.0
    dist_adjusted_discount = max(0.0, angle_based_discount * dist_multiplier)
    return int(100.0*(1-dist_adjusted_discount))
    

# avoid overshooting the target
dist_thres = 2000.0
def adjust_by_distance(in_thrust, distance):
    dist_discount = min(1.0, (distance/dist_thres)**2)
    return int(in_thrust * dist_discount)


# optimize boost calculation to a specific location
def get_boost_to_loc(x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle, used_boost):
    if next_checkpoint_angle >= 90 or next_checkpoint_angle <= -90:
        thrust = 0
    else:
        # thrust = 100
        thrust = compute_thrust(next_checkpoint_angle, next_checkpoint_dist)
        thrust = adjust_by_distance(thrust, next_checkpoint_dist)

    if not used_boost and abs(next_checkpoint_angle) < 10 and next_checkpoint_dist > angle_dist_thres:
        thrust = 'BOOST'
        used_boost = True
    return used_boost, thrust


# game loop
used_boost = False
my_status = HoverCraftStatus()
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."
    my_status.update_status(x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle)
    used_boost, thrust = get_boost_to_loc(
        my_status.x, my_status.y, my_status.next_x, my_status.next_y,
        my_status.chkpt_dist, my_status.chkpt_angle, my_status.used_boost)
    my_status.used_boost = used_boost

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + \
            str(thrust))
