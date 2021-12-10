from utils.timer import timer_decorator

@timer_decorator
def Part1(data):

    errors = { ')' : 0, ']' : 0, '}' : 0, '>' : 0 }

    for line in data:
        characters = []
        for char in line:
            if char == '(' or char == '[' or char == '{' or char == '<':
                characters += [char]
            else:
                if characters[-1] == '(':
                    if char == ')':
                        characters.pop()
                    else:
                        errors[char] += 1
                        break
                elif characters[-1] == '[':
                    if char == ']':
                        characters.pop()
                    else:
                        errors[char] += 1
                        break
                elif characters[-1] == '{':
                    if char == '}':
                        characters.pop()
                    else:
                        errors[char] += 1
                        break
                elif characters[-1] == '<':
                    if char == '>':
                        characters.pop()
                    else:
                        errors[char] += 1
                        break

    return errors[')'] * 3 + errors[']'] * 57 + errors['}'] * 1197 + errors['>'] * 25137

@timer_decorator
def Part2(data):

    errors = { ')' : 0, ']' : 0, '}' : 0, '>' : 0 }

    incomplete_data = []
    scores = []

    for line in data:
        line_corrupted = False
        characters = []

        for char in line:
            if char == '(' or char == '[' or char == '{' or char == '<':
                characters += [char]
            else:
                if characters[-1] == '(':
                    if char == ')':
                        characters.pop()
                    else:
                        line_corrupted = True
                        break
                elif characters[-1] == '[':
                    if char == ']':
                        characters.pop()
                    else:
                        line_corrupted = True
                        break
                elif characters[-1] == '{':
                    if char == '}':
                        characters.pop()
                    else:
                        line_corrupted = True
                        break
                elif characters[-1] == '<':
                    if char == '>':
                        characters.pop()
                    else:
                        line_corrupted = True
                        break
        
        if line_corrupted == False:
            incomplete_data.append(characters)

    for line in incomplete_data:
        # print(line)
        score = 0

        for char in reversed(line):
            if char == '(':
                score = score * 5 + 1
            elif char == '[':
                score = score * 5 + 2
            elif char == '{':
                score = score * 5 + 3
            elif char == '<':
                score = score * 5 + 4
            
            # print(score)
        
        scores.append(score)

    # print(scores)
    scores = sorted(scores)
    # print(scores)

    middleIndex = int((len(scores) - 1) / 2)

    return scores[middleIndex]

if __name__ == "__main__":
    with open("input/day_10.txt") as file:    
        data = [[x for x in line.rstrip()] for line in file]

        print("Part 1:", Part1(data))
        print("Part 2:", Part2(data))
    