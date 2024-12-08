#!/usr/bin/env python3

import sys
from collections import defaultdict

def get_antinodes(node1,node2,width,height,enable_harmonics):
    i= -1 if enable_harmonics else 0
    antinodes = []
    delta = ((node1[0]-node2[0]),(node1[1]-node2[1]))
    while True:
        i+=1
        antinode = (node1[0]+(i*delta[0]),node1[1]+(i*delta[1]))
        if antinode[0] < 0 or antinode[1] < 0 or antinode[0] >= width or antinode[1] >= height:
            return antinodes
        antinodes.append(antinode)
        if not enable_harmonics:
            return antinodes


if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

antenna_locations = defaultdict(lambda: [])

with open(sys.argv[1]) as file:
    lines = file.readlines()
    height = len(lines)
    for y, line in enumerate(lines):
        width = len(line.strip())
        for x, char in enumerate(line.strip()):
            if char!=".":
                antenna_locations[char].append((x,y))

antinode_locations = set()
antinode_locations_with_harmonics = set()
total_lolcations = 0
for antennas in antenna_locations.values():
    for i in range(len(antennas)):
        for j in range(len(antennas)):
            if i==j:
                continue
            # each pair of antennas creates two antinodes
            antinode_locations.update(get_antinodes(antennas[i],antennas[j],width,height,False))
            antinode_locations.update(get_antinodes(antennas[j],antennas[i],width,height,False))
            antinode_locations_with_harmonics.update(get_antinodes(antennas[i],antennas[j],width,height,True))
            antinode_locations_with_harmonics.update(get_antinodes(antennas[j],antennas[i],width,height,True))

print("Found {} antinode locations within the map, {} once harmonics are considered".format(len(antinode_locations),len(antinode_locations_with_harmonics)))
