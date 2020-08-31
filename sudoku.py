import sys
import os

SQUARES = [[x + y for x in alpha for y in num] for alpha in ['ABC', 'DEF', 'GHI'] for num in ['123', '456', '789']]

ALPHA = 'ABCDEFGHI'
NUM = '123456789'

ROWS = [[x + y for y in NUM] for x in ALPHA]
COLS = [[x + y for x in ALPHA] for y in NUM]

BOARD = [x + y for x in ALPHA for y in NUM]

filename = 'sudoku.txt'

class Sudoku:
    
    def __init__(self, board):
        self.board = board
        self.possible = dict(zip([x + y for x in ALPHA for y in NUM], [[]] * 81))
        self.flag = True

    def find_row(self, pos):
        ''' Given a position on the board, returns list of the remaining positions in the same row '''
        return [pos[0] + y for y in NUM if y != pos[1]]

    def find_col(self, pos):
        ''' Given a position on the board, returns list of the remaining positions in the same column '''
        return [x + pos[1] for x in ALPHA if x != pos[0]]

    def find_square(self, pos):
        ''' Given a position on the board, returns list of the remaining positions in the same square '''
        for square in SQUARES:
            if pos in square:
                return square

    def possible_move(self, pos):
        ''' Given a position on the board, returns list of possible numbers that can fill that position.
        A number may fill the position if it is not present in any row, column or square which the position is a part of. '''
        related = set(self.find_row(pos) + self.find_col(pos) + self.find_square(pos))
        contents = [self.board[x] for x in related]
        return [x for x in range(1, 10) if x not in contents]

    def naked_singles(self):
        ''' Updates the possible moves for each position and assigns value to position if there is no other valid move possible '''
        for pos in self.possible.keys():
            if self.board[pos] == 0:
                self.possible[pos] = self.possible_move(pos)
                if len(self.possible[pos]) == 1:
                    self.board[pos] = self.possible[pos][0]
                    self.flag = True

    def solve_naked_singles(self):
        ''' Tries to solve for naked singles until there are no more naked singles left for the given state of the board '''
        while self.flag:
            self.flag = False
            self.naked_singles()
        self.flag = True

    def solve_hidden_singles(self):
        ''' Identifies hidden singles in each row, column and square of board '''
        self.hidden_singles(ROWS)
        self.hidden_singles(COLS)
        self.hidden_singles(SQUARES)

    def hidden_singles(self, GROUPS):
        ''' Identifies hidden singles in group (could be rows, columns or squares) and eliminates possibilities based on them '''
        for group in GROUPS:
            possibles = [self.possible[pos] for pos in group]
            for i in range(1, 10):
                pos = [idx for idx, possible in enumerate(possibles) if i in possible]
                if len(pos) == 1:
                    self.board[group[pos[0]]] = i
                    self.possible[group[pos[0]]] = []
        self.solve_naked_singles()

    def solve_naked_pairs(self):
        ''' Identifies naked pairs/triples in rows, columns and squares '''
        self.naked_pairs(ROWS)
        self.naked_pairs(COLS)
        self.naked_pairs(SQUARES)
        self.naked_pairs(ROWS, 3)
        self.naked_pairs(COLS, 3)
        self.naked_pairs(SQUARES, 3)

    def naked_pairs(self, GROUPS, key = 2):
        ''' Identifies naked pairs (or triples or quads) in group (rows, columns or squares) and eliminates possibilities based on them '''
        for group in GROUPS:
            possibles = {pos : self.possible[pos] for pos in group if len(self.possible[pos]) == key}
            hist = []
            for i in possibles.keys():
                if i in hist:
                    continue
                equals = [i]
                for j in possibles.keys():
                    if i == j:
                        continue
                    if set(possibles[i]) == set(possibles[j]):
                        equals += [j]
                if len(equals) != key:
                    continue
                others = [pos for pos in group if pos not in equals and self.board[pos] == 0]
                for possible in possibles[i]:
                    for j in others:
                        if possible in self.possible[j]:
                            self.possible[j].remove(possible)
                hist += equals
        self.solve_hidden_singles()

    def solve_hidden_pairs(self):
        ''' Identifies hidden pairs/triples in rows, columns and squares '''
        self.hidden_pairs(ROWS)
        self.hidden_pairs(COLS)
        self.hidden_pairs(SQUARES)
        self.hidden_pairs(ROWS, 3)
        self.hidden_pairs(COLS, 3)
        self.hidden_pairs(SQUARES, 3)

    def hidden_pairs(self, GROUPS, key = 2):
        ''' Identifies hidden pairs (or triples or quads) in groups (rows, columns or squares) and eliminates possibilities based on them '''
        for group in GROUPS:
            hist = []
            possibles = [[]] + [[pos for pos in group if i in self.possible[pos]] for i in range(1, 10)]
            for i in range(1, 10):
                if i in hist:
                    continue
                if len(possibles[i]) != key:
                    continue
                equals = [i]
                for j in range(1, 10):
                    if i == j:
                        continue
                    if len(possibles[j]) != key:
                        continue
                    if set(possibles[i]) == set(possibles[j]):
                        equals += [j]
                if len(equals) != key:
                    continue
                for pos in possibles[i]:
                    self.possible[pos] = equals[:]
                hist += equals
        self.solve_naked_pairs()

    def solve_naked_quads(self):
        ''' Identifies naked quads in rows, columns and squares '''
        self.naked_pairs(ROWS, 3)
        self.naked_pairs(COLS, 3)
        self.naked_pairs(SQUARES, 3)
        self.solve_hidden_pairs()

    def solve_hidden_quads(self):
        ''' Identifies hidden quads in rows, columns and squares '''
        self.hidden_pairs(ROWS, 4)
        self.hidden_pairs(COLS, 4)
        self.hidden_pairs(SQUARES, 4)
        self.solve_naked_quads()

    def is_solved(self):
        ''' Returns True if all squares are full, else False '''
        return list(self.board.values()).count(0) == 0

    def solve(self):
        ''' Solves an incomplete sudoku grid '''
        self.solve_naked_singles()
        if not self.is_solved():
            self.solve_hidden_singles()
        if not self.is_solved():
            self.solve_naked_pairs()
        if not self.is_solved():
            self.solve_hidden_pairs()
        if not self.is_solved():
            self.solve_naked_quads()
        if not self.is_solved():
            self.solve_hidden_quads()
        if not self.is_solved():
            print("\nHmm this is a tough one, we need some backtracking here!\n")
            if not self.solve_backtrack():
                print("\nCannot be solved\n")

    def solve_backtrack(self):
        ''' Recursively solve the Sudoku grid by using trial and error '''
        empty = self.get_empty()
        if not empty:
            return True
        for i in range(1, 10):
            if i in self.possible_move(empty):
                self.board[empty] = i
                if self.solve_backtrack():
                    return True
                self.board[empty] = 0
        return False

    def get_empty(self):
        ''' Returns first empty position. If no empty positions found, return None '''
        for pos in BOARD:
            if self.board[pos] == 0:
                return pos
        return None

    def display(self):
        ''' Displays the sudoku board '''
        print()
        for i in range(0, 73, 9):
            print(*list(self.board.values())[i : i + 9])
        print()

    def is_valid(self):
        ''' Returns True if current sudoku board is a correct solution, else False '''
        return self.group_validate(ROWS) and self.group_validate(COLS) and self.group_validate(SQUARES)

    def validate(self):
        ''' Prints message for verdict of solution '''
        print("Verdict: \n")
        if self.is_valid():
            print("Answer seems totally correct, yay!")
        else:
            print("Uh, looks like something went wrong here...")
        print()

    def group_validate(self, GROUPS):
        ''' Checks if all numbers from 1 - 9 are present exactly once in the groups (rows, columns or squares) '''
        for group in GROUPS:
            contents = [self.board[pos] for pos in group]
            if not all(contents.count(i) == 1 for i in range(1, 10)):
                return False
        return True

values = []

if len(sys.argv) == 2:
    filename = sys.argv[1]

if os.path.isfile(filename):
    with open(filename) as f:
        for row in f:
            values += [int(x) for x in row.strip()]
else:
    print("No such file exists")
    sys.exit(0)

board = dict(zip(BOARD, values))

S = Sudoku(board)
print("Here is the original board:\n")
S.display()
print("\nSolving:\n")
S.solve()

S.display()
S.validate()
