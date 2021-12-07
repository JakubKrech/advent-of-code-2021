from utils.timer import timer_decorator

class FuelChart:
    calculated = False
    cost = {0 : 0}

def PrecalculateFuelChart(max):
    if FuelChart.calculated == True:
        return
    
    for x in range(1, max + 1):
        FuelChart.cost[x] = FuelChart.cost[x - 1] + x

    FuelChart.calculated = True

def CostFunctionPart1(distance):
    return abs(distance)

def CostFunctionPart2(distance):
    if FuelChart.calculated == False:
        PrecalculateFuelChart(max(data))

    return FuelChart.cost[abs(distance)]

def CalculateFuelCost(data, position, costFunction):
    cost_for_position = 0

    for number in data:
        cost_for_position += costFunction(number - position)

    return cost_for_position

@timer_decorator
def FindMinimalFuelCost(data, costFunction):

    avg_position = round(sum(data) / len(data))
    minimum_cost = CalculateFuelCost(data, avg_position, costFunction)
    direction = 1 if CalculateFuelCost(data, avg_position + 1, costFunction) < minimum_cost else -1
    
    position = avg_position + direction

    while True:
        cost_for_position = CalculateFuelCost(data, position, costFunction)

        if cost_for_position >= minimum_cost:
            break
        else:
            minimum_cost = cost_for_position
            position += direction
        
    return minimum_cost

if __name__ == "__main__":
    with open("input/day_07.txt") as file:    
        data = [int(s) for s in list(file)[0].split(',')]
        
        print("Part 1:", FindMinimalFuelCost(data, CostFunctionPart1))
        print("Part 2:", FindMinimalFuelCost(data, CostFunctionPart2))
