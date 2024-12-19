#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

with open(sys.argv[1]) as file:
	lines = file.readlines()
	towels = [x.strip() for x in lines[0].split(",")]
	designs = [x.strip() for x in lines[2:]]

def match_towel(design, prior_towels, evaluated):
	for towel in towels:
		pattern_so_far = prior_towels+towel
		if pattern_so_far in evaluated:
			continue
		evaluated.add(pattern_so_far)
		if pattern_so_far == design:
			return True
		elif design.startswith(pattern_so_far):
			if match_towel(design, pattern_so_far, evaluated):
				return True
	return False

valid = 0
for design in designs:
	evaluated = set()
	print("Work out if {} is valid".format(design))
	if match_towel(design, "", evaluated):
		valid += 1

print("{} of the {} designs can be made with towels".format(valid, len(designs)))
