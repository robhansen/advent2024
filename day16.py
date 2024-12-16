#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

DIRECTIONS = ((0,1),(1,0),(0,-1),(-1,0))

class Node:
    def __init__(self,pos):
        self.pos = pos
        self.edges = []

    def add_edge(self,pos):
        self.edges.append(pos)

nodes = {}
start = None
end = None

with open(sys.argv[1]) as file:
    for y, line in enumerate(file.readlines()):
        for x, char in enumerate(line.strip()):
            if char=='.' or char=='S' or char=='E':
                pos = (x,y)
                nodes[pos] = Node(pos)
                if char=='S':
                    start = (pos)
                if char=='E':
                    end = (pos)

def sum_vectors(vec1,vec2):
    return (vec1[0]+vec2[0],vec1[1]+vec2[1])

for node in nodes.values():
    for move in DIRECTIONS:
        adjacent = sum_vectors(node.pos, move)
        if adjacent in nodes:
            node.add_edge(adjacent)

def get_next_steps(nodes, position, facing, cost_so_far, path_so_far, visited): # return list of tuples of (position, facing, cost_so_far, path_so_far)
    next_steps = []
    for move in DIRECTIONS:
        adjacent = sum_vectors(position, move)
        if adjacent not in nodes[position].edges:
            continue
        incremental_cost = (1 if move==facing else 1001)
        if sum_vectors(facing,move) == (0,0):
            if cost_so_far > 0:
                continue # never a reason to go directly back the way we came after the first move
            else:
                incremental_cost += 1000 # don't forget to account for turning around fully from the starting position
        if (adjacent,move) in visited:
            continue
        next_steps.append((adjacent, move, cost_so_far+incremental_cost, path_so_far+[adjacent]))
    return next_steps

cost_of_shortest_path = None
nodes_on_best_paths = set()
visited = set() # (position, facing) # include facing in this
potential_next_steps = get_next_steps(nodes, start, (1,0), 0, [start], visited)
potential_next_steps.sort(key=lambda x: x[2])
while True:
    next_step = potential_next_steps.pop(0)
    if cost_of_shortest_path is not None and next_step[2] > cost_of_shortest_path:
        break
    if next_step[0] == end:
        cost_of_shortest_path = next_step[2]
        nodes_on_best_paths.update(next_step[3])
        # don't break now so that we can find all equally cheap paths to the end
    visited.add((next_step[0],next_step[1]))
    new_potential_steps = get_next_steps(nodes, next_step[0], next_step[1], next_step[2], next_step[3], visited)
    if len(new_potential_steps) > 0:
        potential_next_steps.extend(new_potential_steps)
        potential_next_steps.sort(key=lambda x: x[2]) # sort by cost, ascending

print("Cost of optimal path is {}. The optimal path(s) pass through {} different nodes".format(cost_of_shortest_path, len(nodes_on_best_paths)))
