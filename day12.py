#!/usr/bin/env python3

import sys

DIRECTIONS = ((0,1),(1,0),(0,-1),(-1,0))

def fill_region_from(region,position,plant_type,plant_map,width,height):    
    for direction in DIRECTIONS:
        next_pos = (position[0]+direction[0],position[1]+direction[1])
        if next_pos not in region and next_pos[0] >= 0 and next_pos[1] >= 0 and next_pos[0] < width and next_pos[1] < height:
            if plant_map[next_pos[1]][next_pos[0]] == plant_type:
                region.add(next_pos)
                region = fill_region_from(region,next_pos,plant_type,plant_map,width,height)
    return region

def get_perimeter_length(region):
    perimiter_length = 0
    for plot in region:
        for direction in DIRECTIONS:
            adjacent = (plot[0]+direction[0],plot[1]+direction[1])
            perimiter_length += 1 if adjacent not in region else 0
    return perimiter_length

def get_adjacent_fences(side, fences, fence):
    next_fences = []
    next_fences.append(((fence[0][0]+fence[1][0], fence[0][1]+fence[1][1]), fence[1]))
    next_fences.append(((fence[0][0]-fence[1][0], fence[0][1]-fence[1][1]), fence[1])) # adjacent fences in a side can be in two different directions
    for next_fence in next_fences:
        if next_fence not in side and next_fence in fences:
                side.add(next_fence)
                side = get_adjacent_fences(side, fences, next_fence)
    return side

def get_perimeter_sides(region):
    fences = []
    for plot in region:
        for direction in DIRECTIONS:
            adjacent = (plot[0]+direction[0],plot[1]+direction[1])
            if adjacent not in region:                
                fences.append((plot, (direction[1],direction[0]))) # reverse the direction 90 degrees since the fence runs at right angles to the direction of the empty plot

    fences_allocated_to_a_side = set()
    side_count = 0
    for fence in fences:
        if fence not in fences_allocated_to_a_side:
            side = {fence}
            side = get_adjacent_fences(side, fences, fence)
            fences_allocated_to_a_side.update(side)
            side_count += 1

    return side_count

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

plant_map = []
with open(sys.argv[1]) as file:
    lines = file.readlines()
    height = len(lines)
    for line in lines:
        width = len(line.strip())
        row_vals = [x for x in line]
        plant_map.append(row_vals)

regions = []
plants_in_region = set()

for y in range(height):
    for x in range(width):
        pos = (x,y)
        if pos not in plants_in_region:
            region = {pos} # set
            region = fill_region_from(region,pos,plant_map[y][x],plant_map,width,height)
            plants_in_region.update(region)
            regions.append(region)

total_fence_cost = 0
total_side_cost = 0
for region in regions:
    total_fence_cost+=(len(region)*get_perimeter_length(region))
    total_side_cost +=(len(region)*get_perimeter_sides(region))

print("found {} regions, with total fence cost {}, total side cost {}".format(len(regions), total_fence_cost, total_side_cost))
