from utils.timer import timer_decorator

@timer_decorator
def Part1(data):

    character_pairs = {'(' : ')', '[' : ']','{' : '}', '<' : '>'}
    errors = { ')' : 0, ']' : 0, '}' : 0, '>' : 0 }
    incomplete_data = []

    for line in data:
        line_corrupted = False
        characters = []

        for char in line:
            if char in ['(', '[', '{', '<']:
                characters.append(char)
            else:
                if char == character_pairs[characters[-1]]:
                    characters.pop()
                else:
                    errors[char] += 1
                    line_corrupted = True
                    break
                
        if not line_corrupted:
            incomplete_data.append(characters)

    syntax_error_score = errors[')'] * 3 + errors[']'] * 57 + errors['}'] * 1197 + errors['>'] * 25137

    return incomplete_data, syntax_error_score

@timer_decorator
def Part2(incomplete_data):

    character_scoring = {'(' : 1, '[' : 2,'{' : 3, '<' : 4}
    scores = []

    for line in incomplete_data:
        score = 0

        for char in reversed(line):
            score = score * 5 + character_scoring[char]
        
        scores.append(score)

    middleIndex = int((len(scores) - 1) / 2)

    return sorted(scores)[middleIndex]

if __name__ == "__main__":
    with open("input/day_10.txt") as file:    
        data = [[x for x in line.rstrip()] for line in file]

        incomplete_data, part_1_result = Part1(data)

        print("Part 1:", part_1_result)
        print("Part 2:", Part2(incomplete_data))
    