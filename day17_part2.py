#!/usr/bin/env python3

# Program: 2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0

# 2,4, # reg A mod 8 (bottom three bits) to reg B
# 1,5, # XOR B with 0b101 and write to reg A
# 7,5, # reg C = reg A / 2^B
# 1,6, # XOR B with 0b110 and write to reg B
# 0,3, # reg A = reg A / 8
# 4,2, # reg B = reg B ^ reg C (XOR)
# 5,5, # output reg B % 8
# 3,0  # jumps to start unless A is 0

# B = A % 8
# B = B ^ 5
# C = A / (2**B)
# B = B ^ 6
# A = A / 8
# B = B ^ C
# output B % 8

# Each loop, take the bottom 3 bits of A, manipulate it and output that value and then right-shift A 3 bits
# Since A is involved in the manipulation, have to work backwards from the last digit so that A is always known, and build up a valid answer
# As we want the smallest valid answer the first value reached might not be smallest (since the top octect drives what is smallest) so generate all answers and sort

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

        self.saved_reg = [self.reg[0], self.reg[1], self.reg[2]]

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

    def run(self, init_reg_a_to):
        self.reg[0] = init_reg_a_to
        self.reg[1] = self.saved_reg[1]
        self.reg[2] = self.saved_reg[2]
        self.ip = 0
        self.output = []

        while self.ip < len(self.instructions):
            self.step()
        return self.output

    def find_reg_a(self, initial_a):
        answers = []
        for i in range(initial_a, initial_a+8):
            output = self.run(i)
            if self.instructions[-len(output):] == output: # last N instructions match output
                if len(output)==len(self.instructions):
                    answers.append(i)
                else:
                    # calculate prior octet
                    answers.extend(self.find_reg_a(i*8))
        return answers

with open(sys.argv[1]) as file:
    machine = Machine(file)

answers = machine.find_reg_a(0)
answers.sort()
print("Found {} values of Register A that cause the output to match the instructions. The smallest value to do so is {}".format(len(answers), answers[0]))


