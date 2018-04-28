import sys
import math
import numpy as np


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
    dist_discount = min(1.0, distance/dist_thres)
    return int(in_thrust * dist_discount)

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
used_boost = False
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in raw_input().split()]
    opponent_x, opponent_y = [int(i) for i in raw_input().split()]

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."
    if next_checkpoint_angle >= 90 or next_checkpoint_angle <= -90:
        thrust = 20
    else:
        # thrust = 100
        thrust = compute_thrust(next_checkpoint_angle, next_checkpoint_dist)
        thrust = adjust_by_distance(thrust, next_checkpoint_dist)
        
    if not used_boost and abs(next_checkpoint_angle) < 10 and next_checkpoint_dist > angle_dist_thres:
        thrust = 'BOOST'
        used_boost = True

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + \
            str(thrust)
