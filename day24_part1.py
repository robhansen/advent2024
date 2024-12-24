#!/usr/bin/env python3

import sys
import uuid
from collections import defaultdict

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

class Gate:
	def __init__(self, type, output):
		self.id = uuid.uuid4() # could use an incrementing global integer but I like UUIDs
		self.type = type
		self.inputs = []
		self.output = output

	def input(self, value):
		self.inputs.append(value)
		return len(self.inputs)>=2 # returns True if energised

	def value(self):
		assert len(self.inputs)==2
		inputs = sum(self.inputs)
		if self.type=="AND":
			return 1 if inputs==2 else 0
		elif self.type=="OR":
			return 1 if inputs>0 else 0
		elif self.type=="XOR":
			return 1 if inputs==1 else 0

class Wire:
	def __init__(self):
		self.connections = []
		self.value = None
	def add_connection(self, gate):
		self.connections.append(gate)

gates = {}
wires = defaultdict(lambda: Wire())
ready_to_evaluate = [] # wires that have values that haven't yet energised their respective gates

reading_inputs = True
with open(sys.argv[1]) as file:
    for line in file:
    	if line.strip()=="":
    		reading_inputs = False
    	elif reading_inputs:
    		tokens = line.strip().split(": ")
    		wires[tokens[0]].value = int(tokens[1])
    		ready_to_evaluate.append(tokens[0])
    	else:
    		tokens = line.strip().split()
    		gate = Gate(tokens[1], tokens[4])
    		gates[gate.id] = gate
    		wires[tokens[0]].add_connection(gate.id)
    		wires[tokens[2]].add_connection(gate.id)

gates_energised = 0
while gates_energised<len(gates)> 0:
	wire = wires[ready_to_evaluate.pop(0)]
	for gate in wire.connections:
		if gates[gate].input(wire.value):
			gates_energised+=1
			wires[gates[gate].output].value = gates[gate].value()
			ready_to_evaluate.append(gates[gate].output)

output_value = 0
for wire_name, wire_obj in wires.items():
	if wire_name.startswith("z"):
		output_value += wire_obj.value * (2**int(wire_name[1:]))

print("After energising {} gates, the output value is {}".format(gates_energised, output_value))
