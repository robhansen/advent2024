#!/usr/bin/env python3

import sys
import math

if len(sys.argv) != 5:
    print("Help: {} <filename> <width> <height> <max_walls>".format(sys.argv[0]))
    sys.exit(0)

width = int(sys.argv[2])
height = int(sys.argv[3])
wall_count = int(sys.argv[4])

class Node:
    def __init__(self,pos):
        self.pos = pos
        self.edges = []

    def add_edge(self,pos):
        self.edges.append(pos)

class Maze:
    def __init__(self, wall_list, width, height):
        self.walls = set(wall_list)
        self.nodes = {}
        self.width = width
        self.height = height
        # initialise nodes
        for y in range(self.height):
            for x in range(self.width):
                pos = (x,y)
                if pos not in self.walls:
                    self.nodes[pos] = Node(pos)
        # initialise edges
        for node in self.nodes.values():
            directions = ((0,1),(1,0),(0,-1),(-1,0))
            for move in directions:
                adjacent = (node.pos[0]+move[0],node.pos[1]+move[1])
                if adjacent in self.nodes:
                    node.add_edge(adjacent)

    def get_next_steps(self, position, path_len, visited): # return list of tuples of (position, path_len)
        next_steps = []
        for adjacent in self.nodes[position].edges:
            if adjacent in visited:
                continue
            next_steps.append((adjacent, path_len+1))
            visited.add(adjacent)
        return next_steps

    def get_length_of_shortest_solution(self):
        start = (0,0)
        end = (self.width-1,self.height-1)
        visited = set()
        steps_to_try = self.get_next_steps(start, 0, visited)
        while len(steps_to_try) > 0:
            next_step = steps_to_try.pop(0)
            if next_step[0] == end:
                return next_step[1]
            steps_to_try.extend(self.get_next_steps(next_step[0], next_step[1], visited))

walls = []
with open(sys.argv[1]) as file:
    for line in file:
        walls.append(tuple([int(x) for x in line.strip().split(",")]))

maze = Maze(walls[:wall_count],width,height)
print("With {} walls, the shortest path to the end is {} steps".format(wall_count, maze.get_length_of_shortest_solution()))

# binary chop the solution space to find the smallest number of blocks with no path to the exit quickly
max_with_path = wall_count
min_without_path = len(walls)
while True:
    next_trial = (max_with_path+min_without_path)//2
    if next_trial <= max_with_path:
        next_trial = max_with_path+1 # always increment by at least 1
    maze = Maze(walls[:next_trial],width,height)
    if maze.get_length_of_shortest_solution() is None:
        min_without_path = next_trial
    else:
        max_with_path = next_trial

    if min_without_path == max_with_path+1:
        print("After {} blocks have fallen there is no longer a way to the exit; last block to fall is at {},{}".format(min_without_path, walls[min_without_path-1][0],walls[min_without_path-1][1]))
        break
