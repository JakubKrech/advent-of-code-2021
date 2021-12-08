from utils.timer import timer_decorator

@timer_decorator
def Part1(output_values):
    
    unique_segments_length = [2, 4, 3, 7] # corresponding to numbers 1, 4, 7, 8
    counter = 0

    for output in output_values:
        for value in output:
            if len(value) in unique_segments_length:
                counter += 1

    return counter

@timer_decorator
def Part2(signal_patterns, output_values):

    sum_of_outputs = 0

    for index, pattern in enumerate(signal_patterns):
        # There are few digits with unique number of segments in them: 1 (2 segments), 4 (4s), 7 (3s), 8 (7s) 
        # There are also digits that share number of segments with other digits:
        # 2, 3, 5 -> 5 segments
        # 0, 6, 9 -> 6 segments
        # Using that information it is possible to determine letter identifiers of each segment.

        sorted_patterns = sorted(pattern, key=len)
        segments_id = ['', '', '', '', '', '', '']

        # Each segments_id element assigns segment shown below to its id letter, e.g. segmends_id[0] will
        # hold letter that identifies top horizontal segment
        #
        #  0000 
        # 1    2
        # 1    2
        #  3333 
        # 4    5
        # 4    5
        #  6666

        # get top segment (0000) by comparing segments of number 7 and 1
        segments_id[0] += [letter for letter in sorted_patterns[1] if letter not in sorted_patterns[0]][0]

        # get top right segment (2222) (6 segment number which does not contain all of number 1 segments)
        # it will be number 6, and letter he is missing will be top right segment identifier
        if [letter for letter in sorted_patterns[0] if letter not in sorted_patterns[6]] != []:
            segments_id[2] = [letter for letter in sorted_patterns[0] if letter not in sorted_patterns[6]][0]
        elif [letter for letter in sorted_patterns[0] if letter not in sorted_patterns[7]] != []:
            segments_id[2] = [letter for letter in sorted_patterns[0] if letter not in sorted_patterns[7]][0]
        elif [letter for letter in sorted_patterns[0] if letter not in sorted_patterns[8]] != []:
            segments_id[2] = [letter for letter in sorted_patterns[0] if letter not in sorted_patterns[8]][0]

        # this tells us, that second letter of two-segment number (1) is bottom right segment identifier (5555)
        segments_id[5] = [letter for letter in sorted_patterns[0] if letter not in segments_id[2]][0]

        # get top left segment (1111) (5 segment number (2) which contains top right but doesnt bottom right)
        # sum of its segments plus bot right segment will leave one letter, which is top left identifier
        if segments_id[2] in sorted_patterns[3] and segments_id[5] not in sorted_patterns[3]:
            number_two_plus_bot_right = sorted_patterns[3] + segments_id[5]
        elif segments_id[2] in sorted_patterns[4] and segments_id[5] not in sorted_patterns[4]:
            number_two_plus_bot_right = sorted_patterns[4] + segments_id[5]
        elif segments_id[2] in sorted_patterns[5] and segments_id[5] not in sorted_patterns[5]:
            number_two_plus_bot_right = sorted_patterns[5] + segments_id[5]

        segments_id[1] += [letter for letter in sorted_patterns[9] if letter not in number_two_plus_bot_right][0]

        # now we can find middle segment (3333), since all but one segments of number 4 are known
        number_4_with_one_missing = segments_id[1] + segments_id[2] + segments_id[5]
        segments_id[3] += [letter for letter in sorted_patterns[2] if letter not in number_4_with_one_missing][0]

        # get bottom left segment (4444), it will be only 6 segment number containing both middle and top-right segment
        # we can find bottom segment identifier by substracting letters of found number from all available letters
        if segments_id[2] in sorted_patterns[6] and segments_id[3] in sorted_patterns[6]:
            segments_id[4] = [letter for letter in sorted_patterns[9] if letter not in sorted_patterns[6]][0]
        elif segments_id[2] in sorted_patterns[7] and segments_id[3] in sorted_patterns[7]:
            segments_id[4] = [letter for letter in sorted_patterns[9] if letter not in sorted_patterns[7]][0]
        elif segments_id[2] in sorted_patterns[8] and segments_id[3] in sorted_patterns[8]:
            segments_id[4] = [letter for letter in sorted_patterns[9] if letter not in sorted_patterns[8]][0]

        # only one segment left (6666)
        found_letters = ''.join(segments_id)
        segments_id[6] = [letter for letter in sorted_patterns[9] if letter not in found_letters][0]

        # decipher signal pattern for each digit
        unique_signal_patterns = {}

        # 0
        pattern = segments_id[0] + segments_id[1] + segments_id[2] + segments_id[4] + segments_id[5] + segments_id[6]
        unique_signal_patterns[''.join(sorted(pattern))] = '0'
        # 1
        pattern = segments_id[2] + segments_id[5]
        unique_signal_patterns[''.join(sorted(pattern))] = '1'
        # 2
        pattern = segments_id[0] + segments_id[2] + segments_id[3] + segments_id[4] + segments_id[6]
        unique_signal_patterns[''.join(sorted(pattern))] = '2'
        # 3
        pattern = segments_id[0] + segments_id[2] + segments_id[3] + segments_id[5] + segments_id[6]
        unique_signal_patterns[''.join(sorted(pattern))] = '3'
        # 4
        pattern = segments_id[1] + segments_id[2] + segments_id[3] + segments_id[5]
        unique_signal_patterns[''.join(sorted(pattern))] = '4'
        # 5
        pattern = segments_id[0] + segments_id[1] + segments_id[3] + segments_id[5] + segments_id[6]
        unique_signal_patterns[''.join(sorted(pattern))] = '5'
        # 6
        pattern = segments_id[0] + segments_id[1] + segments_id[3] + segments_id[4] + segments_id[5] + segments_id[6]
        unique_signal_patterns[''.join(sorted(pattern))] = '6'
        # 7
        pattern = segments_id[0] + segments_id[2] + segments_id[5]
        unique_signal_patterns[''.join(sorted(pattern))] = '7'
        # 8
        pattern = segments_id[0] + segments_id[1] + segments_id[2] + segments_id[3] + segments_id[4] + segments_id[5] + segments_id[6]
        unique_signal_patterns[''.join(sorted(pattern))] = '8'
        # 9
        pattern = segments_id[0] + segments_id[1] + segments_id[2] + segments_id[3] + segments_id[5] + segments_id[6]
        unique_signal_patterns[''.join(sorted(pattern))] = '9'

        output_number_str = ''

        for output_number in output_values[index]:
            output_number_str += unique_signal_patterns[''.join(sorted(output_number))]

        sum_of_outputs += int(output_number_str)

    return sum_of_outputs

if __name__ == "__main__":
    with open("input/day_08.txt") as file: 
        data = []
        for line in file: 
            data.append([s for s in line.rstrip().split(' ')])
        
        signal_patterns = []
        output_values = []
        
        for x in range(len(data)):
            signal_patterns.append(data[x][:10])
            output_values.append(data[x][11:])

        print("Part 1:", Part1(output_values))
        print("Part 2:", Part2(signal_patterns, output_values))
    