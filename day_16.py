from utils.timer import timer_decorator
from functools import reduce

packet_version_sum = 0

def DecodePattern(binary_encoded_transmition, current_bit):
    global packet_version_sum
    # print("> DECODING PACKET! Starting bit:", current_bit, "/", len(binary_encoded_transmition) - 1)
    
    operation_names = ["SUM", "MUL", "MIN", "MAX", "LITERAL VALUE", "GREATER", "LOWER", "EQUAL"] 
    subpackets_return_values = []
    first_bit = current_bit
    
    packet_version = binary_encoded_transmition[current_bit:current_bit + 3]
    current_bit += 3
    packet_type_id = binary_encoded_transmition[current_bit:current_bit + 3]
    current_bit += 3
    
    packet_type_id = int(packet_type_id, 2)
    packet_version_sum += int(packet_version, 2)

    if packet_type_id == 4: # packet with literal value
        full_literal_value_bits = ''

        while True:
            is_last_group = True if binary_encoded_transmition[current_bit] == '0' else False
            current_bit += 1
            bit_group = binary_encoded_transmition[current_bit:current_bit + 4]
            current_bit += 4
            full_literal_value_bits += bit_group

            if is_last_group:
                break

        decoded_transmission_to_return = int(full_literal_value_bits, 2)

    else: # packet with an operator that performs some calculation on one or more subpackets contained within
        length_type_id = binary_encoded_transmition[current_bit:current_bit + 1]
        current_bit += 1
        length_type_id = int(length_type_id, 2)

        if length_type_id == 0: # the next 15 bits represents the total length in bits of the subpackets contained by this packet
            total_length_in_bits_of_subpackets = binary_encoded_transmition[current_bit:current_bit + 15]
            current_bit += 15
            subpackets_ending_bit = current_bit + int(total_length_in_bits_of_subpackets, 2)

            while current_bit < subpackets_ending_bit:
                current_bit, decoded = DecodePattern(binary_encoded_transmition, current_bit)
                subpackets_return_values.append(decoded)

        elif length_type_id == 1: # the next 11 bits represents the number of subpackets immediately contained by this packet
            number_of_subpackets = binary_encoded_transmition[current_bit:current_bit + 11]
            current_bit += 11
            for _ in range(int(number_of_subpackets, 2)):
                current_bit, decoded = DecodePattern(binary_encoded_transmition, current_bit)
                subpackets_return_values.append(decoded)

        if packet_type_id in [5, 6, 7] and len(subpackets_return_values) != 2:
            raise ValueError('ERROR - WRONG LENGTH!')

        if packet_type_id == 0:   # sum
            decoded_transmission_to_return = sum(subpackets_return_values)
        elif packet_type_id == 1: # product
            decoded_transmission_to_return = 0 if len(subpackets_return_values) == 0 else reduce((lambda x, y: x * y), subpackets_return_values)
        elif packet_type_id == 2: # minimum
            decoded_transmission_to_return = min(subpackets_return_values)
        elif packet_type_id == 3: # maximum
            decoded_transmission_to_return = max(subpackets_return_values)
        elif packet_type_id == 5: # greater than
            decoded_transmission_to_return = 1 if subpackets_return_values[0] > subpackets_return_values[1] else 0
        elif packet_type_id == 6: # lower than
            decoded_transmission_to_return = 1 if subpackets_return_values[0] < subpackets_return_values[1] else 0
        elif packet_type_id == 7: # equal to
            decoded_transmission_to_return = 1 if subpackets_return_values[0] == subpackets_return_values[1] else 0

    # print("< PACKET DECODED! Bits:", first_bit, '-', current_bit - 1, "/", len(binary_encoded_transmition) - 1, subpackets_return_values, "RETURNING", operation_names[packet_type_id], ':', decoded_transmission_to_return)

    return current_bit, decoded_transmission_to_return
    

@timer_decorator
def EvaluateTheBITSExpression(hexadecimal_encoded_transmition):
    binary_encoded_transmition = bin(int(hexadecimal_encoded_transmition, 16))[2:].zfill(len(hexadecimal_encoded_transmition) * 4)
    return DecodePattern(binary_encoded_transmition, 0)

if __name__ == "__main__":
    with open("input/day_16.txt") as file:

        _, expression_result = EvaluateTheBITSExpression(list(file)[0])
        
        print("Part 1:", packet_version_sum)
        print("Part 2:", expression_result)
