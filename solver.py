import random
import copy

class SudokuSolver:
    def __init__(self):
        self.board = [[0]*9 for _ in range(9)]
        self.steps = 0

    def set_board(self, board):
        self.board = [row[:] for row in board]
        self.steps = 0

    def get_board(self):
        return self.board

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return (r, c)
        return None

    def find_empty_mrv(self):
        min_options = 10
        best_cell = None

        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    choices_count = 0
                    for num in range(1, 10):
                        if self.is_valid(num, (r, c)):
                            choices_count += 1

                    if choices_count < min_options:
                        min_options = choices_count
                        best_cell = (r, c)
                        if min_options == 1:
                            return best_cell
        return best_cell

    def is_valid(self, num, pos):
        for c in range(9):
            if self.board[pos[0]][c] == num and pos[1] != c:
                return False

        for r in range(9):
            if self.board[r][pos[1]] == num and pos[0] != r:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for r in range(box_y*3, box_y*3 + 3):
            for c in range(box_x*3, box_x*3 + 3):
                if self.board[r][c] == num and (r,c) != pos:
                    return False

        return True

    def is_board_valid(self):
        for r in range(9):
            for c in range(9):
                val = self.board[r][c]
                if val != 0:
                    self.board[r][c] = 0
                    valid = self.is_valid(val, (r, c))
                    self.board[r][c] = val
                    if not valid:
                        return False
        return True

    def solve(self, use_mrv=True, callback=None):
        find = self.find_empty_mrv() if use_mrv else self.find_empty()
        if not find:
            return True
        row, col = find

        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.board[row][col] = i
                self.steps += 1

                if callback:
                    callback(self.board, row, col, i, "assign")

                if self.solve(use_mrv, callback):
                    return True

                self.board[row][col] = 0
                if callback:
                    callback(self.board, row, col, 0, "backtrack")

        return False

    def solve_randomized(self):
        find = self.find_empty()
        if not find:
            return True
        row, col = find

        nums = list(range(1, 10))
        random.shuffle(nums)

        for i in nums:
            if self.is_valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve_randomized():
                    return True

                self.board[row][col] = 0

        return False

    def generate_puzzle(self, difficulty):
        self.board = [[0]*9 for _ in range(9)]

        self.solve_randomized()

        if difficulty == "Easy":
            to_remove = 35
        elif difficulty == "Medium":
            to_remove = 45
        elif difficulty == "Hard":
            to_remove = 55
        else:
            to_remove = 45

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        for i in range(to_remove):
            r, c = cells[i]
            self.board[r][c] = 0
        self.steps = 0

    def get_hint(self):
        if not self.is_board_valid():
            return None, "The current board is invalid. Please resolve conflicting numbers first!"

        board_copy = copy.deepcopy(self.board)
        solver_copy = SudokuSolver()
        solver_copy.set_board(board_copy)

        if solver_copy.solve(use_mrv=True):
            solved_board = solver_copy.get_board()
            empty_cells = [(r, c) for r in range(9) for c in range(9) if self.board[r][c] == 0]

            if not empty_cells:
                return None, "The board is already solved!"

            empty_cells.sort(key=lambda pos: sum(1 for num in range(1, 10) if self.is_valid(num, pos)))
            row, col = empty_cells[0]
            val = solved_board[row][col]
            return (row, col, val), None
        else:
            return None, "No solution exists for this Sudoku configuration."
