from utils.timer import timer_decorator

answers = set()
w, x, y, z = 0, 0, 0, 0

@timer_decorator
def FindModelNumbers(data):

    addition_instructions_numbers = 1111111

    while True:
        a_nums = str(addition_instructions_numbers)
        full_number = list(f"{a_nums[0:5]}_{a_nums[5]}__{a_nums[6]}____")
        w, x, y, z = 0, 0, 0, 0
        
        if '0' not in full_number:
            for index, line in enumerate(data):

                x = (z % 26) + line[1]

                if full_number[index] == '_':
                    if x < 1 or x > 9:
                        break
                    else:
                        w = x
                        full_number[index] = str(w)
                else:
                    w = int(full_number[index])

                z = int(z / line[0])

                x = 0 if x == w else 1

                if x == 1:

                    y = 25 * x + 1
                    z *= y
                    y = (w + line[2]) * x
                    z += y

            if z == 0:
                answers.add(int(''.join(full_number)))

        addition_instructions_numbers += 1
        if addition_instructions_numbers > 9999999:
            break

    return max(answers), min(answers)

if __name__ == "__main__":

    with open("input/day_24.txt") as file:
        data = [line.rstrip().split(' ') for line in list(file)]

        required_data = []

        counter = 0
        while counter < 14:
            line_data = []
            line_data.append(int(data[18 * counter + 4][2]))
            line_data.append(int(data[18 * counter + 5][2]))
            line_data.append(int(data[18 * counter + 15][2]))

            required_data.append(line_data)
            counter += 1

        maxModelNumber, minModelNumber = FindModelNumbers(required_data)

        print("Part 1:", maxModelNumber)
        print("Part 2:", minModelNumber)


# w_x_y_z = [0, 0, 0, 0]
# variables = {'w' : 0, 'x': 1, 'y': 2, 'z': 3}

# def inp(variable, input_value):
#     w_x_y_z[variables[variable]] = input_value

# def add(variable, b):

#     if b in ['w', 'x', 'y', 'z']:
#         w_x_y_z[variables[variable]] += w_x_y_z[variables[b]]
#     else:
#         w_x_y_z[variables[variable]] += b

# def mul(variable, b):
    
#     if b in ['w', 'x', 'y', 'z']:
#         w_x_y_z[variables[variable]] *= w_x_y_z[variables[b]]
#     else:
#         w_x_y_z[variables[variable]] *= b

# def div(variable, b):
    
#     if b in ['w', 'x', 'y', 'z']:
#         divisor = w_x_y_z[variables[b]]
#         if divisor != 0:
#             division_result = w_x_y_z[variables[variable]] / divisor
#             if division_result >= 0:
#                 w_x_y_z[variables[variable]] = floor(division_result)
#             else:
#                 w_x_y_z[variables[variable]] = ceil(division_result)
#     else:
#         divisor = b
#         if divisor != 0:
#             division_result = w_x_y_z[variables[variable]] / b
#             if division_result >= 0:
#                 w_x_y_z[variables[variable]] = floor(division_result)
#             else:
#                 w_x_y_z[variables[variable]] = ceil(division_result)

# def mod(variable, b):

#     if b in ['w', 'x', 'y', 'z']:
#         if w_x_y_z[variables[variable]] >= 0 and w_x_y_z[variables[b]] > 0:
#             w_x_y_z[variables[variable]] = w_x_y_z[variables[variable]] % w_x_y_z[variables[b]]
#     else:
#         if w_x_y_z[variables[variable]] >= 0 and b > 0:
#             w_x_y_z[variables[variable]] = w_x_y_z[variables[variable]] % b

# def eql(variable, b):

#     if b in ['w', 'x', 'y', 'z']:
#         w_x_y_z[variables[variable]] = 1 if w_x_y_z[variables[variable]] == w_x_y_z[variables[b]] else 0
#     else:
#         w_x_y_z[variables[variable]] = 1 if w_x_y_z[variables[variable]] == b else 0