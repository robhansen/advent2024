#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

DIRECTIONS = ((0,1),(1,0),(0,-1),(-1,0)) 
MOVEMENTS = ["v",">","^","<"]

robot = None
boxes = []
walls = []
instructions = []
with open(sys.argv[1]) as file:
	reading_instructions = False
	for y, line in enumerate(file.readlines()):
		if line.strip() == "":
			reading_instructions = True
			continue

		for x, char in enumerate(line.strip()):
			if reading_instructions:
				instructions.append(MOVEMENTS.index(char))
			else:
				if char=="@":
					robot = (x,y)
				elif char=="O":
					boxes.append((x,y))
				elif char=="#":
					walls.append((x,y))

def get_move(position, move):
	return (position[0]+move[0],position[1]+move[1])

for instruction in instructions:
	move = DIRECTIONS[instruction]
	boxes_to_move = []
	next_pos = get_move(robot,move)
	while next_pos in boxes:
		boxes_to_move.append(next_pos)
		next_pos = get_move(next_pos,move)

	if next_pos in walls:
		continue # move is blocked, does not occur
	else:
		# move robot and any boxes
		robot = get_move(robot,move)
		new_box_positions = [get_move(x,move) for x in boxes_to_move]
		boxes = [x for x in boxes if x not in boxes_to_move]
		boxes.extend(new_box_positions)

sum_of_gps_coordinates = 0
for box in boxes:
	sum_of_gps_coordinates+=(box[0]+(box[1]*100))

print("After {} instructions the sum of GPS coordinates from {} boxes is {}".format(len(instructions), len(boxes), sum_of_gps_coordinates))
