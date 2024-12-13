#!/usr/bin/env python3

import sys
import re
import numpy as np

PRIZE_POSITION_ADJUSTMENT = 10000000000000

class ClawMachine:
    def __init__(self, value_list):
        self.a = value_list[0]
        self.b = value_list[1]
        self.prize = [value_list[2][0]+PRIZE_POSITION_ADJUSTMENT,value_list[2][1]+PRIZE_POSITION_ADJUSTMENT]
        self.a_cost = 3
        self.b_cost = 1

    def get_cheapest_cost_to_win(self):
        # thanks https://stackoverflow.com/questions/58878594/solving-simultaneous-equations-with-python
        A = [[self.a[0],self.b[0]],[self.a[1],self.b[1]]]
        Y = self.prize
        result = [int(x) for x in np.linalg.inv(A).dot(Y)]

        # Using result as-is doesn't work due to precision issues. There must be a better way than this, but it does work...
        lowest_cost = None
        for i in range(result[0]-10,result[0]+10):
            for j in range(result[1]-10,result[1]+10):
                position = [(i*self.a[0])+(j*self.b[0]),(i*self.a[1])+(j*self.b[1])]
                if position == self.prize:
                    cost = (i*self.a_cost)+(j*self.b_cost)
                    if lowest_cost is None or cost < lowest_cost:
                        lowest_cost = cost
                elif position[0] > self.prize[0] or position[1] > self.prize[1]: # have overshot
                    break
        return lowest_cost

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

machines = []
with open(sys.argv[1]) as file:
    value_list = []
    for line in file:
        if line.strip() == "":
            machines.append(ClawMachine(value_list))
            value_list = []
        else:
            value_list.append([int(x) for x in re.findall(r'\d+', line)]) # each line contains a pair of positive digit strings
    if len(value_list)>0:
        machines.append(ClawMachine(value_list))

costs = []
for machine in machines:
    cost = machine.get_cheapest_cost_to_win()
    if cost is not None:
        costs.append(cost)

print("{} tokens required to win {} prizes".format(sum(costs),len(costs)))
