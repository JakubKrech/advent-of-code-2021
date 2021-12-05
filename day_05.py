from utils.timer import timer_decorator
import re

class Coordinates:
    def __init__(self, x1, y1, x2, y2):
        self.x_start = x1
        self.y_start = y1
        self.x_end = x2
        self.y_end = y2

    def __str__(self):
        return 'Coordinates: (%d,%d) -> (%d,%d)' % (self.x_start, self.y_start, self.x_end, self.y_end)

class Map:
    def __init__(self, x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.mapArray = [[0 for _ in range(self.y_max + 1)] for _ in range(self.x_max + 1)]

    def PrintMap(self):
        for y in range(self.y_max + 1):
            for x in range(self.x_max + 1):
                print(self.mapArray[x][y], end="")
            print("")
        return ""

    def CalculateMultiplyCovered(self):
        doubleCoveredSpots = 0

        for y in range(self.y_max + 1):
            for x in range(self.x_max + 1):
                if self.mapArray[x][y] >= 2:
                    doubleCoveredSpots += 1

        return doubleCoveredSpots

@timer_decorator
def CalculateOverlappingNodes(data, max_x, max_y, calculateDiagonals = False):
    map = Map(max_x, max_y)

    for coords in data:
        # handle vertical lines
        if coords.x_start == coords.x_end:
            for y in range(min(coords.y_start, coords.y_end), max(coords.y_start, coords.y_end) + 1):
                map.mapArray[coords.x_start][y] += 1
        # handle horizontal lines  
        elif coords.y_start == coords.y_end: 
            for x in range(min(coords.x_start, coords.x_end), max(coords.x_start, coords.x_end) + 1):
                map.mapArray[x][coords.y_start] += 1
        # handle diagonal lines
        else:
            if calculateDiagonals == False:
                continue

            x_current = coords.x_start
            y_current = coords.y_start

            x_direction = 1 if coords.x_start < coords.x_end else -1
            y_direction = 1 if coords.y_start < coords.y_end else -1

            while x_current != coords.x_end:
                map.mapArray[x_current][y_current] += 1
                x_current += x_direction
                y_current += y_direction
            map.mapArray[x_current][y_current] += 1 # increment value of last node
        
    return map.CalculateMultiplyCovered()

if __name__ == "__main__":

    with open("input/day_05.txt") as file:
        coordinatesData = []

        max_x = 0
        max_y = 0

        for line in file:
            coords = re.search("(\d+),(\d+) -> (\d+),(\d+)", line)
            
            x1 = int(coords[1])
            x2 = int(coords[3])
            y1 = int(coords[2])
            y2 = int(coords[4])

            coordinatesData.append(Coordinates(x1, y1, x2, y2))

            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)

        print("Part 1: ", CalculateOverlappingNodes(coordinatesData, max_x, max_y, calculateDiagonals=False))
        print("Part 2: ", CalculateOverlappingNodes(coordinatesData, max_x, max_y, calculateDiagonals=True))
