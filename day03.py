#!/usr/bin/env python3

import sys
import re

def do_mul(mul_string):
    #eg mul(44,46)
    nums = [int(x) for x in mul_string[4:-1].split(",")]
    return nums[0]*nums[1]

def get_total(instructions):
    total = 0
    matches = re.findall(r'mul\(\d+,\d+\)', instructions)
    for match in matches:
        total += do_mul(match)
    return total

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

with open(sys.argv[1]) as file:
    instruction_string = "".join(file.readlines())

print("total is {}".format(get_total(instruction_string)))

dont_splits = instruction_string.split("don't()")
instruction_string_with_start_stop = dont_splits[0]
for disabled in dont_splits[1:]:
    disabled_enabled = disabled.split("do()", 1) # only care about first do()
    if len(disabled_enabled) > 1:
        instruction_string_with_start_stop += disabled_enabled[1]

print("total with dos/don'ts is {}".format(get_total(instruction_string_with_start_stop)))
