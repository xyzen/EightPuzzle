import tkinter as tk
import tkinter.font as font
import EightPuzzleSolver as solver

class EightPuzzle(tk.Tk):
    
    default = (
        (8, 6, 7),
        (2, 5, 4),
        (3, 0, 1)
    )
    
    def __init__(self, icon = None, state = default):
        tk.Tk.__init__(self)
        self.title("EightPuzzle")
        self.resizable(False, False)
        self.state = self.default
        self.buttons=[]
        self.setButtons()
        self.solution = tk.Label(self, text=solver.AStarSearch(state))
        self.solution.grid(row = 4, columnspan = 3)
        
    def findZero(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j
        
    def setState(self, state):
        self.state = state
        self.refresh()
        
    def setButtons(self):
        for row in range(3):
            self.buttons.append([])
            for col in range(3):
                label = self.state[row][col]
                self.buttons[row].append(
                    tk.Button(
                        self, height = 3, width = 6,
                        text=str(label) if label != 0 else "",
                        command=lambda r=row, c=col: self.onClick(r, c),
                        relief = tk.SUNKEN if label == 0 else tk.RAISED,
                        font = font.Font(size=20)
                    )
                )
                self.buttons[row][col].grid(row=row, column=col)
                
    def move(self, row, col):
        row_e, col_e = self.findZero()
        if abs(row - row_e) + abs(col - col_e) != 1:
            return
        label = self.state[row][col]
        if label == 0:
            return
        new_state = [list(row) for row in self.state]
        new_state[row_e][col_e] = label
        new_state[row][col] = 0
        self.state = tuple([tuple(row) for row in new_state])
        
    def refresh(self):
        for row in range(3):
            for col in range(3):
                label = self.state[row][col]
                self.buttons[row][col].config(
                    text=str(label) if label != 0 else "",
                    relief = tk.RAISED if label != 0 else tk.SUNKEN
                )
                
    def onClick(self, row, col):
        self.move(row, col)
        self.refresh()
        self.search()

    def search(self):
        msg = solver.AStarSearch(self.state)
        if msg == "":
            msg = "Solved"
        self.solution.config(text=msg)
        
if __name__ == "__main__":
    EightPuzzle().mainloop()
