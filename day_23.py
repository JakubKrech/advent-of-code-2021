from utils.timer import timer_decorator
from copy import deepcopy
import re

def print_amphipods(d):
    print()
    print("_________________________")
    print(f"| {d[0]} {d[1]} . {d[2]} . {d[3]} . {d[4]} . {d[5]} {d[6]} |")
    print(f"|---- {d[7][0]} | {d[8][0]} | {d[9][0]} | {d[10][0]} ----|")
    print(f"    | {d[7][1]} | {d[8][1]} | {d[9][1]} | {d[10][1]} |  ")
    print(f"    | {d[7][2]} | {d[8][2]} | {d[9][2]} | {d[10][2]} |  ")
    print(f"    | {d[7][3]} | {d[8][3]} | {d[9][3]} | {d[10][3]} |  ")
    print("    -----------------  ")

moveCost = {'A': 1, 'a': 1, 'B': 10, 'b': 10, 'C': 100, 'c': 100, 'D': 1000, 'd': 1000}
energies_required = set()

def MoveToCorridorPosition(d, el, position, move_to_corridor_cost, cost, curr_index, interrupted, current_column_index):

    new_interrupted = deepcopy(interrupted)
    if new_interrupted:
        return new_interrupted

    new_d = deepcopy(d)

    if not new_interrupted and new_d[position] == '.':

        new_d[position] = el.lower()
        new_d[current_column_index][curr_index] = '.'
        new_cost = deepcopy(cost) 
        new_cost += moveCost[el] * (move_to_corridor_cost + curr_index)

        ReccurentAmphipod(new_d, new_cost)
    else:
        new_interrupted = True

    return new_interrupted


def MoveToColumns(d, el, cost, curr_index, target_column_index, current_column_index):
    can_move_to_column = True
    if can_move_to_column:
        if '.' not in d[target_column_index]:
            can_move_to_column = False

        if d[target_column_index] != ['.', '.', '.', '.']:
            for col_elem in d[target_column_index]:
                if col_elem != '.' and el not in [col_elem.lower(), col_elem.upper()]:
                    can_move_to_column = False
                    break

    if can_move_to_column:
        for col_elem_index in [3, 2, 1, 0]:

            can_assign = None
            if col_elem_index == 3:
                can_assign = d[target_column_index][col_elem_index] == '.'
            else:
                can_assign = d[target_column_index][col_elem_index] == '.' and '.' not in d[target_column_index][col_elem_index + 1:]

            # move to last column element
            if can_assign:

                new_d = deepcopy(d)
                new_d[target_column_index][col_elem_index] = el.lower()
                new_d[current_column_index][curr_index] = '.'
                # move up from column (curr_index to account for climbing from lower elements) +
                # distance between columns * 2 + 1 to enter collumn + col_elem_index if needed to go lower into column
                new_cost = deepcopy(cost)
                new_cost += moveCost[el] * (1 + curr_index + abs(current_column_index - target_column_index) * 2 + 1 + col_elem_index) 
                ReccurentAmphipod(new_d, new_cost)


def MoveCorridorElementToColumn(d, el, cost, target_column_index, corridor_index, cost_to_reach_column):
    can_move_to_column = True

    if can_move_to_column:
        if '.' not in d[target_column_index]:
            can_move_to_column = False

        if d[target_column_index] != ['.', '.', '.', '.']:
            for col_elem in d[target_column_index]:
                if col_elem != '.' and el not in [col_elem.lower(), col_elem.upper()]:
                    can_move_to_column = False
                    break

    if can_move_to_column:
        for col_elem_index in [3, 2, 1, 0]:

            can_assign = None
            if col_elem_index == 3:
                can_assign = d[target_column_index][col_elem_index] == '.'
            else:
                can_assign = d[target_column_index][col_elem_index] == '.' and '.' not in d[target_column_index][col_elem_index + 1:]

            # move to last column element
            if can_assign:
                new_d = deepcopy(d)
                new_d[target_column_index][col_elem_index] = el.lower()
                new_d[corridor_index] = '.'
                new_cost = deepcopy(cost)
                new_cost += moveCost[el] * (cost_to_reach_column + 1 + col_elem_index) 
                ReccurentAmphipod(new_d, new_cost)


def ReccurentAmphipod(d, cost):

    if energies_required:
        if cost > min(energies_required):
            return

    # Check if victory condition fullfilled
    if  d[7][0] in ['A', 'a'] and d[7][1] in ['A', 'a'] and d[7][2] in ['A', 'a'] and d[7][3] in ['A', 'a'] and \
        d[8][0] in ['B', 'b'] and d[8][1] in ['B', 'b'] and d[8][2] in ['B', 'b'] and d[8][3] in ['B', 'b'] and \
        d[9][0] in ['C', 'c'] and d[9][1] in ['C', 'c'] and d[9][2] in ['C', 'c'] and d[9][3] in ['C', 'c'] and \
        d[10][0] in ['D', 'd'] and d[10][1] in ['D', 'd'] and d[10][2] in ['D', 'd'] and d[10][3] in ['D', 'd']:
        
        if not energies_required or cost < min(energies_required):
            print("NEW MINIMUM COST FOUND:", cost)

        energies_required.add(cost)
        return

    # Check every element and try to move it to every possible location

    # column A
    current_column_index = 7
    for curr_index, elem in enumerate(d[current_column_index]):

        # break if element is blocked by another element above it
        if curr_index > 0 and d[current_column_index][curr_index - 1] != '.':
            break

        if elem in ['A', 'B', 'C', 'D']:
            # MOVE TO CORRIDOR POSITIONS ON THE LEFT
            interrupted = False
            # # move to left_corridor
            interrupted = MoveToCorridorPosition(d, elem, 1, 2, cost, curr_index, interrupted, current_column_index)   
            # move to leftmost_corridor
            interrupted = MoveToCorridorPosition(d, elem, 0, 3, cost, curr_index, interrupted, current_column_index)
            # MOVE TO CORRIDOR POSITIONS ON THE RIGHT
            interrupted = False
            # move to mid_left
            interrupted = MoveToCorridorPosition(d, elem, 2, 2, cost, curr_index, interrupted, current_column_index)
            # move to mid_mid
            interrupted = MoveToCorridorPosition(d, elem, 3, 4, cost, curr_index, interrupted, current_column_index)
            # move to mid_right
            interrupted = MoveToCorridorPosition(d, elem, 4, 6, cost, curr_index, interrupted, current_column_index)
            # move to right_corridor
            interrupted = MoveToCorridorPosition(d, elem, 5, 8, cost, curr_index, interrupted, current_column_index)
            # move to rightmost_corridor
            interrupted = MoveToCorridorPosition(d, elem, 6, 9, cost, curr_index, interrupted, current_column_index)

            # MOVE TO ANOTHER COLUMNS
            if elem == 'A':
                target_column_index = 7
                can_move_towards_column = False # Same column
            elif elem == 'B':
                target_column_index = 8
                can_move_towards_column = (d[2] == '.')
            elif elem == 'C':
                target_column_index = 9
                can_move_towards_column = (d[2] == '.' and d[3] == '.')
            elif elem == 'D':
                target_column_index = 10
                can_move_towards_column = (d[2] == '.' and d[3] == '.' and d[4] == '.')

            if can_move_towards_column:
                MoveToColumns(d, elem, cost, curr_index, target_column_index, current_column_index)

    # column B
    current_column_index = 8
    for curr_index, elem in enumerate(d[current_column_index]):

        # break if element is blocked by another element above it
        if curr_index > 0 and d[current_column_index][curr_index - 1] != '.':
            break

        if elem in ['A', 'B', 'C', 'D']:

            # MOVE TO CORRIDOR POSITIONS ON THE LEFT
            interrupted = False
            # move to mid_left
            interrupted = MoveToCorridorPosition(d, elem, 2, 2, cost, curr_index, interrupted, current_column_index)
            # # move to left_corridor
            interrupted = MoveToCorridorPosition(d, elem, 1, 4, cost, curr_index, interrupted, current_column_index)   
            # move to leftmost_corridor
            interrupted = MoveToCorridorPosition(d, elem, 0, 5, cost, curr_index, interrupted, current_column_index)

            # MOVE TO CORRIDOR POSITIONS ON THE RIGHT
            interrupted = False
            # move to mid_mid
            interrupted = MoveToCorridorPosition(d, elem, 3, 2, cost, curr_index, interrupted, current_column_index)
            # move to mid_right
            interrupted = MoveToCorridorPosition(d, elem, 4, 4, cost, curr_index, interrupted, current_column_index)
            # move to right_corridor
            interrupted = MoveToCorridorPosition(d, elem, 5, 6, cost, curr_index, interrupted, current_column_index)
            # move to rightmost_corridor
            interrupted = MoveToCorridorPosition(d, elem, 6, 7, cost, curr_index, interrupted, current_column_index)

            # MOVE TO ANOTHER COLUMNS
            if elem == 'A':
                target_column_index = 7
                can_move_towards_column = (d[2] == '.')
            elif elem == 'B':
                target_column_index = 8
                can_move_towards_column = False # Same column
            elif elem == 'C':
                target_column_index = 9
                can_move_towards_column = (d[3] == '.')
            elif elem == 'D':
                target_column_index = 10
                can_move_towards_column = (d[3] == '.' and d[4] == '.')

            if can_move_towards_column:
                MoveToColumns(d, elem, cost, curr_index, target_column_index, current_column_index)

    # column C
    current_column_index = 9
    for curr_index, elem in enumerate(d[current_column_index]):

        # break if element is blocked by another element above it
        if curr_index > 0 and d[current_column_index][curr_index - 1] != '.':
            break

        if elem in ['A', 'B', 'C', 'D']:

            # MOVE TO CORRIDOR POSITIONS ON THE LEFT
            interrupted = False
            # move to mid_mid
            interrupted = MoveToCorridorPosition(d, elem, 3, 2, cost, curr_index, interrupted, current_column_index)
            # move to mid_left
            interrupted = MoveToCorridorPosition(d, elem, 2, 4, cost, curr_index, interrupted, current_column_index)
            # # move to left_corridor
            interrupted = MoveToCorridorPosition(d, elem, 1, 6, cost, curr_index, interrupted, current_column_index)   
            # move to leftmost_corridor
            interrupted = MoveToCorridorPosition(d, elem, 0, 7, cost, curr_index, interrupted, current_column_index)

            # MOVE TO CORRIDOR POSITIONS ON THE RIGHT
            interrupted = False
            # move to mid_right
            interrupted = MoveToCorridorPosition(d, elem, 4, 2, cost, curr_index, interrupted, current_column_index)
            # move to right_corridor
            interrupted = MoveToCorridorPosition(d, elem, 5, 4, cost, curr_index, interrupted, current_column_index)
            # move to rightmost_corridor
            interrupted = MoveToCorridorPosition(d, elem, 6, 5, cost, curr_index, interrupted, current_column_index)

            # MOVE TO ANOTHER COLUMNS
            if elem == 'A':
                target_column_index = 7
                can_move_towards_column = (d[3] == '.' and d[2] == '.')
            elif elem == 'B':
                target_column_index = 8
                can_move_towards_column = (d[3] == '.')
            elif elem == 'C':
                target_column_index = 9
                can_move_towards_column = False # Same column
            elif elem == 'D':
                target_column_index = 10
                can_move_towards_column = (d[4] == '.')

            if can_move_towards_column:
                MoveToColumns(d, elem, cost, curr_index, target_column_index, current_column_index)

    # column D
    current_column_index = 10
    for curr_index, elem in enumerate(d[current_column_index]):

        # break if element is blocked by another element above it
        if curr_index > 0 and d[current_column_index][curr_index - 1] != '.':
            break

        if elem in ['A', 'B', 'C', 'D']:

            # MOVE TO CORRIDOR POSITIONS ON THE LEFT
            interrupted = False
            # move to mid_right
            interrupted = MoveToCorridorPosition(d, elem, 4, 2, cost, curr_index, interrupted, current_column_index)
            # move to mid_mid
            interrupted = MoveToCorridorPosition(d, elem, 3, 4, cost, curr_index, interrupted, current_column_index)
            # move to mid_left
            interrupted = MoveToCorridorPosition(d, elem, 2, 6, cost, curr_index, interrupted, current_column_index)
            # # move to left_corridor
            interrupted = MoveToCorridorPosition(d, elem, 1, 8, cost, curr_index, interrupted, current_column_index)   
            # move to leftmost_corridor
            interrupted = MoveToCorridorPosition(d, elem, 0, 9, cost, curr_index, interrupted, current_column_index)

            # MOVE TO CORRIDOR POSITIONS ON THE RIGHT
            interrupted = False
            
            # move to right_corridor
            interrupted = MoveToCorridorPosition(d, elem, 5, 2, cost, curr_index, interrupted, current_column_index)
            # move to rightmost_corridor
            interrupted = MoveToCorridorPosition(d, elem, 6, 3, cost, curr_index, interrupted, current_column_index)

            # MOVE TO ANOTHER COLUMNS
            if elem == 'A':
                target_column_index = 7
                can_move_towards_column = (d[4] == '.' and d[3] == '.' and d[2] == '.')
            elif elem == 'B':
                target_column_index = 8
                can_move_towards_column = (d[4] == '.' and d[3] == '.')
            elif elem == 'C':
                target_column_index = 9
                can_move_towards_column = (d[4] == '.')
            elif elem == 'D':
                target_column_index = 10
                can_move_towards_column = False # Same column

            if can_move_towards_column:   
                MoveToColumns(d, elem, cost, curr_index, target_column_index, current_column_index)

    # HANDLE MOVEMENT FOR ELEMENTS THAT ARE CURRENTLY IN THE CORRIDOR            
    
    # leftmost element
    corridor_index = 0
    elem = d[corridor_index]
    if elem != '.':

        # try to move elem to appropriate column
        if elem == 'a':
            target_column_index = 7
            can_move_towards_column = (d[1] == '.')
            cost_to_reach_column = 2
        elif elem == 'b':
            target_column_index = 8
            can_move_towards_column = (d[1] == '.' and d[2] == '.')
            cost_to_reach_column = 4
        elif elem == 'c':
            target_column_index = 9
            can_move_towards_column = (d[1] == '.' and d[2] == '.' and d[3] == '.')
            cost_to_reach_column = 6
        elif elem == 'd':
            target_column_index = 10
            can_move_towards_column = (d[1] == '.' and d[2] == '.' and d[3] == '.' and d[4] == '.')
            cost_to_reach_column = 8

        if can_move_towards_column:
            MoveCorridorElementToColumn(d, elem, cost, target_column_index, corridor_index, cost_to_reach_column)
    
    # left element
    corridor_index = 1
    elem = d[corridor_index]
    if elem != '.':

        # try to move elem to appropriate column
        if elem == 'a':
            target_column_index = 7
            can_move_towards_column = True
            cost_to_reach_column = 1
        elif elem == 'b':
            target_column_index = 8
            can_move_towards_column = (d[2] == '.')
            cost_to_reach_column = 3
        elif elem == 'c':
            target_column_index = 9
            can_move_towards_column = (d[2] == '.' and d[3] == '.')
            cost_to_reach_column = 5
        elif elem == 'd':
            target_column_index = 10
            can_move_towards_column = (d[2] == '.' and d[3] == '.' and d[4] == '.')
            cost_to_reach_column = 7

        if can_move_towards_column:
            MoveCorridorElementToColumn(d, elem, cost, target_column_index, corridor_index, cost_to_reach_column)

    # mid-left element
    corridor_index = 2
    elem = d[corridor_index]
    if elem != '.':

        # try to move elem to appropriate column
        if elem == 'a':
            target_column_index = 7
            can_move_towards_column = True
            cost_to_reach_column = 1
        elif elem == 'b':
            target_column_index = 8
            can_move_towards_column = True
            cost_to_reach_column = 1
        elif elem == 'c':
            target_column_index = 9
            can_move_towards_column = (d[3] == '.')
            cost_to_reach_column = 3
        elif elem == 'd':
            target_column_index = 10
            can_move_towards_column = (d[3] == '.' and d[4] == '.')
            cost_to_reach_column = 5

        if can_move_towards_column:
            MoveCorridorElementToColumn(d, elem, cost, target_column_index, corridor_index, cost_to_reach_column)

    # mid-mid element
    corridor_index = 3
    elem = d[corridor_index]
    if elem != '.':

        # try to move elem to appropriate column
        if elem == 'a':
            target_column_index = 7
            can_move_towards_column = (d[2] == '.')
            cost_to_reach_column = 3
        elif elem == 'b':
            target_column_index = 8
            can_move_towards_column = True
            cost_to_reach_column = 1
        elif elem == 'c':
            target_column_index = 9
            can_move_towards_column = True
            cost_to_reach_column = 1
        elif elem == 'd':
            target_column_index = 10
            can_move_towards_column = (d[4] == '.')
            cost_to_reach_column = 3

        if can_move_towards_column:
            MoveCorridorElementToColumn(d, elem, cost, target_column_index, corridor_index, cost_to_reach_column)

    # mid-right element
    corridor_index = 4
    elem = d[corridor_index]
    if elem != '.':

        # try to move elem to appropriate column
        if elem == 'a':
            target_column_index = 7
            can_move_towards_column = (d[3] == '.' and d[2] == '.')
            cost_to_reach_column = 5
        elif elem == 'b':
            target_column_index = 8
            can_move_towards_column = (d[3] == '.')
            cost_to_reach_column = 3
        elif elem == 'c':
            target_column_index = 9
            can_move_towards_column = True
            cost_to_reach_column = 1
        elif elem == 'd':
            target_column_index = 10
            can_move_towards_column = True
            cost_to_reach_column = 1

        if can_move_towards_column:
            MoveCorridorElementToColumn(d, elem, cost, target_column_index, corridor_index, cost_to_reach_column)

    # right element
    corridor_index = 5
    elem = d[corridor_index]
    if elem != '.':

        # try to move elem to appropriate column
        if elem == 'a':
            target_column_index = 7
            can_move_towards_column = (d[4] == '.' and d[3] == '.' and d[2] == '.')
            cost_to_reach_column = 7
        elif elem == 'b':
            target_column_index = 8
            can_move_towards_column = (d[4] == '.' and d[3] == '.')
            cost_to_reach_column = 5
        elif elem == 'c':
            target_column_index = 9
            can_move_towards_column = (d[4] == '.')
            cost_to_reach_column = 3
        elif elem == 'd':
            target_column_index = 10
            can_move_towards_column = True
            cost_to_reach_column = 1

        if can_move_towards_column:
            MoveCorridorElementToColumn(d, elem, cost, target_column_index, corridor_index, cost_to_reach_column)

    # rightmost element
    corridor_index = 6
    elem = d[corridor_index]
    if elem != '.':

        # try to move elem to appropriate column
        if elem == 'a':
            target_column_index = 7
            can_move_towards_column = (d[5] == '.' and d[4] == '.' and d[3] == '.' and d[2] == '.')
            cost_to_reach_column = 8
        elif elem == 'b':
            target_column_index = 8
            can_move_towards_column = (d[5] == '.' and d[4] == '.' and d[3] == '.')
            cost_to_reach_column = 6
        elif elem == 'c':
            target_column_index = 9
            can_move_towards_column = (d[5] == '.' and d[4] == '.')
            cost_to_reach_column = 4
        elif elem == 'd':
            target_column_index = 10
            can_move_towards_column = (d[5] == '.')
            cost_to_reach_column = 2

        if can_move_towards_column:
            MoveCorridorElementToColumn(d, elem, cost, target_column_index, corridor_index, cost_to_reach_column)

    return

@timer_decorator
def CalculateLeastRequiredEnergy(data):

    leftmost_corridor = '.'  # data[0]
    left_corridor = '.'      # data[1]

    mid_left = '.'               # data[2]
    mid_mid = '.'                # data[3]
    mid_right = '.'              # data[4]

    right_corridor = '.'     # data[5]
    rightmost_corridor = '.' # data[6]

    column_A = [data[0][0], data[1][0], data[2][0], data[3][0]]  # data[7]
    column_B = [data[0][1], data[1][1], data[2][1], data[3][1]]  # data[8]
    column_C = [data[0][2], data[1][2], data[2][2], data[3][2]]  # data[9]
    column_D = [data[0][3], data[1][3], data[2][3], data[3][3]]  # data[10]

    full_data = [leftmost_corridor, left_corridor, mid_left, mid_mid, mid_right, right_corridor, rightmost_corridor, \
        column_A, column_B, column_C, column_D]

    ReccurentAmphipod(full_data, 0)

    retVal = 0
    if energies_required:
        retVal = min(energies_required)

    return retVal


if __name__ == "__main__":

    with open("input/day_23.txt") as file:
        data = [line.rstrip() for line in list(file)]

        amphipods = []

        for line in data[2:6]:
            match = re.search("\#([ABCD])\#([ABCD])\#([ABCD])\#([ABCD])", line)
            l = [match.group(1), match.group(2), match.group(3), match.group(4)]
            amphipods.append(l)

        print("Part 2: ", CalculateLeastRequiredEnergy(amphipods))
