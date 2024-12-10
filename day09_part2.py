#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

class Block:
    def __init__(self, id_val, start_index, length):
        self.id = id_val
        self.start_index = start_index
        self.len = length

    def get_checksum(self):
        checksum = 0
        for i in range(self.len):
            checksum += self.id*(self.start_index+i)
        return checksum

filled_blocks = []
empty_blocks = []
with open(sys.argv[1]) as file:
    values = [int(x) for x in file.readlines()[0].strip()]
    id_counter = 0
    index = 0
    free = False
    for val in values:
        if val > 0:
            if free:
                empty_blocks.append(Block(None,index,val))
            else:
                filled_blocks.append(Block(id_counter,index,val))
                id_counter+=1
        free = not free
        index += val

# iterate through filled blocks in reverse order trying to move each one
for block in filled_blocks[::-1]:
    moved = False
    remove_index = None
    for i, empty in enumerate(empty_blocks):
        if empty.start_index > block.start_index:
            break
        if empty.len >= block.len:
            # can move it here
            block.start_index = empty.start_index
            if empty.len > block.len:
                empty.start_index += block.len
                empty.len -= block.len
            else:
                remove_index = i
            moved = True
            break

    if remove_index is not None:
        del(empty_blocks[remove_index])
    if not moved and block.len ==1: # if we can't find a space for a block of size 1 there's no point in continuing to look
        break

checksum = 0
for block in filled_blocks:
    checksum += block.get_checksum()

print("Checksum value={}".format(checksum))
