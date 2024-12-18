#!/usr/bin/env python3

import sys
import math

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

class Machine:
    def __init__(self,file):
        self.reg = [None] * 3
        lines = [x.strip() for x in file]
        for i in range(3):
            self.reg[i] = int(lines[i][12:])
        self.instructions = [int(x) for x in lines[4][9:].split(",")]
        self.ip = 0 # instruction pointer
        self.output = []

    def get_combo_operand_value(self, op):
        if op < 4:
            return op
        return self.reg[op-4]

    def debug(self):
        print("ip={} regA={} regB={} regC={} output={}".format(self.ip, self.reg[0], self.reg[1], self.reg[2], self.output))

    def step(self):
        instruction = self.instructions[self.ip]
        operand = self.instructions[self.ip+1]
        #self.debug()
        if instruction == 0: # adv
            # The numerator is the value in the A register. 
            # The denominator is found by raising 2 to the power of the instruction's combo operand. 
            # (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
            # The result of the division operation is truncated to an integer and then written to the A register.
            self.reg[0] = math.floor(self.reg[0] / (2**self.get_combo_operand_value(operand)))

        elif instruction == 1: # bxl
            # calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.
            self.reg[1] = (self.reg[1] ^ operand)

        elif instruction == 2: # bst
            # calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.
            self.reg[1] = self.get_combo_operand_value(operand) % 8

        elif instruction == 3: # jnz
            # does nothing if the A register is 0. 
            # However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; 
            # if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
            if self.reg[0]!=0:
                self.ip = operand
                return

        elif instruction == 4: # bxc
            # calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
            self.reg[1] = (self.reg[1] ^ self.reg[2])

        elif instruction == 5: # out
            # calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)
            self.output.append(self.get_combo_operand_value(operand) % 8)

        elif instruction == 6: # bdv
            # works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)
            self.reg[1] = math.floor(self.reg[0] / (2**self.get_combo_operand_value(operand)))

        elif instruction == 7: # cdv
            # works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)
            self.reg[2] = math.floor(self.reg[0] / (2**self.get_combo_operand_value(operand)))

        else:
            print("Invalid instruction {}!".format(instruction))

        self.ip += 2

    def run(self):
        self.output = []
        while self.ip < len(self.instructions):
            self.step()
        print(",".join([str(x) for x in self.output]))

with open(sys.argv[1]) as file:
    machine = Machine(file)
machine.run()


