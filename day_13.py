from utils.timer import timer_decorator

@timer_decorator
def FoldThePaper(points, folds, max_x, max_y):

    paper_sheet = [['.' for x in range(max_y + 1)] for y in range(max_x + 1)]
    first_fold_dot_count = None

    for point in points:
        paper_sheet[point[0]][point[1]] = '#'

    for fold in folds:
        if 'x' in fold[0]:
            new_paper = [['.' for x in range(len(paper_sheet[0]))] for y in range(int(len(paper_sheet) / 2))]
            
            for x in range(len(paper_sheet)):
                new_x = abs(x - fold[1]) - 1
                for y in range(len(paper_sheet[0])):
                    if paper_sheet[x][y] == '#':
                        new_paper[new_x][y] = '#'

            paper_sheet = new_paper[:]
        else:
            new_paper = [['.' for x in range(int(len(paper_sheet[0]) / 2))] for y in range(len(paper_sheet))]
            
            for y in range(len(paper_sheet[0])):
                new_y = abs(y - fold[1]) - 1
                for x in range(len(paper_sheet)):
                    if paper_sheet[x][y] == '#':
                        new_paper[x][new_y] = '#'

            paper_sheet = new_paper[:]

        if first_fold_dot_count == None:    
            first_fold_dot_count = sum([line.count('#') for line in paper_sheet])

    return first_fold_dot_count, paper_sheet

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
                folds.append([axis, int(line)])

        part_1_solution, part_2_solution = FoldThePaper(points, folds, max_x, max_y)
        
        print("Part 1:", part_1_solution)
        print("Part 2:")
        # Print code
        for y in reversed(range(len(part_2_solution[0]))):
            for x in reversed(range(len(part_2_solution))): 
                print(part_2_solution[x][y], end='')
            print()
    