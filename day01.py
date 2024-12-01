#!/usr/bin/env python3

import sys
from collections import defaultdict

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

lists = [[],[]]
value_counter = defaultdict(lambda: 0)
with open(sys.argv[1]) as file:
    for line in file:
        vals = [int(x) for x in line.split()]
        lists[0].append(vals[0])
        lists[1].append(vals[1])
        value_counter[vals[1]]+=1            

lists[0].sort()
lists[1].sort()

distance = 0
similarity = 0
for i in range(len(lists[0])):
    distance+=abs(lists[0][i]-lists[1][i])
    similarity+= (lists[0][i] * value_counter[lists[0][i]])

print("Total distance is {}".format(distance))
print("Similarity score is {}".format(similarity))
