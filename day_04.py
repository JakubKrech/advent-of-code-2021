from itertools import product
from utils.timer import timer_decorator

class BingoBoard:
    
    def __init__(self, boardId, boardNumbers):
        self.boardId = boardId
        self.boardNumbers = boardNumbers
        self.boardStatus = [[0 for _ in range(5)] for _ in range(5)]
        self.setOfNumbers = set()
        self.numbersFound = 0

        self.boardWon = False
        self.wonAtNumber = -1

        for x in range(5):
            for y in range(5):
                self.setOfNumbers.add(boardNumbers[x][y])

    def PrintBoardStatus(self):
        print("Printing board statuses for board #", self.boardId)
        for x in self.boardStatus:
            print(x)

    def PrintBoardNumbers(self):
        print("Printing board numbers for board #", self.boardId)
        for x in self.boardNumbers:
            print(x)
        
    def SumUncheckedNumbers(self):
        sum = 0
        for x, y in product(range(5), range(5)):
            if self.boardStatus[x][y] == 0:
                sum += self.boardNumbers[x][y]
        return sum

    def CheckForBingoVictory(self, x, y):
        # Check if bingo found in row of checked number
        bingoFoundInRow = True
        for row in range(5):
            if self.boardStatus[x][row] != 1:
                bingoFoundInRow = False
        
        if bingoFoundInRow == True:
            return True

        # Check if bingo found in column of checked number
        bingoFoundInColumn = True
        for column in range(5):
            if self.boardStatus[column][y] != 1:
                bingoFoundInColumn = False

        if bingoFoundInColumn == True:
            return True
        
        return False

    def MarkNumberAndCheckForVictory(self, number):
        if self.boardWon == True:
            return False

        if number in self.setOfNumbers:
            for x, y in product(range(5), range(5)):
                if self.boardNumbers[x][y] == number:
                    self.boardStatus[x][y] = 1
                    self.numbersFound += 1

                    if self.numbersFound >= 5:
                        if self.CheckForBingoVictory(x, y):
                            self.boardWon = True
                            self.wonAtNumber = number
                            return True
                    break
        
        return False
    
@timer_decorator
def PrepareBingoBoards(data):
    boards = []

    ammount_of_boards = int(len(data) / 5)
    print("Generating", ammount_of_boards, "bingo boards...")

    for board_id in range(ammount_of_boards):
        numbers = []

        for x in range(5):
            numbers.append(list(map(int, data[board_id * 5 + x].split())))

        boards.append(BingoBoard(board_id, numbers))

    return boards

@timer_decorator
def PlaySomeBingo(bingoNumbers, bingoBoards):
         
    firstWonBoardResult = -1
    boardsWon = 0

    for number in bingoNumbers:
        for board in bingoBoards:
            if board.MarkNumberAndCheckForVictory(number):
                boardsWon += 1

                if firstWonBoardResult == -1:
                    firstWonBoardResult = board.wonAtNumber * board.SumUncheckedNumbers()

                if boardsWon == len(bingoBoards):
                    lastWonBoardResult = board.wonAtNumber * board.SumUncheckedNumbers()
                    return firstWonBoardResult, lastWonBoardResult

    return -1, -1

if __name__ == "__main__":

    with open("input/day_04.txt") as file:

        data = [line.strip('\n') for line in list(file)]

        bingoNumbers = list(map(int, data[0].split(',')))
        bingoBoards = PrepareBingoBoards(list(filter(None, data[1:])))

        firstBingoBoard, lastBingoBoard = PlaySomeBingo(bingoNumbers, bingoBoards)

        print("Part 1:", firstBingoBoard)
        print("Part 2:", lastBingoBoard)
