from utils.timer import timer_decorator
import bisect

class CanBeVisited:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost
    def __lt__(self, other):
        return self.cost < other.cost
    def __str__(self):
        return '{},{} - {}'.format(self.x, self.y, self.cost)

@timer_decorator
def DijkstraPathfinding(risk_data):

    x_size = len(risk_data)
    y_size = len(risk_data[0])

    visited = [[0 for x in range(len(risk_data))] for y in range(len(risk_data[0]))]
    tentative_risk = [[-1 for x in range(len(risk_data))] for y in range(len(risk_data[0]))]
    tentative_risk[0][0] = 0
    can_be_visited = [CanBeVisited(0,0,0)]

    x, y = 0, 0

    while visited[-1][-1] == 0:
        element = can_be_visited.pop(0)
        x, y = element.x, element.y
        visited[x][y] = 1

        curr_tentative = tentative_risk[x][y]

        # check left neighbour
        if x > 0:
            xx, yy = x - 1, y
            if tentative_risk[xx][yy] == -1 or tentative_risk[xx][yy] > curr_tentative + risk_data[xx][yy]:
                tentative_risk[xx][yy] = curr_tentative + risk_data[xx][yy]
                bisect.insort(can_be_visited, CanBeVisited(xx, yy, tentative_risk[xx][yy]))
        # check right neighbour
        if x + 1 < x_size:
            xx, yy = x + 1, y
            if tentative_risk[xx][yy] == -1 or tentative_risk[xx][yy] > curr_tentative + risk_data[xx][yy]:
                tentative_risk[xx][yy] = curr_tentative + risk_data[xx][yy]
                bisect.insort(can_be_visited, CanBeVisited(xx, yy, tentative_risk[xx][yy]))
        # check top neighbour
        if y > 0:
            xx, yy = x, y - 1
            if tentative_risk[xx][yy] == -1 or tentative_risk[xx][yy] > curr_tentative + risk_data[xx][yy]:
                tentative_risk[xx][yy] = curr_tentative + risk_data[xx][yy]
                bisect.insort(can_be_visited, CanBeVisited(xx, yy, tentative_risk[xx][yy]))
        # check bottom neighbour
        if y + 1 < y_size:
            xx, yy = x, y + 1
            if tentative_risk[xx][yy] == -1 or tentative_risk[xx][yy] > curr_tentative + risk_data[xx][yy]:
                tentative_risk[xx][yy] = curr_tentative + risk_data[xx][yy]
                bisect.insort(can_be_visited, CanBeVisited(xx, yy, tentative_risk[xx][yy]))

    return tentative_risk[-1][-1]

@timer_decorator
def PathForBiggerData(risk_data):
    multiplier = 5
    size_x = len(risk_data)
    size_y = len(risk_data[0])
    bigger_risk_data = [[0 for x in range(size_x * multiplier)] for y in range(size_y * multiplier)]

    for x in range(len(bigger_risk_data)):
        whole_x = int(x / size_x)
        mod_x = x % size_x
        for y in range(len(bigger_risk_data)):
            whole_y = int(y / size_y)
            mod_y = y % size_y
            new_risk_value = risk_data[mod_x][mod_y] + whole_x + whole_y

            bigger_risk_data[x][y] = new_risk_value if new_risk_value <= 9 else new_risk_value % 9

    return DijkstraPathfinding(bigger_risk_data)

if __name__ == "__main__":
    with open("input/day_15.txt") as file:    
        data = [list(map(int, s.rstrip())) for s in list(file)]
        
        print("Part 1:", DijkstraPathfinding(data))
        print("Part 2:", PathForBiggerData(data))
