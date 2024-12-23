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

def add_to_group(list_of_computers_in_group, groups, computers, evaluated):
    group_hash = ",".join(sorted(list_of_computers_in_group))
    if group_hash in evaluated:
        return
    evaluated.add(group_hash)
    additions_to_group = computers[list_of_computers_in_group[0]]
    for i in range(1,len(list_of_computers_in_group)):
        additions_to_group = additions_to_group.intersection(computers[list_of_computers_in_group[i]])

    if len(additions_to_group) > 0:
        for addition in additions_to_group:
            add_to_group(list_of_computers_in_group+[addition], groups, computers, evaluated)
    elif len(list_of_computers_in_group) > 3: # only bother with ones of size 4 and up, since we know we have lots of groups of 3
        groups.add(group_hash)

groups = set()
evaluated = set()
for computer in computers.keys():
    add_to_group([computer], groups, computers, evaluated)

longest_group = ""
for group in groups:
    if len(group) > len(longest_group):
        longest_group = group

print("Of the {} groups of 4 or more computers, the longest is {}".format(len(groups), longest_group))
