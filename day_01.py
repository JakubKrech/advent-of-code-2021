def part1(data):
    
    bigger = 0

    for x in range(1, len(data)):
        if data[x] - data[x - 1] > 0:
            bigger += 1

    return bigger

def part2(data):
         
    bigger = 0

    for x in range(3, len(data)):
        if data[x] - data[x - 3] > 0:
            bigger += 1

    return bigger

if __name__ == "__main__":

    with open("input/day_01.txt") as file:
        data = [int(s) for s in list(file)]

        print("Part 1: ", part1(data))
        print("Part 2: ", part2(data))
