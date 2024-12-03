#!/usr/bin/env python3

import sys

def is_safe(vals):
    increasing = 0
    decreasing = 0
    for i in range(len(vals)-1):
        diff = vals[i] - vals[i+1]
        if diff > 0:
            increasing = 1
        else:
            decreasing = 1 # not strictly correct, but 0 is unsafe anyway so it doesn't matter

        diff = abs(diff)
        if diff < 1 or diff > 3:
            return False
    return (increasing+decreasing==1)

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

safe_count = 0
safe_with_ignore_count = 0
with open(sys.argv[1]) as file:
    for line in file:
        vals = [int(x) for x in line.split()]
        if is_safe(vals):
            safe_count += 1
            safe_with_ignore_count += 1
        else:
            # try with the Problem Dampener
            safe_with_ignore = False
            for i in range(len(vals)):
                vals_ignored = vals.copy()
                del vals_ignored[i]
                if is_safe(vals_ignored):
                    safe_with_ignore = True
                    break
            if safe_with_ignore:
                safe_with_ignore_count += 1

print("{} reports are safe".format(safe_count))
print("{} reports are safe with Problem Dampener".format(safe_with_ignore_count))
