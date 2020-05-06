import copy
import time

class Block(object): # each block in a sudoku board
    options = []
    val = 0 # value in this block
    tried = []

    def __init__(self):
        self.options = [True for _ in range(9)]
        self.tried = [False for _ in range(9)]

    def is_duplicate(self, value, lst):
        for val in lst:
            if val == 0:
                pass
            elif val == value:
                return True
        return False

    def get_first_untried(self, row, col, group):
        self.check(row)
        self.check(col)
        self.check(group)
        for i in range(len(self.tried)):
            if not self.tried[i] and self.options[i]:
                value = i + 1
                self.tried[i] = True
                return value
        return -1

    def set_value(self, value):
        self.val = value

    def get_value(self):
        return self.val

    def is_empty(self):
        return self.val == 0

    def is_invalid(self):
        return self.is_empty() and not any(self.options)

    def check(self, lst):
        '''check in current set, whether every value is possible
            lst: current set of blocks'''
        for i in range(len(lst)):
            if not lst[i].is_empty():
                self.options[lst[i].get_value() - 1] = False




class Sudoku(object): 

    board = []

    def __init__(self):
        self.board = [[Block() for i in range(9)] for j in range(9)]

    def print_board(self):
        print('\n')
        print('***board shown below***\n')
        row_count = col_count = 0
        for i in range(9):
            for j in range(9):
                print(self.board[i][j].get_value(), end = ' ')
                col_count += 1
                if col_count == 3:
                    print('', end = '\t')
                    col_count = 0
            print('')
            row_count += 1
            if row_count == 3:
                print('')
                row_count = 0
        print('***board shown above***')

    def create_puzzle(self):
        self.board[0][0].set_value(3)
        # self.board[0][2].set_value(6)        
        # self.board[0][3].set_value(5)        
        # self.board[0][5].set_value(8)        
        # self.board[0][6].set_value(4)        
        # self.board[1][0].set_value(5)        
        # self.board[1][1].set_value(2)        
        # self.board[2][1].set_value(8)        
        # self.board[2][2].set_value(7)        
        # self.board[2][7].set_value(3)        
        # self.board[2][8].set_value(1)               
        # self.board[3][2].set_value(3)        
        # self.board[3][4].set_value(1)        
        # self.board[3][7].set_value(8)        
        # self.board[4][0].set_value(9)        
        # self.board[4][3].set_value(8)        
        # self.board[4][4].set_value(6)        
        # self.board[4][5].set_value(3)        
        # self.board[4][8].set_value(5)        
        # self.board[5][1].set_value(5)        
        # self.board[5][4].set_value(9)        
        # self.board[5][6].set_value(6)        
        # self.board[6][0].set_value(1)        
        # self.board[6][1].set_value(3)        
        # self.board[6][6].set_value(2)        
        # self.board[6][7].set_value(5)        
        # self.board[7][7].set_value(7)        
        # self.board[7][8].set_value(4)        
        # self.board[8][2].set_value(5)        
        # self.board[8][3].set_value(2)        
        # self.board[8][5].set_value(6)        
        # self.board[8][6].set_value(3)
        self.print_board()

    def is_duplicate(self, lst):
        seen = []
        for val in lst:
            if val == 0:
                pass
            elif val not in seen:
                seen.append(val)
            else:
                return True
        return False

    def is_invalid(self):
        for i in range(9): # check row
            row = self.board[i]
            row_vals = [b.get_value() for b in row]
            if self.is_duplicate(row_vals):
                print('dulicate in row: %d' %(i + 1))
                return True
            for block in row:
                if block.is_empty():
                    block.check(row)
                    if block.is_invalid():
                        return True
                 
        for j in range(9): # check col
            col = [self.board[k][j] for k in range(9)]
            col_vals = [b.get_value() for b in col]
            if self.is_duplicate(col_vals):
                print('duplicate in col: %d' %(j + 1))
                return True
            for block in col:
                if block.is_empty():
                    block.check(col)
                    if block.is_invalid():
                        return True

        for row_group in range(3): # check group
            for col_group in range(3):
                group = self.board[row_group * 3][col_group * 3 : (col_group + 1) * 3] \
                            + self.board[row_group * 3 + 1][col_group * 3 : (col_group + 1) * 3] \
                            + self.board[row_group * 3 + 2][col_group * 3 : (col_group + 1) * 3]
                group_vals = [b.get_value() for b in group]
                if self.is_duplicate(group_vals):
                    print('dupicate in group : (%d, %d)' %(row_group + 1, col_group + 1))
                    return True
                for block in group:
                    if block.is_empty():
                        block.check(group)
                        if block.is_invalid():
                            return True
        return False

    def solve(self):
        sol_stack = [] # use list as stack to record attemps
        i = 0
        while i < 9:
            j = 0
            while j < 9:
                curr_block = self.board[i][j]
                if curr_block.is_empty():
                    row = self.board[i]
                    col = [self.board[k][j] for k in range(9)]
                    row_group = i // 3
                    col_group = j // 3
                    group = self.board[row_group * 3][col_group * 3 : (col_group + 1) * 3] \
                            + self.board[row_group * 3 + 1][col_group * 3 : (col_group + 1) * 3] \
                            + self.board[row_group * 3 + 2][col_group * 3 : (col_group + 1) * 3]
                    value = curr_block.get_first_untried(row, col, group)
                    if value == -1 and not sol_stack:
                        return False # No valid solution, shouldn't happen
                    elif value == -1:
                        # last step is wrong, go back
                        curr_block.options = [True for _ in curr_block.options]
                        curr_block.tried = [False for _ in curr_block.tried]
                        last_step = sol_stack.pop()
                        last_i, last_j = last_step[0], last_step[1]
                        last_block = self.board[last_i][last_j]
                        last_block.set_value(0)
                        i, j = last_i, last_j - 1
                        self.print_board()
                        if j == -1:   
                            print('curr_pos: (%d, %d), bactrack to (%d, %d)' %(i, j + 1, i - 1, 0))
                        else:
                            print('curr_pos: (%d, %d), bactrack to (%d, %d)' %(i, j + 1, i, j))
                    else:
                        sol_stack.append([i, j])
                        curr_block.set_value(value)
                        self.print_board()
                        print('curr_pos: (%d, %d), set value to %d' %(i, j, value))
                j += 1
            i += 1
                        

if __name__ == '__main__':
    sudoku = Sudoku()
    sudoku.create_puzzle()
    if not sudoku.is_invalid():
        print('There is an answer for this puzzle')
        print('Start solving the puzzle:')
        sudoku.solve()
        if not sudoku.is_invalid():
            print('\nPuzzle Solved!')
    else:
        print('There is no answer for this puzzle')