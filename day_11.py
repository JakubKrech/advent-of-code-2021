from utils.timer import timer_decorator
from itertools import product

ABOUT_TO_FLASH = -1
ALREADY_FLASHED = 0

def increase_neighbour_energy_lvl(data, x, y):
    if x >= 0 and x < len(data) and y >= 0 and y < len(data[0]):
        if data[x][y] != ALREADY_FLASHED and data[x][y] != ABOUT_TO_FLASH:
            data[x][y] += 1

@timer_decorator
def DumboOctopuses(data, flash_counting_steps):

    data_range = range(len(data))
    step = 1
    total_flashes = 0
    all_octo_flashed_at_once_step = -1

    while step <= flash_counting_steps or all_octo_flashed_at_once_step == -1:

        for x, y in product(data_range, data_range):
            data[x][y] += 1

        at_least_one_octopus_flashed = True

        while at_least_one_octopus_flashed:

            at_least_one_octopus_flashed = False

            for x, y in product(data_range, data_range):
                if data[x][y] > 9:
                    data[x][y] = ABOUT_TO_FLASH

            for x, y in product(data_range, data_range):
                if data[x][y] == ABOUT_TO_FLASH:    
                    
                    data[x][y] = ALREADY_FLASHED

                    increase_neighbour_energy_lvl(data, x - 1, y - 1)
                    increase_neighbour_energy_lvl(data, x - 1, y    )
                    increase_neighbour_energy_lvl(data, x - 1, y + 1)
                    increase_neighbour_energy_lvl(data, x    , y - 1)
                    increase_neighbour_energy_lvl(data, x    , y + 1)
                    increase_neighbour_energy_lvl(data, x + 1, y - 1)
                    increase_neighbour_energy_lvl(data, x + 1, y    )
                    increase_neighbour_energy_lvl(data, x + 1, y + 1)
                    
                    at_least_one_octopus_flashed = True

                    if step <= flash_counting_steps:
                        total_flashes += 1

        all_octopuses_flashed = True
        
        for x, y in product(data_range, data_range):
            if data[x][y] != 0:
                all_octopuses_flashed = False
                break

        if all_octopuses_flashed == True:
            all_octo_flashed_at_once_step = step

        step += 1
    
    return total_flashes, all_octo_flashed_at_once_step

if __name__ == "__main__":
    with open("input/day_11.txt") as file:    
        data = [[int(x) for x in line.rstrip()] for line in file]

        part_1, part_2 = DumboOctopuses(data, 100)

        print("Part 1:", part_1)
        print("Part 2:", part_2)
