from utils.timer import timer_decorator

@timer_decorator
def Part1(data):

    risk_level = 0

    y_size = len(data[0])
    x_size = len(data)

    for x, row in enumerate(data):
        for y, element in enumerate(row):
            # check left neighbour
            if x > 0:
                if int(data[x - 1][y]) <= int(element):
                    continue
            # check right neighbour
            if x + 1 < x_size:
                if int(data[x + 1][y]) <= int(element):
                    continue
            # check top neighbour
            if y > 0:
                if int(data[x][y - 1]) <= int(element):
                    continue
            # check bottom neighbour
            if y + 1 < y_size:
                if int(data[x][y + 1]) <= int(element):
                    continue

            risk_level += (int(element) + 1)

    return risk_level

def CheckBasin(data, belongs_to_basin, x, y, x_size, y_size, basinSize):

    belongs_to_basin[x][y] = '1'
    basinSize += 1

    # check left neighbour
    if x > 0:
        if data[x - 1][y] != '9':
            if belongs_to_basin[x - 1][y] != '1':
                basinSize = CheckBasin(data, belongs_to_basin, x - 1, y, x_size, y_size, basinSize)
        else:
            belongs_to_basin[x - 1][y] = '9'

    # check right neighbour
    if x + 1 < x_size:
        if data[x + 1][y] != '9':
            if belongs_to_basin[x + 1][y] != '1':
                basinSize = CheckBasin(data, belongs_to_basin, x + 1, y, x_size, y_size, basinSize)
        else:
            belongs_to_basin[x + 1][y] = '9'

    # check top neighbour
    if y > 0:
        if data[x][y - 1] != '9':
            if belongs_to_basin[x][y - 1] != '1':
                basinSize = CheckBasin(data, belongs_to_basin, x, y - 1, x_size, y_size, basinSize)
        else:
            belongs_to_basin[x][y - 1] = '9'

    # check bottom neighbour
    if y + 1 < y_size:
        if data[x][y + 1] != '9':
            if belongs_to_basin[x][y + 1] != '1':
                basinSize = CheckBasin(data, belongs_to_basin, x, y + 1, x_size, y_size, basinSize)
        else:
            belongs_to_basin[x][y + 1] = '9'

    return basinSize

@timer_decorator
def Part2(data):

    x_size = len(data)
    y_size = len(data[0])

    belongs_to_basin = [['0' for x in range(y_size)] for y in range(x_size)]
    basins_sizes = []

    for x, row in enumerate(data):
        for y, element in enumerate(row):
            if belongs_to_basin[x][y] == '0':

                if element == '1':
                    continue

                if element == '9':
                    belongs_to_basin[x][y] = '9'
                    continue

                basins_sizes.append(CheckBasin(data, belongs_to_basin, x, y, x_size, y_size, 0))

    basins_sizes.sort(reverse=True)

    return basins_sizes[0] * basins_sizes[1] * basins_sizes[2]

if __name__ == "__main__":
    with open("input/day_09.txt") as file:    
        data = [[x for x in line.rstrip()] for line in file]

        print("Part 1:", Part1(data))
        print("Part 2:", Part2(data))
    