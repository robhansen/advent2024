#!/usr/bin/env python3

import sys

def get_unique_positions_of_guard(layout, position):
    direction_index = 0 # always starts facing up
    directions = [
        (-1,0),
        (0,1),
        (1,0),
        (0,-1)
    ]

    positions = {(position[0],position[1])} # set
    transitions = set() # for loop detection
    while True:
        next_pos = [position[0]+directions[direction_index][0], position[1]+directions[direction_index][1]]
        if next_pos[0]<0 or next_pos[0]>=len(layout) or next_pos[1]<0 or next_pos[1]>=len(layout[0]):
            return positions # leaving the map
        elif layout[next_pos[0]][next_pos[1]]: # is a barrier
            direction_index += 1 # turn right
            if direction_index>=len(directions):
                direction_index = 0
            continue

        transition = (position[0],position[1],next_pos[0],next_pos[1])
        if transition in transitions: # if we ever make the same move twice we're in a loop
            return None

        # actually do the move
        position = next_pos
        positions.add((position[0],position[1]))
        transitions.add(transition)

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

layout = []
position = [None,None]

with open(sys.argv[1]) as file:
    for i,line in enumerate(file.readlines()):
        row = []
        for j,char in enumerate(line.strip()):
            row.append(bool(char=="#"))
            if char=="^": # always starts facing up
                position = [i,j]
        layout.append(row)
positions_crossed = get_unique_positions_of_guard(layout, position)
print("The guard covered {} positions".format(len(positions_crossed)))

insertions_that_cause_loops = 0
# try inserting an obstacle at every location the guard normally crosses and see how many lead to loops
for insertion in positions_crossed:
    if not (position[0]==insertion[0] and position[1]==insertion[1]):
        layout[insertion[0]][insertion[1]] = True
        insertions_that_cause_loops += 1 if get_unique_positions_of_guard(layout, position) is None else 0
        layout[insertion[0]][insertion[1]] = False

print("Of those {} positions, there are {} where inserting an object causes a loop".format(len(positions_crossed), insertions_that_cause_loops))
