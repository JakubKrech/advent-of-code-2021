import copy

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

def CalculateExpectedBitValues(data, parameter):
    ammount_of_true_bits = [0] * len(data[0])
    expected_bit_value = [-1] * len(data[0])
    total_ammount_of_bits = len(data)

    for line in data:
        for bit_index, bit in enumerate(line):
            if bit == '1':
                ammount_of_true_bits[bit_index] += 1

    for bit_index, true_bits in enumerate(ammount_of_true_bits):
        if parameter == "oxygen":
            expected_bit_value[bit_index] = '1' if true_bits >= total_ammount_of_bits / 2 else '0'
        elif parameter == "CO2":
            expected_bit_value[bit_index] = '1' if true_bits < total_ammount_of_bits / 2 else '0'

    return expected_bit_value

def CalculateDiagnosticRating(full_data, rating_identifier):
    value_one_bits = [0] * len(full_data[0])
    data = copy.deepcopy(full_data)
    newData = []
    
    for bit_index, _ in enumerate(value_one_bits):
        expected_bit_values = CalculateExpectedBitValues(data, rating_identifier)

        for line_index, line in enumerate(data):    
            if expected_bit_values[bit_index] == line[bit_index]:
                newData.insert(0, data[line_index])
        
        data = copy.deepcopy(newData)
        newData.clear()

        if len(data) == 1:
            break

    return BinaryToDecimal(data[0])

def Part2(data):
    oxygen = CalculateDiagnosticRating(data, "oxygen")
    CO2 = CalculateDiagnosticRating(data, "CO2")
    
    return  oxygen * CO2

if __name__ == "__main__":

    with open("input/day_03.txt") as file:
        data = [line.strip('\n') for line in list(file)]

        print("Part 1: ", Part1(data))
        print("Part 2: ", Part2(data))
