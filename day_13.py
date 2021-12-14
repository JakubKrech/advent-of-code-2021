from utils.timer import timer_decorator

@timer_decorator
def FoldThePaper(points, folds, x1, x2, y1, y2):
    paper_sheet = [['.' for x in range(y2)] for y in range(x2)]
    first_fold_dot_count = None

    for point in points:
        paper_sheet[point[0]][point[1]] = '#'

    for fold in folds:
        if 'x' == fold[0]:
            for x in range(fold[1] + 1, x2):
                for y in range(y1, y2):
                    if paper_sheet[x][y] == '#':
                        paper_sheet[x2 - x - 1][y] = '#'
            x2 = fold[1]
        else:
            for x in range(x1, x2):
                for y in range(fold[1] + 1, y2):
                    if paper_sheet[x][y] == '#':
                        paper_sheet[x][y2 - y - 1] = '#'
            y2 = fold[1]

        if first_fold_dot_count == None:    
            first_fold_dot_count = sum([line[:y2].count('#') for line in paper_sheet[:x2]])

    return first_fold_dot_count, paper_sheet, x2, y2

if __name__ == "__main__":
    with open("input/day_13.txt") as file:    
        data = [line.rstrip() for line in file]
        points, folds = [], []
        max_x, max_y = 0, 0

        for line in data:
            if ',' in line:
                x, y = map(int, line.split(','))
                points.append([x, y])
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            elif 'fold' in line:
                axis, line = line.split('=')
                folds.append([axis[-1], int(line)])

        part_1_solution, part_2_solution, x2, y2 = FoldThePaper(points, folds, 0, max_x + 1, 0, max_y + 1)
        
        print("Part 1:", part_1_solution)
        print("Part 2:")
        # Print result of part 2
        for y in range(y2):
            for x in range(x2): 
                print(part_2_solution[x][y], end='')
            print()
    