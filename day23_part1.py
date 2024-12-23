#!/usr/bin/env python3

import sys
from collections import defaultdict

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

computers = defaultdict(lambda: set())
with open(sys.argv[1]) as file:
    for line in file:
        comps = line.strip().split("-")
        computers[comps[0]].add(comps[1])
        computers[comps[1]].add(comps[0])

trios = set()
for computer, linked_computers in computers.items():
    for linked_computer in linked_computers:
        third_comps = computers[linked_computer].intersection(linked_computers)
        for third_computer in third_comps:
            trios.add(tuple(sorted([computer, linked_computer, third_computer])))

trios_with_a_t = 0
for trio in trios:
    for computer in trio:
        if computer[0] == "t":
            trios_with_a_t += 1
            break

print("Of the {} sets of three inter-connected computers, {} contain a computer starting with 't'".format(len(trios), trios_with_a_t))
