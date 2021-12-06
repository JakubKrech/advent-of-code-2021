from utils.timer import timer_decorator

@timer_decorator
def SimulateLanternfish(data, days):

    timers = [0] * 9
    newlyCreatedFishes = 0

    for timer in data:
        timers[timer] += 1

    for _ in range(days): 
        newlyCreatedFishes = timers[0]
        for index in range(0, 8): # change timers for lanternfishes in the middle of the cycle
            timers[index] = timers[index + 1]
        
        timers[8] = newlyCreatedFishes       # new lanternfishes are created
        timers[6] += newlyCreatedFishes      # latnerfishes that gave birth have their timers reset to 6 

    return sum(timers)

if __name__ == "__main__":
    with open("input/day_06.txt") as file:    
        data = [int(s) for s in list(file)[0].split(',')]
        
        print("Part 1:", SimulateLanternfish(data, 80))
        print("Part 2:", SimulateLanternfish(data, 256))
    