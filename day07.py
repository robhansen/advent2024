#!/usr/bin/env python3

import sys

def value_to_base_n_string(val, n): # stolen from stackoverflow
    if val == 0:
        return '0'
    nums = []
    while val:
        val, r = divmod(val, n)
        nums.append(str(r))
    return ''.join(reversed(nums))

class Equation:
    def __init__(self, answer_string, input_string):
        self.answer = int(answer_string)
        self.inputs = [int(x) for x in input_string.strip().split()]

    def calculate_possible_answers(self, num_operators):
        for i in range(num_operators ** (len(self.inputs)-1)): # possible permutations of operators
            answer = self.inputs[0]
            operator_string = value_to_base_n_string(i, num_operators).rjust(len(self.inputs)-1, '0') # binary/ternary representation, though converting it to a string and back to do it is a bit rubbish...
            for j in range(len(self.inputs)-1):
                operator_type = int(operator_string[j])
                if operator_type==2: # ||
                    answer = (answer * (10 ** len(str(self.inputs[j+1])))) + self.inputs[j+1]
                elif operator_type==1: # *
                    answer = answer * self.inputs[j+1]
                else: # +
                    answer = answer + self.inputs[j+1]
            if answer == self.answer:
                return answer
        return 0


if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

equations = []
with open(sys.argv[1]) as file:
    for line in file:
        tokens = line.split(":")
        equations.append(Equation(tokens[0],tokens[1]))

calibration_result_with_2 = 0
calibration_result_with_3 = 0
for equation in equations:
    print(i)
    calibration_result_with_2 += equation.calculate_possible_answers(2)
    calibration_result_with_3 += equation.calculate_possible_answers(3)

print("Total calibration results with 2 operators is {}, with 3 is {}".format(calibration_result_with_2,calibration_result_with_3))
