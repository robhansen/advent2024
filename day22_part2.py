#!/usr/bin/env python3

import sys
from collections import defaultdict

NUM_ITERATIONS = 2000

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

prices = []
changes = []
for buyer in buyers:
    prices.append([buyer % 10])
    changes.append([None])

bananas_per_sequence = defaultdict(lambda: 0)
for i in range(NUM_ITERATIONS):
    buyers = [get_next_number(x) for x in buyers]
    for j, buyer in enumerate(buyers):
        price = buyer % 10
        changes[j].append(price - prices[j][-1])
        prices[j].append(price)

for i in range(len(changes)):
    sequences_seen_for_this_buyer = set() # only allow each sequence once
    for j in range(1, NUM_ITERATIONS-2):
        sequence = tuple(changes[i][j:j+4])
        if sequence in sequences_seen_for_this_buyer:
            continue
        bananas_per_sequence[sequence] += prices[i][j+3]
        sequences_seen_for_this_buyer.add(sequence)

max_bananas = 0
best_sequence = None
for sequence, bananas in bananas_per_sequence.items():
    if bananas > max_bananas:
        max_bananas = bananas
        best_sequence = sequence

print("By buying at sequence {} we get {} bananas".format(best_sequence, max_bananas))
