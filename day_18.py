from utils.timer import timer_decorator
from math import ceil, floor

def IsExplodeRequired(expression):
    nesting_level = 0
    begin_index = -1
    back_index = -1

    for index in range(len(expression)):
        if expression[index] == '[':
            nesting_level += 1
        elif expression[index] == ']':
            nesting_level -= 1
        
        if nesting_level > 4:
            begin_index = index

            while expression[index] != ']':
                index += 1

            back_index = index + 1

            return True, begin_index, back_index

    return False, -1, -1

def IsSplitRequired(expression):
    split_begin_index = -1
    split_back_index = -1

    for index in range(len(expression)):

        if expression[index].isdigit():
            number = expression[index]
            number_begin_index = index
            index += 1

            while expression[index].isdigit():
                number += expression[index]
                index += 1

            if int(number) >= 10: # if number is bigger or equal to 10, it splits

                split_begin_index = number_begin_index
                split_back_index = index

                return True, split_begin_index, split_back_index

    return False, -1, -1

def Explode(expression, begin_index, back_index):

    left = None  # left_closest_number
    right = None # right_closest_number

    # find left closest number
    index = begin_index - 1
    while index >= 0:
        if expression[index].isdigit():
            number = ''
            number_back_index = index + 1

            while expression[index].isdigit():
                number = expression[index] + number
                index -= 1

            number_begin_index = index + 1
            left = (int(number), number_begin_index, number_back_index)
            break
        index -= 1

    # find right closest number
    index = back_index
    while index < len(expression):
        if expression[index].isdigit():
            number = ''
            number_begin_index = index

            while expression[index].isdigit():
                number += expression[index]
                index += 1

            number_back_index = index

            right = (int(number), number_begin_index, number_back_index)
            break
        index += 1
    
    # calculate the values by which the numbers of the neighbours on the left and right will increase
    left_explosion_increment, right_explosion_increment = expression[begin_index + 1:back_index - 1].split(',')
    
    # glue all the pieces together for new expression
    new_expression = ''

    # beggining plus optional left regular number that got increased
    if left:
        new_expression += expression[:left[1]] + str(left[0] + int(left_explosion_increment)) + expression[left[2]:begin_index]
    else:
        new_expression += expression[:begin_index]

    # replace exploded pair with zero
    new_expression += '0'

    # optional right regular number that got increased plus ending
    if right:
        new_expression += expression[back_index:right[1]] + str(right[0] + int(right_explosion_increment)) + expression[right[2]:]
    else:
        new_expression += expression[back_index:]

    return new_expression

def Split(expression, begin_index, back_index):
    number_to_split = int(expression[begin_index:back_index])
    left_number = floor(number_to_split / 2)
    right_number = ceil(number_to_split / 2)

    return expression[:begin_index] + '[' + str(left_number) + ',' + str(right_number) + ']' + expression[back_index:]

def CalculateMagnitude(expression):
    magnitude = 0

    while ',' in expression:
        index_end = expression.find(']') + 1

        for i in reversed(range(0, index_end - 1)):
            if expression[i] == '[':
                index_front = i
                break

        number_1, number_2 = expression[index_front + 1:index_end - 1].split(',')
        magnitude = int(number_1) * 3 + int(number_2) * 2

        expression = expression[:index_front] + str(magnitude) + expression[index_end:]

    return magnitude

def CalculateFinalSum(data):

    num = data[0]
    
    for index in range(1, len(data)):
        num = '[' + num + ',' + data[index] + ']'

        explodeRequired, splitRequired = True, True

        while explodeRequired or splitRequired:
            explodeRequired, begin_expl_index, back_expl_index = IsExplodeRequired(num)
            splitRequired, begin_split_index, back_split_index = IsSplitRequired(num)

            if explodeRequired:
                num = Explode(num, begin_expl_index, back_expl_index)
                continue

            if splitRequired:
                num = Split(num, begin_split_index, back_split_index)
                continue
    
    return num

@timer_decorator
def Part1(data):
    finalSum = CalculateFinalSum(data)
    return CalculateMagnitude(finalSum)

@timer_decorator
def Part2(data):
    maxMagnitude = 0
    length = len(data)
    for x in range(0, length):
        for y in range(0, length):
            if x == y:
                continue

            finalSum = CalculateFinalSum([data[x], data[y]])
            maxMagnitude = max(maxMagnitude, CalculateMagnitude(finalSum))

    return maxMagnitude

if __name__ == "__main__":

    with open("input/day_18.txt") as file:
        data = [line.rstrip() for line in file]

        print("Part 1:", Part1(data))
        print("Part 2:", Part2(data))
