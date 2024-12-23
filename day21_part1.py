#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

numeric_keypad = {
    "7": (0,0),
    "8": (1,0),
    "9": (2,0),
    "4": (0,1),
    "5": (1,1),
    "6": (2,1),
    "1": (0,2),
    "2": (1,2),
    "3": (2,2),
    "0": (1,3),
    "A": (2,3)
}
directional_keypad = {
    "^": (1,0),
    "A": (2,0),
    "<": (0,1),
    "v": (1,1),
    ">": (2,1)
}
directions = {
    (0,1): "v",
    (1,0): ">",
    (0,-1):"^",
    (-1,0):"<"
}

class Code:
    def __init__(self, target):
        self.target = target

    def distance_between_positions(self,p1,p2):
        return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

    def take_step_on_path(self, keypad, path):
        new_paths = []
        if len(path[1])>0:
            current_pos = path[1][-1][1]
        else:
            current_pos = keypad["A"]            
        move_towards = keypad[path[0][0]]

        if current_pos == move_towards:
            return [[path[0][1:], path[1]+[("A",current_pos)]]]

        for direction in directions.keys():
            next_pos = (current_pos[0]+direction[0],current_pos[1]+direction[1])
            if next_pos not in keypad.values():
                continue
            if self.distance_between_positions(next_pos,move_towards) < self.distance_between_positions(current_pos,move_towards):
                new_paths.append([path[0], path[1]+[(directions[direction],next_pos)]])
        return new_paths

    def get_directions_for_keypad(self, keypad, target):
        instruction_sets = []
        paths = self.take_step_on_path(keypad, [target, []])
        # each path is a list of [target, [(instruction,position)]]
        while len(paths) > 0:
            new_paths = self.take_step_on_path(keypad, paths.pop(0))
            if len(new_paths)==1 and new_paths[0][0]=="":
                instruction_sets.append("".join([x[0] for x in new_paths[0][1]]))
            else:
                paths.extend(new_paths)

        return instruction_sets

    def get_shortest_instructions(self, instruction_sets):
        min_instruction_len = len(instruction_sets[0])
        for instructions in instruction_sets:
            if len(instructions) < min_instruction_len:
                min_instruction_len = len(instructions)
        return [x for x in instruction_sets if len(x)==min_instruction_len]

    def get_directions(self, num_directional_keypads=2):
        # assume that at each step we only need to evaluate the shortest instruction sets
        instruction_sets = self.get_directions_for_keypad(numeric_keypad, self.target)
        instruction_sets = self.get_shortest_instructions(instruction_sets)
        for i in range(num_directional_keypads):
            new_instruction_sets = []
            for instructions in instruction_sets:
                new_instruction_sets.extend(self.get_directions_for_keypad(directional_keypad, instructions))
            instruction_sets = self.get_shortest_instructions(new_instruction_sets)
        return instruction_sets

codes = []
with open(sys.argv[1]) as file:
    for line in file:
        codes.append(Code(line.strip()))

sum_of_complexities = 0
for code in codes:
    instruction_sets = code.get_directions()
    min_instruction_len = len(instruction_sets[0])
    complexity = int(code.target[:3])*min_instruction_len
    sum_of_complexities += complexity
    print("{}: got {} sets of instructions, shortest length is {}, complexity is {}".format(code.target, len(instruction_sets), min_instruction_len, complexity))

print("Sum of complexities is {}".format(sum_of_complexities))
