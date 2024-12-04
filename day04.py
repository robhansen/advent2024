#!/usr/bin/env python3

import sys

def get_char(wordsearch,i,j):
	if i < 0 or i >= len(wordsearch):
		return ""
	if j < 0 or j >= len(wordsearch[i]):
		return ""
	return wordsearch[i][j]

def match_slash(wordsearch,i,j,match_pattern):
	for matches in match_pattern:
		matched = True
		for match in matches:
			if match[0]!=get_char(wordsearch,i+match[1],j+match[2]):
				matched = False
		if matched:
			return True
	return False

def count_mas(wordsearch,i,j):
	match_patterns_slash = [
	(("M",-1,-1),("S",1,1)),
	(("S",-1,-1),("M",1,1)),
	]
	match_patterns_backslash = [
	(("M",-1,1),("S",1,-1)),
	(("S",-1,1),("M",1,-1)),
	]

	return 1 if (match_slash(wordsearch,i,j,match_patterns_slash) and match_slash(wordsearch,i,j,match_patterns_backslash)) else 0

def count_xmas(wordsearch,i,j):
	searches = [
		[(0,1),(0,2),(0,3)],
		[(1,1),(2,2),(3,3)],
		[(-1,1),(-2,2),(-3,3)],
		[(1,0),(2,0),(3,0)],
		[(-1,0),(-2,0),(-3,0)],
		[(0,-1),(0,-2),(0,-3)],
		[(1,-1),(2,-2),(3,-3)],
		[(-1,-1),(-2,-2),(-3,-3)]
	]
	match_pattern = "MAS"
	xmas_count = len(searches)

	for search in searches:
		for k,match in enumerate(match_pattern):
			if match!=get_char(wordsearch,i+search[k][0],j+search[k][1]):
				xmas_count-=1
				break
	return xmas_count


with open(sys.argv[1]) as file:
    wordsearch = [x.strip() for x in file.readlines()]

xmas_total = 0
mas_total = 0
for i, row in enumerate(wordsearch):
	for j, char in enumerate(row):
		if char=="X":
			xmas_total+=count_xmas(wordsearch,i,j)
		if char=="A":
			mas_total+=count_mas(wordsearch,i,j)

print("Found {} instances of XMAS".format(xmas_total))
print("Found {} instances of X-MAS".format(mas_total))
