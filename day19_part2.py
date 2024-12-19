#!/usr/bin/env python3

import sys
from collections import defaultdict

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

with open(sys.argv[1]) as file:
	lines = file.readlines()
	towels = [x.strip() for x in lines[0].split(",")]
	designs = [x.strip() for x in lines[2:]]

def add_new_subpatterns(design, prior_towels, permutations, subpatterns):
	design_permutations = 0
	for towel in towels:
		pattern_so_far = prior_towels+towel
		if design == pattern_so_far:
			design_permutations += permutations
		elif design.startswith(pattern_so_far):
			subpatterns[pattern_so_far] += permutations
	return design_permutations

total_path_count = 0
for design in designs:
	subpatterns = defaultdict(lambda: 0)
	add_new_subpatterns(design, "", 1, subpatterns)
	permutations = 0
	while len(subpatterns.keys()) > 0:
		shortest_subpattern = None
		for key in subpatterns.keys():
			if shortest_subpattern is None or len(key) <  len(shortest_subpattern):
				shortest_subpattern = key
		permutations += add_new_subpatterns(design, shortest_subpattern, subpatterns[shortest_subpattern], subpatterns)
		del subpatterns[shortest_subpattern]

	total_path_count += permutations

print("There are a total of {} ways to make the {} designs".format(total_path_count, len(designs)))
