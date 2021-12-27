from utils.timer import timer_decorator
from copy import deepcopy

@timer_decorator
def MoveCucumbers(data):

    steps = 0
    cucumberHasMoved = True
    
    while cucumberHasMoved:
        cucumberHasMoved = False

        # move east-facing cucumbers
        new_data = deepcopy(data)

        for y, line in enumerate(data):
            for x, _ in enumerate(line):
                
                if data[y][x] == '>':
                    if x + 1 < len(line):
                        if data[y][x + 1] == '.':
                            new_data[y][x] = '.'
                            new_data[y][x + 1] = '>'
                            cucumberHasMoved = True
                    else:
                        if data[y][0] == '.':
                            new_data[y][x] = '.'
                            new_data[y][0] = '>'
                            cucumberHasMoved = True

        data = deepcopy(new_data)
        new_data = deepcopy(data)

        # move south-facing cucumbers
        for y, line in enumerate(data):
            for x, _ in enumerate(line):

                if data[y][x] == 'v':
                    if y + 1 < len(data):
                        if data[y + 1][x] == '.':
                            new_data[y][x] = '.'
                            new_data[y + 1][x] = 'v'
                            cucumberHasMoved = True
                    else:
                        if data[0][x] == '.':
                            new_data[y][x] = '.'
                            new_data[0][x] = 'v'
                            cucumberHasMoved = True

        steps += 1
        data = deepcopy(new_data)

    return steps

if __name__ == "__main__":

    with open("input/day_25.txt") as file:
        data = [[char for char in line.rstrip()] for line in list(file)]

        print("Part 1: ", MoveCucumbers(data))
