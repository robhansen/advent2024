#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

def mix(val1, val2):
    return val1 ^ val2

def prune(value):
    return value % 16777216

def get_next_number(value):
    value = prune(mix(value, value*64))
    value = prune(mix(value, (value // 32)))
    value = prune(mix(value, (value*2048)))
    return value

with open(sys.argv[1]) as file:
    buyers = [int(x) for x in file.readlines()]

for i in range(2000):
    buyers = [get_next_number(x) for x in buyers]

print("sum of all buyers' 2000th secret numbers is {}".format(sum(buyers)))
