#!/usr/bin/env python3

def find_peak(x,y,width,height,height_map):
    peaks = set()
    rating = 0
    directions = ((0,1),(1,0),(0,-1),(-1,0))
    for direction in directions:
        next_pos = (x+direction[0],y+direction[1])
        if next_pos[0] >= 0 and next_pos[1] >= 0 and next_pos[0] < width and next_pos[1] < height:
            if height_map[next_pos[1]][next_pos[0]] == height_map[y][x]+1:
                if height_map[next_pos[1]][next_pos[0]] == 9:
                    peaks.add(next_pos)
                    rating+=1
                else:
                    new_peaks,updated_rating = find_peak(next_pos[0],next_pos[1],width,height,height_map)
                    peaks.update(new_peaks)
                    rating+=updated_rating
    return peaks,rating

import sys
if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

height_map = []
trailheads = []
with open(sys.argv[1]) as file:
    lines = file.readlines()
    height = len(lines)
    for line in lines:
        width = len(line.strip())
        #height_map.append([int(x) for x in line.strip()])
        row_vals = []
        for char in line.strip():
            row_vals.append(-1 if char=="." else int(char))
        height_map.append(row_vals)

score_total = 0
rating_total = 0
for y,row in enumerate(height_map):
    for x,val in enumerate(row):
        if val==0: # trailhead
            reachable_peaks,rating = find_peak(x,y,width,height,height_map)
            score_total += len(reachable_peaks)
            rating_total += rating

print("Total of trailhead scores is {}, total of ratings is {}".format(score_total, rating_total))

