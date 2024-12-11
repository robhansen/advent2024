#!/usr/bin/env python3

import sys
from collections import defaultdict

def do_blink(stones):
    new_stones = defaultdict(lambda: 0)
    for engraving, num in stones.items():
        if engraving == 0:
            new_stones[1] += num
            continue
        engraving_string = str(engraving)
        if len(engraving_string) % 2 == 0:
            hw = int(len(engraving_string)/2)
            new_stones[int(engraving_string[:hw])] += num
            new_stones[int(engraving_string[hw:])] += num
        else:
            new_stones[engraving*2024] += num
    return new_stones

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

stones = defaultdict(lambda: 0) # key is the value of the stone, the value is the number of instances
with open(sys.argv[1]) as file:
    for val in [int(x) for x in file.readlines()[0].strip().split()]:
        stones[val] += 1

NUM_BLINKS = 25
for i in range(NUM_BLINKS):
    stones = do_blink(stones)

print("After {} blinks there are {} stones".format(NUM_BLINKS, sum(stones.values())))

NUM_FUTHER_BLINKS = 50
for i in range(NUM_FUTHER_BLINKS):
    stones = do_blink(stones)

print("After {} blinks there are {} stones".format(NUM_BLINKS+NUM_FUTHER_BLINKS, sum(stones.values())))
