import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.is_clicked = [[False for _ in range(cols)] for _ in range(rows)]
        self.create_widgets()
        self.place_mines()
        self.game_over = False

    def create_widgets(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row][col] = tk.Button(
                    self.master, width=2, height=1, bd=1,
                    command=lambda r=row, c=col: self.click_button(r, c)
                )
                self.buttons[row][col].grid(row=row, column=col)
                self.buttons[row][col].bind("<Button-3>", lambda event, r=row, c=col: self.place_flag(event, r, c))

        restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        restart_button.grid(row=self.rows, columnspan=self.cols)

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_placed += 1
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] != -1:
                            self.board[r][c] += 1

    def click_button(self, row, col):
        if self.game_over or self.is_clicked[row][col]:
            return

        self.is_clicked[row][col] = True
        if self.board[row][col] == -1:
            self.buttons[row][col].config(bg="red")
            self.end_game()
        else:
            mines_around = self.board[row][col]
            self.buttons[row][col].config(text=str(mines_around), state=tk.DISABLED)
            if mines_around == 0:
                self.auto_reveal_cells(row, col)
            self.check_win()
        
    def auto_reveal_cells(self, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.rows and 0 <= c < self.cols and not self.is_clicked[r][c]:
                    self.click_button(r, c)

    def dfs_reveal_empty_cells(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols) or self.is_clicked[row][col]:
            return
        
        self.is_clicked[row][col] = True
        self.buttons[row][col].config(state=tk.DISABLED)

        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.click_button(r, c)

    def place_flag(self, event, row, col):
        if self.game_over or self.is_clicked[row][col]:
            return

        if self.buttons[row][col]["text"] == "F":
            self.buttons[row][col].config(text="")
            self.flags += 1
        elif self.flags > 0:
            self.buttons[row][col].config(text="F", bg="yellow")
            self.flags -= 1

    def check_win(self):
        unclicked_cells = sum(not self.is_clicked[r][c] for r in range(self.rows) for c in range(self.cols))
        if unclicked_cells == self.mines:
            self.end_game(True)

    def end_game(self, win=False):
        self.game_over = True
        if win:
            messagebox.showinfo("Congratulations!", "You won!")
        else:
            self.reveal_board()
            messagebox.showinfo("Game Over", "You clicked on a mine! Game Over.")

    def restart_game(self):
        self.master.destroy()
        start_game(self.rows, self.cols, self.mines)

    def reveal_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    self.buttons[row][col].config(text="X", bg="red")
                else:
                    mines_around = self.board[row][col]
                    self.buttons[row][col].config(text=str(mines_around), state=tk.DISABLED)


def start_game(rows, cols, mines):
    root = tk.Tk()
    root.title("Minesweeper")

    game = Minesweeper(root, rows, cols, mines)
    root.mainloop()

start_game(15, 15, 50)
