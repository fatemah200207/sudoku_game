import tkinter as tk
from tkinter import messagebox
from collections import deque

# Check if placing a number is valid
def is_valid_move(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
    for x in range(9):
        if grid[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

# Find the next empty cell
def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

# BFS Sudoku Solver
def bfs_sudoku_solver(grid):
    queue = deque([grid])
    while queue:
        current_grid = queue.popleft()
        if not find_empty_cell(current_grid):
            return current_grid
        row, col = find_empty_cell(current_grid)
        for num in range(1, 10):
            if is_valid_move(current_grid, row, col, num):
                new_grid = [row[:] for row in current_grid]
                new_grid[row][col] = num
                queue.append(new_grid)
    return None

# DFS-based Sudoku solver
def dfs_sudoku_solver(grid):
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True
    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if dfs_sudoku_solver(grid):
                return True
            grid[row][col] = 0
    return False

# UCS-based Sudoku solver
def ucs_sudoku_solver(start_grid):
    queue = [start_grid]
    while queue:
        current_grid = queue.pop(0)
        if not find_empty_cell(current_grid):
            return current_grid

        row, col = find_empty_cell(current_grid)
        for num in range(1, 10):
            if is_valid_move(current_grid, row, col, num):
                new_grid = [current_row[:] for current_row in current_grid]
                new_grid[row][col] = num
                queue.append(new_grid)

    return None

class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.board = []
        self.create_board()
        self.create_buttons()

    def create_board(self):
        for i in range(9):
            row = []
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                    entry.insert(0, str(self.puzzle[i][j]))
                    entry.config(state='disabled', disabledbackground="lightgray", disabledforeground="black")
                else:
                    entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                row.append(entry)
            self.board.append(row)

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=9, column=0, columnspan=9, pady=10)
        bfs_button = tk.Button(button_frame, text="Solve using BFS", command=self.solve_bfs, width=15)
        bfs_button.grid(row=0, column=0, padx=5)
        dfs_button = tk.Button(button_frame, text="Solve using DFS", command=self.solve_dfs, width=15)
        dfs_button.grid(row=0, column=1, padx=5)
        ucs_button = tk.Button(button_frame, text="Solve using UCS", command=self.solve_ucs, width=15)
        ucs_button.grid(row=0, column=2, padx=5)
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_board, width=15)
        clear_button.grid(row=0, column=3, padx=5)

    def extract_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.board[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            grid.append(row)
        return grid

    def update_board(self, solution):
        if solution:
            for i in range(9):
                for j in range(9):
                    self.board[i][j].delete(0, tk.END)
                    self.board[i][j].insert(0, str(solution[i][j]))
                    if self.puzzle[i][j] == 0:
                        self.board[i][j].config(state='normal')
                    else:
                        self.board[i][j].config(state='disabled')
        else:
            messagebox.showerror("Error", "No solution found.")

    def validate_and_fix_grid(self):
        current_grid = self.extract_grid()
        valid = True

        for i in range(9):
            row_nums = set()
            col_nums = set()
            for j in range(9):
                if current_grid[i][j] != 0:
                    if current_grid[i][j] in row_nums:
                        valid = False
                    else:
                        row_nums.add(current_grid[i][j])

                if current_grid[j][i] != 0:
                    if current_grid[j][i] in col_nums:
                        valid = False
                    else:
                        col_nums.add(current_grid[j][i])

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                nums = set()
                for i in range(box_row, box_row + 3):
                    for j in range(box_col, box_col + 3):
                        if current_grid[i][j] != 0:
                            if current_grid[i][j] in nums:
                                valid = False
                            else:
                                nums.add(current_grid[i][j])

        if not valid:
            messagebox.showinfo("Invalid Input", "Conflicts detected. Please fix them.")
        return valid

    def solve_bfs(self):
        if self.validate_and_fix_grid():  
            current_grid = self.extract_grid()
            solution = bfs_sudoku_solver(current_grid)
            self.update_board(solution)

    def solve_dfs(self):
        if self.validate_and_fix_grid(): 
            current_grid = self.extract_grid()
            if dfs_sudoku_solver(current_grid):
                self.update_board(current_grid)
            else:
                messagebox.showerror("Error", "No solution found.")

    def solve_ucs(self):
        if self.validate_and_fix_grid():  
            current_grid = self.extract_grid()
            solution = ucs_sudoku_solver(current_grid)
            self.update_board(solution)

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    self.board[i][j].delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuUI(root)
    root.mainloop()
