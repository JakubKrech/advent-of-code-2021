from utils.timer import timer_decorator
import copy

@timer_decorator
def Part1(data):
    gamma = 0
    epsilon = 0

    ammount_of_true_bits = [0] * len(data[0])

    for line in data:
        for bit_index, bit in enumerate(line):
            if bit == '1':
                ammount_of_true_bits[bit_index] += 1

    for bit_index, ones in enumerate(reversed(ammount_of_true_bits)):
        if ones > (len(data) / 2):
            gamma += 2 ** bit_index
        else:
            epsilon += 2 ** bit_index

    return gamma * epsilon 

def BinaryToDecimal(binaryForm):
    if isinstance(binaryForm, str):
        binaryForm = [int(number) for number in list(binaryForm)]

    decimalValue = 0

    for bit_index, bit in enumerate(reversed(binaryForm)):
        decimalValue += bit * (2 ** bit_index)

    return decimalValue

def CalculateExpectedBitValue(data, bit_index, parameter):
    ammount_of_true_bits = 0
    expected_bit_value = -1

    for line in data:
        if line[bit_index] == '1':
            ammount_of_true_bits += 1

    if parameter == "oxygen":
        expected_bit_value = '1' if ammount_of_true_bits >= len(data) / 2 else '0'
    elif parameter == "CO2":
        expected_bit_value = '1' if ammount_of_true_bits < len(data) / 2 else '0'

    return expected_bit_value

def CalculateDiagnosticRating(full_data, rating_identifier):
    data = copy.deepcopy(full_data)
    newData = []
    
    for bit_index in range(len(full_data[0])):
        expected_bit_value = CalculateExpectedBitValue(data, bit_index, rating_identifier)

        for line in data:    
            if expected_bit_value == line[bit_index]:
                newData.append(line)
        
        data[:] = newData
        newData.clear()

        if len(data) == 1:
            break

    return BinaryToDecimal(data[0])

@timer_decorator
def Part2(data):
    oxygen = CalculateDiagnosticRating(data, "oxygen")
    co2 = CalculateDiagnosticRating(data, "CO2")
    
    return  oxygen * co2

if __name__ == "__main__":

    with open("input/day_03.txt") as file:
        data = [line.strip('\n') for line in list(file)]

        print("Part 1: ", Part1(data))
        print("Part 2: ", Part2(data))
