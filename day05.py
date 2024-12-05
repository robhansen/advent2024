#!/usr/bin/env python3

import sys
import math
from collections import defaultdict

def is_valid(update):
    already_seen = set()
    for value in update:
        if bool(ordering[value].intersection(already_seen)): # not empty
            return False
        already_seen.add(value)
    return True
        

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

ordering = defaultdict(lambda: set())
reading_ordering_rules = True
updates = []
with open(sys.argv[1]) as file:
    for line in file:
        if line.strip()=="":
            reading_ordering_rules = False
        elif reading_ordering_rules:
            values = [x for x in line.strip().split("|")]
            ordering[values[0]].add(values[1])
        else:
            updates.append(line.strip().split(","))

sum_of_middles = 0
for update in updates:
    if is_valid(update):
        sum_of_middles += int(update[math.floor(len(update)/2)])
print("Sum of middles is {}".format(sum_of_middles))

sum_of_updated_middles = 0
for update in updates:
    if not is_valid(update):
        while not is_valid(update):
            # swap elements that are out of order until it is valid
            already_seen = set()
            for i in range(len(update)):
                out_of_order = ordering[update[i]].intersection(already_seen)
                if bool(out_of_order): # not empty
                    val_to_swap = out_of_order.pop()
                    index_to_swap = update.index(val_to_swap)
                    update[index_to_swap] = update[i]
                    update[i] = val_to_swap
                    break
                else:
                    already_seen.add(update[i])
        # is now valid
        sum_of_updated_middles += int(update[math.floor(len(update)/2)])
print("Sum of updated middles is {}".format(sum_of_updated_middles))
