#!/usr/bin/env python3

import sys
from collections import defaultdict

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
    def __init__(self, target, initial_position = "A"):
        self.target = target
        self.initial_position = initial_position

    def distance_between_positions(self,p1,p2):
        return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

    def take_step_on_path(self, keypad, path):
        new_paths = []
        if len(path[1])>0:
            current_pos = path[1][-1][1]
        else:
            current_pos = keypad[self.initial_position]
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
        if len(paths)==1 and paths[0][0]=="":
            instruction_sets.append("".join([x[0] for x in paths[0][1]]))
            return instruction_sets

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

    def get_directions(self, num_directional_keypads, directional_keyboard_lookup_table):
        instruction_sets = self.get_directions_for_keypad(numeric_keypad, self.target)
        instruction_sets = self.get_shortest_instructions(instruction_sets)
        fragment_sets = []
        for instructions in instruction_sets:
            fragments = defaultdict(lambda: 0)
            frags = instructions.split("A")[:-1]
            for frag in frags:
                fragments[frag+"A"]+=1
            fragment_sets.append(fragments)

        for i in range(num_directional_keypads):
            new_fragment_sets = []
            for fragments in fragment_sets:
                new_fragments = defaultdict(lambda: 0)
                for fragment in fragments.keys():
                    route = "A"+fragment
                    next_gen_route = ""
                    for j in range(len(route)-1):
                        sequence = route[j]+route[j+1]
                        next_gen_route+=directional_keyboard_lookup_table[sequence]
                    frags = next_gen_route.split("A")[:-1]
                    for frag in frags:
                        new_fragments[frag+"A"]+=fragments[fragment]
                new_fragment_sets.append(new_fragments)
            fragment_sets = new_fragment_sets

        direction_lengths = []
        for fragments in fragment_sets:
            length = 0
            for fragment in fragments.keys():
                length += (len(fragment)*fragments[fragment])
            direction_lengths.append(length)
        return min(direction_lengths)


# for each pair of positions in the directional_keypad, find the set of moves to it that is the most efficient
# continue to generate new generations of moves until one is more efficient than the alternatives
directional_keypad_lookup_table = {"vA": "^>A"} # the two options for "vA" proved equally complex for longer than I wanted to calculate, tried each and found the one that gives the smaller answer
for origin in directional_keypad.keys():
    for target in directional_keypad.keys():
        sequence = origin+target
        if sequence not in directional_keypad_lookup_table:
            code = Code(target, origin)
            base_instruction_sets = code.get_directions_for_keypad(directional_keypad, target)
            if len(base_instruction_sets) > 1:
                code.initial_position = "A"
                compare_instruction_sets = []
                for instructions in base_instruction_sets:
                    compare_instruction_sets.append([instructions])
                continue_evaluating = list(range(len(compare_instruction_sets)))
                while True:
                    for i in range(len(compare_instruction_sets)):
                        if i not in continue_evaluating:
                            continue
                        new_instruction_sets = []
                        for instructions in compare_instruction_sets[i]:
                            new_instruction_sets.extend(code.get_directions_for_keypad(directional_keypad, instructions))
                        compare_instruction_sets[i] = code.get_shortest_instructions(new_instruction_sets)
                    most_efficient_instructions_index = 0
                    for i in range(1, len(compare_instruction_sets)):
                        if i not in continue_evaluating:
                            continue
                        if len(compare_instruction_sets[i][0]) < len(compare_instruction_sets[most_efficient_instructions_index][0]):
                            most_efficient_instructions_index = i
                    for i in range(len(compare_instruction_sets)):
                        if i not in continue_evaluating:
                            continue
                        if len(compare_instruction_sets[i][0]) > len(compare_instruction_sets[most_efficient_instructions_index][0]):
                            continue_evaluating.remove(i)
                    if len(continue_evaluating) == 1:
                        directional_keypad_lookup_table[sequence] = base_instruction_sets[continue_evaluating[0]]
                        break
            else:
                directional_keypad_lookup_table[sequence] = base_instruction_sets[0]

codes = []
with open(sys.argv[1]) as file:
    for line in file:
        codes.append(Code(line.strip()))

sum_of_complexities = 0
for code in codes:
    min_instruction_len = code.get_directions(25,directional_keypad_lookup_table)
    complexity = int(code.target[:3])*min_instruction_len
    sum_of_complexities += complexity
    print("{}: shortest length is {}, complexity is {}".format(code.target, min_instruction_len, complexity))

print("Sum of complexities is {}".format(sum_of_complexities))
