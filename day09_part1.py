#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

blocks = []
with open(sys.argv[1]) as file:
    values = [int(x) for x in file.readlines()[0].strip()]
    id_counter = 0
    free = False
    for val in values:
        if val > 0:
            if free:
                blocks.extend([None] * val)
            else:
                blocks.extend([id_counter] * val)
                id_counter+=1
        free = not free

start_index = 0
end_index = len(blocks)-1
while start_index < end_index:
    if blocks[start_index] is None:
        if blocks[end_index] is not None:
            blocks[start_index] = blocks[end_index]
            blocks[end_index] = None
        end_index -= 1
    else:
        start_index += 1

checksum = 0
for i, val in enumerate(blocks):
    if i > end_index:
        break
    checksum += val*i

print("Checksum value={}".format(checksum))
