import solver

class UserInterface:
    def __init__(self):
        self.solver = solver.SudokuSolver()

    def get_puzzle_from_user(self):
        print("Enter the Sudoku puzzle, row by row. Use 0 for empty cells.")
        board = []
        for i in range(9):
            while True:
                row_str = input(f"Enter row {i+1} (9 digits, 0 for empty): ")
                if len(row_str) == 9 and row_str.isdigit():
                    row = [int(digit) for digit in row_str]
                    board.append(row)
                    break
                else:
                    print("Invalid input. Please enter exactly 9 digits.")
        self.solver.set_board(board)

    def display_solution(self):
        if self.solver.solve():
            print("\nSudoku Solved:")
            board = self.solver.get_board()
            for r in range(9):
                if r % 3 == 0 and r != 0:
                    print("- - - - - - - - - - - - ")
                for c in range(9):
                    if c % 3 == 0 and c != 0:
                        print(" | ", end="")
                    if c == 8:
                        print(board[r][c])
                    else:
                        print(str(board[r][c]) + " ", end="")
        else:
            print("No solution exists for the given Sudoku.")

    def run(self):
        self.get_puzzle_from_user()
        self.display_solution()
