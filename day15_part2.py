#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

DIRECTIONS = ((0,1),(1,0),(0,-1),(-1,0)) 
MOVEMENTS = ["v",">","^","<"]

robot = None
boxes = [[],[]] # left half and right half
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
					robot = (x*2,y)
				elif char=="O":
					boxes[0].append((x*2,y))
					boxes[1].append(((x*2)+1,y))
				elif char=="#":
					walls.append((x*2,y))
					walls.append(((x*2)+1,y))

def get_move(position, move):
	return (position[0]+move[0],position[1]+move[1])

for instruction in instructions:
	move = DIRECTIONS[instruction]
	boxes_to_move = [[],[]]
	next_positions = [get_move(robot,move)]
	while True:
		boxes_moving = [[],[]]
		for next_pos in next_positions:
			if next_pos in boxes[0]:
				boxes_moving[0].append(next_pos)
			if next_pos in boxes[1]:
				boxes_moving[1].append(next_pos)
		if len(boxes_moving[0]) == 0 and len(boxes_moving[1]) == 0:
			break

		next_positions = []

		if move[0] == 0: # move is vertical, need to ensure both halves of each box are moving if not already
			for box in boxes_moving[0]:
				pair = (box[0]+1,box[1])
				if pair not in boxes_moving[1]:
					boxes_moving[1].append(pair)
			for box in boxes_moving[1]:
				pair = (box[0]-1,box[1])
				if pair not in boxes_moving[0]:
					boxes_moving[0].append(pair)

		for box in boxes_moving[0]:
			boxes_to_move[0].append(box)
			next_positions.append(get_move(box,move))
		for box in boxes_moving[1]:
			boxes_to_move[1].append(box)
			next_positions.append(get_move(box,move))

	impact_with_wall = False
	for next_pos in [get_move(robot,move)]+[get_move(x,move) for x in boxes_to_move[0]]+[get_move(x,move) for x in boxes_to_move[1]]:
		if next_pos in walls:
			impact_with_wall = True
			break

	if impact_with_wall:
		continue # move is blocked, does not occur
	else:
		# move robot and any boxes
		robot = get_move(robot,move)
		new_box_positions = [[get_move(x,move) for x in boxes_to_move[0]],[get_move(x,move) for x in boxes_to_move[1]]]
		boxes = [[x for x in boxes[0] if x not in boxes_to_move[0]], [x for x in boxes[1] if x not in boxes_to_move[1]]]
		boxes[0].extend(new_box_positions[0])
		boxes[1].extend(new_box_positions[1])

sum_of_gps_coordinates = 0
for box in boxes[0]:
	sum_of_gps_coordinates+=(box[0]+(box[1]*100))

print("After {} instructions the sum of GPS coordinates from {} boxes is {}".format(len(instructions), len(boxes[0]), sum_of_gps_coordinates))
