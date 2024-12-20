#!/usr/bin/env python3

import sys
import copy

if len(sys.argv) != 4:
    print("Help: {} <filename> <max_cheat_length> <min_cheat_improvement>".format(sys.argv[0]))
    sys.exit(0)

cheat_length = int(sys.argv[2])
minimum_improvement = int(sys.argv[3])

class Node:
    def __init__(self,pos):
        self.pos = pos
        self.edges = []

    def add_edge(self,pos):
        self.edges.append(pos)

class Maze:
    def __init__(self):
        self.nodes = {}

    def add_node(self,pos,is_start,is_end):
        self.nodes[pos] = Node(pos)
        if is_start:
            self.start = pos
        if is_end:
            self.end = pos

    def init_edges(self):
        directions = ((0,1),(1,0),(0,-1),(-1,0))
        for node in self.nodes.values():            
            for move in directions:
                adjacent = (node.pos[0]+move[0],node.pos[1]+move[1])
                if adjacent in self.nodes:
                    node.add_edge(adjacent)

    def get_next_steps(self, position, path): # return list of tuples of (position, path_len)
        next_steps = []
        for adjacent in self.nodes[position].edges:
            if adjacent in path:
                continue
            next_steps.append((adjacent, path+[adjacent]))
        return next_steps

    def get_path(self):
        steps_to_try = self.get_next_steps(self.start, [self.start])
        while len(steps_to_try) > 0:
            next_step = steps_to_try.pop(0)
            if next_step[0] == self.end:
                return next_step[1]
            steps_to_try.extend(self.get_next_steps(next_step[0], next_step[1]))

maze = Maze()
with open(sys.argv[1]) as file:
    for y, line in enumerate(file.readlines()):
        for x, char in enumerate(line.strip()):
            pos = (x,y)
            if char=='.' or char=='S' or char=='E':
                maze.add_node(pos, char=='S', char=='E')
maze.init_edges()
path = maze.get_path()
print("The shortest path to the end without cheats is {} steps".format(len(path)))

def distance_between_positions(p1,p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

# find shorter paths using cheats
good_cheats = 0
for i in range(len(path)): # cheat start point
    for j in range(i+minimum_improvement,len(path)): # only look at ones that will improve by at least minimum_improvement
        cheat_distance = distance_between_positions(path[i],path[j])
        if cheat_distance <= cheat_length and ((j-i)-cheat_distance) >= minimum_improvement:
            good_cheats+=1

print("There are {} cheats that save at least {} picoseconds".format(good_cheats, minimum_improvement))
