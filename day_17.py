from utils.timer import timer_decorator
import re

@timer_decorator
def AnalyseTrajectories(x_begin, x_end, y_begin, y_end):

    max_y_position_reached = 0
    correct_velocities = set()

    for horizontal_velo in range(1, x_end + 1):
        for vertical_velo in range(-abs(y_end) - 1, abs(y_end) + 1):

            x, y = 0, 0
            max_y_current_test = 0

            curr_horizontal_v = horizontal_velo
            curr_vertical_v = vertical_velo

            while True:
                x += curr_horizontal_v  
                if curr_horizontal_v != 0: curr_horizontal_v -= 1 if curr_horizontal_v > 0 else -1

                y += curr_vertical_v
                curr_vertical_v -= 1

                if y > max_y_current_test:
                    max_y_current_test = y

                if x >= x_begin and x <= x_end and y <= y_begin and y >= y_end:
                    correct_velocities.add((horizontal_velo, vertical_velo))
                    
                    if max_y_position_reached < max_y_current_test:
                        max_y_position_reached = max_y_current_test

                if curr_horizontal_v == 0 and x < x_begin:
                    break

                if x > x_end or y < y_end:
                    break
    
    return max_y_position_reached, len(correct_velocities)

if __name__ == "__main__":
    with open("input/day_17.txt") as file:    
        m = re.search("target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)", file.readline())
        x_begin, x_end, y_begin, y_end = m.group(1), m.group(2), m.group(4), m.group(3)
        
        max_y_position_reached, ammount_of_correct_velocities = AnalyseTrajectories(int(x_begin), int(x_end), int(y_begin), int(y_end))

        print("Part 1:", max_y_position_reached)
        print("Part 2:", ammount_of_correct_velocities)
