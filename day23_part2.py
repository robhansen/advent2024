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

def add_to_group(list_of_computers_in_group, computers, evaluated, longest_group):
    group_hash = ",".join(sorted(list_of_computers_in_group))
    if group_hash in evaluated:
        return
    evaluated.add(group_hash)
    additions_to_group = computers[list_of_computers_in_group[0]]
    for i in range(1,len(list_of_computers_in_group)):
        additions_to_group = additions_to_group.intersection(computers[list_of_computers_in_group[i]])

    if len(additions_to_group) > 0:
        for addition in additions_to_group:
            add_to_group(list_of_computers_in_group+[addition], computers, evaluated, longest_group)
    else:
        if len(group_hash) > len(longest_group[0]):
            longest_group[0] = group_hash

longest_group = [""]
evaluated = set()
for computer in computers.keys():
    add_to_group([computer], computers, evaluated, longest_group)

print("The longest group (and hence the password) is {}".format(longest_group[0]))
