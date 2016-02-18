import sys
import time
class Sudoku:
    def __init__(self, size, data):
        if size != len(data) ** 0.5:
            print("Length does not check out.")
        self.__size = size
        self.__box_size = int(size ** 0.5)
        self.__answers = [["" for y in range(size)] for x in range(size)]
        self.__possibilities = [[[] for y in range(0, self.__size)] for x in range(0, self.__size)]
        for i in range(self.__size):
            for j in range(self.__size):
                if data[i * self.__size + j] == '0':
                    self.__answers[i][j] = ' '
                else:
                    self.__answers[i][j] = data[i * self.__size + j]
    def __str__(self):
        data_string = ""
        for i in range(self.__size):
            for j in range(self.__size):
                data_string += str(self.__answers[i][j]) + ' '
                if (j + 1) % self.__box_size == 0 and j + 1 != self.__size: # puts spaces horizontally between boxes
                    data_string += '| '
            data_string += '\n'
            if (i + 1) % self.__box_size == 0 and i + 1 != self.__size: # puts spaces vertically between boxes
                data_string += ('--' * (self.__box_size) + '+-') * (self.__box_size - 1) + ('--' * (self.__box_size - 1)) + '-\n'
        return data_string
    def get(self, row, col):
        return self.__answers[row][col]
    def set(self, row, col, num):
        self.__answers[row][col] = num
    def getPossibilities(self, row, col):
        return self.__possibilities[row][col]
    def isFull(self):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__answers[i][j] == ' ':
                    return False
        return True
    def getNeighbors(self, row, col):
        tuple_list = []
        for i in range(self.__size):
            tuple_list.append((row, i))
            tuple_list.append((i, col))
        for x in range(self.__box_size):
            for y in range(self.__box_size):
                tuple_list.append((row // self.__box_size * self.__box_size + x, col // self.__box_size * self.__box_size + y))
        for item in tuple_list: # removes repeats
            while tuple_list.count(item) > 1:
                tuple_list.remove(item)
        tuple_list.remove((row, col))
        return tuple_list
    def isValid(self):
        for i in range(self.__size):
            for j in range(self.__size):
                tuple_list = self.getNeighbors(i, j)
                for item in tuple_list:
                    if self.__answers[item[0]][item[1]] == self.__answers[i][j] and self.__answers[i][j] != ' ':
                        return False
        return True
    def copy(self):
        data = ""
        for i in range(self.__size):
            data += "".join(self.__answers[i])
        return Sudoku(self.__size, data)
    def updatePossibilities(self, efficient = True):
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__answers[i][j] == ' ':
                    t = self.getNeighbors(i, j)
                    poss = [str(x) for x in range(1, self.__size + 1)]
                    for neighbor in t:
                        if self.__answers[neighbor[0]][neighbor[1]] in poss:
                            poss.remove(self.__answers[neighbor[0]][neighbor[1]])
                    self.__possibilities[i][j] = poss
                else:
                    self.__possibilities[i][j] = []
        if efficient:
            self.fillSingles()
    def fillSingles(self):
        changes = 0
        for i in range(self.__size):
            for j in range(self.__size):
                if len(self.__possibilities[i][j]) == 1: # if only one value can go in a spot
                    changes += 1
                    self.__answers[i][j] = self.__possibilities[i][j][0]
        if changes != 0:
            self.updatePossibilities()
    def efficientSolve(self):
        initial_time = time.clock()
        t = self.efficient_recurse()
        final_time = time.clock()
        print("Calculation time:", final_time - initial_time)
        if t == None or not t.isFull():
            print("Configuration is not solvable!\n\tor this messed up which is probably more likely...")
        else:
            return t
    def efficient_recurse(self):
        s = self.copy()
        s.updatePossibilities(efficient = True)
        if s.isFull() and s.isValid:
            return s
        for i in range(s.__size):
            for j in range(s.__size):
                if s.__answers[i][j] == ' ':
                    for k in s.getPossibilities(i, j):
                        s.set(i, j, str(k))
                        if s.isValid():
                            t = s.efficient_recurse()
                            if isinstance(t, Sudoku):
                                return t                    
                    return
                
# Enter sudoku configurations going from left to right, down the page (same way you'd read a book)
# Unsolved cells can be entered as '0' or ' '
# Alternatively, you can decomment to preset sudokus below and test them out
# The program can quickly solve most Easy and Medium puzzles, not guaranteed for Hard level.
    
#zen = Sudoku(9, "904200007010000000000706500000800090020904060040002000001607000000000030300005702") # Level: Medium
#zen = Sudoku(9, "360020089000361000000000000803000602400603007607000108000000000000418000970030014") # Level: Medium
zen = Sudoku(9, "53  7    6  195    98    6 8   6   34  8 3  17   2   6 6    28    419  5    8  79") # Level: Easy
#zen = Sudoku(4, "0040100000204000") # Example 2x2 Sudoku, Level: Easy

print("Initial configuration:")
print(zen)
print(zen.efficientSolve())








