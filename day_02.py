from utils.timer import timer_decorator

@timer_decorator
def Part1(data):
    
    horizontal = 0
    depth = 0

    for x in data:
        word, number = x.split()

        if word == "forward":
            horizontal += int(number)
        elif word == "down":
            depth += int(number)
        elif word == "up":
            depth -= int(number)

    return horizontal * depth 

@timer_decorator
def Part2(data):
         
    horizontal = 0
    depth = 0
    aim = 0

    for x in data:
        word, number = x.split()

        if word == "forward":
            horizontal += int(number)
            depth += aim * int(number)
        elif word == "down":
            aim += int(number)
        elif word == "up":
            aim -= int(number)

    return horizontal * depth

if __name__ == "__main__":

    with open("input/day_02.txt") as file:
        data = list(file)

        print("Part 1: ", Part1(data))
        print("Part 2: ", Part2(data))
