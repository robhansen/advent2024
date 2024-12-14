#!/usr/bin/env python3

import sys
import re
import math

if len(sys.argv) != 5:
    print("Help: {} <filename> <steps> <width> <height>".format(sys.argv[0]))
    sys.exit(0)

STEPS = int(sys.argv[2])
WIDTH = int(sys.argv[3])
HEIGHT = int(sys.argv[4])

class Robot:
    def __init__(self, value_strings, width, height):
        self.position = self.parse(value_strings[0])
        self.velocity = self.parse(value_strings[1])
        self.width = width
        self.height = height

    def parse(self, value_string):
        return [int(x) for x in value_string.split(",")]

    def _step_linear(self, start, delta, maximum):
        return (start + delta) % maximum
    def step(self):
        self.position[0] = self._step_linear(self.position[0], self.velocity[0], self.width)
        self.position[1] = self._step_linear(self.position[1], self.velocity[1], self.height)

    def is_left(self):
        return (self.position[0] < int((self.width-1)/2))
    def is_right(self):
        return (self.position[0] > int((self.width-1)/2))
    def is_upper(self):
        return (self.position[1] < int((self.height-1)/2))
    def is_lower(self):
        return (self.position[1] > int((self.height-1)/2))

def find_adjacent(positions,current_position,adjacent):
    directions = ((0,1),(1,0),(0,-1),(-1,0)) 
    for direction in directions:
        next_position = (current_position[0]+direction[0],current_position[1]+direction[1])
        if next_position not in adjacent and next_position in positions:
            adjacent.add(next_position)
            adjacent = find_adjacent(positions,next_position,adjacent)
    return adjacent

def display_positions(positions):
    print(positions)
    for y in range(HEIGHT):
        line = ""
        for x in range(WIDTH):
            line += "X" if (x,y) in positions else "."
        print(line)

robots = []
with open(sys.argv[1]) as file:
    for line in file:
        robots.append(Robot(re.findall(r'[\d,-]+', line), WIDTH, HEIGHT))

# assume that the christmas tree will be a big shaped blob and hence will be the largest contiguous group to be seen
largest_contigous_group_seen = 1
second_at_which_largest_contigous_group_seen = 0
positions_at_which_largest_contigous_group_seen = []

for i in range(STEPS):
    for robot in robots:
        robot.step()
    
    in_contigious_group = set()
    largest_contiguous_group = 1
    positions = [tuple(x.position) for x in robots] # convert to tuple so it's hashable
    for position in positions:
        if position not in in_contigious_group:
            contigous_group = {position}
            contigous_group = find_adjacent(positions, position, contigous_group)
            if len(contigous_group) > largest_contiguous_group:
                largest_contiguous_group = len(contigous_group)
    if largest_contiguous_group > largest_contigous_group_seen:
        largest_contigous_group_seen = largest_contiguous_group
        second_at_which_largest_contigous_group_seen = i+1
        positions_at_which_largest_contigous_group_seen = positions

display_positions(positions_at_which_largest_contigous_group_seen)
print("After {} seconds there is a contigous cluster of {} robots, which may or may not look like a Christmas tree (see above)...".format(second_at_which_largest_contigous_group_seen, largest_contigous_group_seen))

quadrants = [0,0,0,0]
for robot in robots:
    quadrants[0] += 1 if robot.is_left() and robot.is_upper() else 0
    quadrants[1] += 1 if robot.is_right() and robot.is_upper() else 0
    quadrants[2] += 1 if robot.is_left() and robot.is_lower() else 0
    quadrants[3] += 1 if robot.is_right() and robot.is_lower() else 0

print("The count of robots in the quadrants after {} steps is {}, total safety factor {}".format(STEPS, quadrants, math.prod(quadrants)))
