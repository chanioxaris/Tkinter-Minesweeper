import sys
import random
import time
import math
import tkinter
from PIL import ImageTk, Image


class Minesweeper():
         
    def __init__(self, master, size, mines):
    
        self.master = master
        self.board_size = size
        self.mines = mines
        self.flagged = 0
        self.total_flagged = 0
        
        self.master.title("Minesweeper")
        self.master.resizable(width = tkinter.FALSE, height = tkinter.FALSE)
        self.master.geometry('{}x{}'.format(self.board_size*35, self.board_size*35 + 50))
               
        self.img_bomb = ImageTk.PhotoImage(Image.open("../img/bomb.png"))        
        self.img_flag = ImageTk.PhotoImage(Image.open("../img/flag.png"))
        self.empty = ImageTk.PhotoImage(Image.open("../img/empty.png"))
        self.default = ImageTk.PhotoImage(Image.open("../img/default.png"))
        self.img_1 = ImageTk.PhotoImage(Image.open("../img/1.png"))
        self.img_2 = ImageTk.PhotoImage(Image.open("../img/2.png"))
        self.img_3 = ImageTk.PhotoImage(Image.open("../img/3.png"))
        self.img_4 = ImageTk.PhotoImage(Image.open("../img/4.png"))
        self.img_5 = ImageTk.PhotoImage(Image.open("../img/5.png"))
        self.img_6 = ImageTk.PhotoImage(Image.open("../img/6.png"))
        self.img_7 = ImageTk.PhotoImage(Image.open("../img/7.png"))
        self.img_8 = ImageTk.PhotoImage(Image.open("../img/8.png"))
        
        self.images = {0:self.empty, 1:self.img_1, 2:self.img_2, 3:self.img_3, 4:self.img_4, 5:self.img_5, 6:self.img_6, 7:self.img_7, 8:self.img_8}
        
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.status = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        
        self.GenerateMines()
        
        self.FindNeighors()
        
        self.Play()
    
    
    def GenerateMines(self):
        mines_pos = random.sample(range(self.board_size**2), self.mines)
        
        for i in mines_pos:
            self.board[i // self.board_size][i % self.board_size] = -1
                      
    
    def FindNeighors(self):
        
        for row in range(self.board_size):            
            for col in range(self.board_size):
                
                counter = 0
                
                if self.board[row][col] == -1:
                    continue
                
                if row-1 >=0 and col-1 >= 0 and self.board[row-1][col-1] == -1:
                    counter += 1
                    
                if row-1 >=0 and col >= 0 and self.board[row-1][col] == -1:
                    counter += 1
                    
                if row-1 >=0 and col+1 < self.board_size and self.board[row-1][col+1] == -1:
                    counter += 1
                    
                if row >=0 and col-1 >= 0 and self.board[row][col-1] == -1:
                    counter += 1
                    
                if row >=0 and col+1 < self.board_size and self.board[row][col+1] == -1:
                    counter += 1
                    
                if row+1 < self.board_size and col-1 >= 0 and self.board[row+1][col-1] == -1:
                    counter += 1
                    
                if row+1 < self.board_size and col >= 0 and self.board[row+1][col] == -1:
                    counter += 1
                
                if row+1 < self.board_size and col+1 < self.board_size and self.board[row+1][col+1] == -1:
                        counter += 1


                self.board[row][col] = counter
    
    
    def OnRightClick(self, event, coord):       
        
        self.total_flagged += 1
        
        self.labelText.set("Flags remain: " + str(self.mines - self.total_flagged))
        
        
        if self.status[coord[1]][coord[0]] == 0:
            self.buttons[coord[0]][coord[1]].configure(image = self.img_flag)
            
            if self.board[coord[1]][coord[0]] == -1:
                self.flagged += 1
        
            self.status[coord[1]][coord[0]] = 2

    
    def OnLeftClick(self, event, coord):
        
        if self.board[coord[1]][coord[0]] == -1:
            self.buttons[coord[0]][coord[1]].configure(image = self.img_bomb)
            self.master.update_idletasks()
            self.Lose()
                       
        if self.status[coord[1]][coord[0]] != 1:    
            key = self.board[coord[1]][coord[0]]
            
            if key == 0:
                self.buttons[coord[0]][coord[1]].configure(image = self.images[0])
                self.RevealEmpty(coord[1], coord[0])
                
            elif key > 0 and key <= 8:
                self.buttons[coord[0]][coord[1]].configure(image = self.images[key])
                
                if self.status[coord[1]][coord[0]] == 2:
                    self.total_flagged -= 1
                   
            self.labelText.set("Flags remain: " + str(self.mines - self.total_flagged))
            self.status[coord[1]][coord[0]] = 1
           
            
        if (self.board_size**2 - self.mines) == sum(x.count(1) for x in self.status):
            self.Win()
    
    
    def RevealEmpty(self, row, col):
                
        if row-1 >=0 and col-1 >= 0 and self.status[row-1][col-1] != 1:           
            key = self.board[row-1][col-1]
            self.buttons[col-1][row-1].configure(image = self.images[key])
                       
            if self.status[row-1][col-1] == 2:
                self.total_flagged -= 1
            
            self.status[row-1][col-1] = 1

            if key == 0:
                self.RevealEmpty(row-1, col-1)
            
        if row-1 >=0 and col >= 0 and self.status[row-1][col] != 1:
            key = self.board[row-1][col]
            self.buttons[col][row-1].configure(image = self.images[key])
            
            if self.status[row-1][col] == 2:
                self.total_flagged -= 1
            
            self.status[row-1][col] = 1 
            
            if key == 0:
                self.RevealEmpty(row-1, col)
            
        if row-1 >=0 and col+1 < self.board_size and self.status[row-1][col+1] != 1:
            key = self.board[row-1][col+1]
            self.buttons[col+1][row-1].configure(image = self.images[key])
            
            if self.status[row-1][col+1] == 2:
                self.total_flagged -= 1
            
            self.status[row-1][col+1] = 1
            
            if key == 0:
                self.RevealEmpty(row-1, col+1)
            
        if row >=0 and col-1 >= 0 and self.status[row][col-1] != 1:
            key = self.board[row][col-1]
            self.buttons[col-1][row].configure(image = self.images[key])
            
            if self.status[row][col-1] == 2:
                self.total_flagged -= 1
            
            self.status[row][col-1] = 1
            
            if key == 0:
                self.RevealEmpty(row, col-1)
            
        if row >=0 and col+1 < self.board_size and self.status[row][col+1] != 1:
            key = self.board[row][col+1]
            self.buttons[col+1][row].configure(image = self.images[key])
            
            if self.status[row][col+1] == 2:
                self.total_flagged -= 1
            
            self.status[row][col+1] = 1
            
            if key == 0:
                self.RevealEmpty(row, col+1)
            
        if row+1 < self.board_size and col-1 >= 0 and self.status[row+1][col-1] != 1:
            key = self.board[row+1][col-1]
            self.buttons[col-1][row+1].configure(image = self.images[key])
            
            if self.status[row+1][col-1] == 2:
                self.total_flagged -= 1
            
            self.status[row+1][col-1] = 1
            
            if key == 0:
                self.RevealEmpty(row+1, col-1)
            
        if row+1 < self.board_size and col >= 0 and self.status[row+1][col] != 1:
            key = self.board[row+1][col]
            self.buttons[col][row+1].configure(image = self.images[key])
            
            if self.status[row+1][col] == 2:
                self.total_flagged -= 1
            
            self.status[row+1][col] = 1
            
            if key == 0:
                self.RevealEmpty(row+1, col)
        
        if row+1 < self.board_size and col+1 < self.board_size and self.status[row+1][col+1] != 1:
            key = self.board[row+1][col+1]
            self.buttons[col+1][row+1].configure(image = self.images[key])
            
            if self.status[row+1][col+1] == 2:
                self.total_flagged -= 1
            
            self.status[row+1][col+1] = 1
            
            if key == 0:
                self.RevealEmpty(row+1, col+1)
          
         
    def Play(self):
        
        self.buttons = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        for i in range(self.board_size):
           for j in range(self.board_size):
                self.buttons[i][j] = tkinter.Button(self.master, height=35, width=35)
                self.buttons[i][j].place(x = i*35, y = j*35)
                self.buttons[i][j].configure(image = self.default)                
                self.buttons[i][j].bind("<Button-1>", lambda event, arg = (i, j): self.OnLeftClick(event, arg))
                self.buttons[i][j].bind("<Button-3>", lambda event, arg = (i, j): self.OnRightClick(event, arg))
                
        
        self.labelText = tkinter.StringVar()
        self.labelText.set("Flags remain: " + str(self.mines))
        
        text1 = tkinter.Label(self.master, textvariable = self.labelText)
        text1.config(font = ("Courier", 10))
        text1.pack(side = tkinter.BOTTOM)

        self.start_time = time.time()
        
               
    def PlayAgain(self, prev, size, mines):
        
        prev.destroy()
        
        ConfigureGame(size, mines)   
    
            
    def Win(self):
        
        self.end_time = time.time()
        
        self.master.withdraw()
  
        d = DialogWin(self.master, self.board_size, self.mines, self.end_time - self.start_time)

        self.master.wait_window(d.top)
    
    
    def Lose(self):
        
        self.master.withdraw()
        
        d = DialogLose(self.master, self.board_size, self.mines)
              
        self.master.wait_window(d.top)
        
    
       
class DialogWin:

    def __init__(self, parent, size, mines, time):
      
        self.top = tkinter.Toplevel(parent)
        center(self.top)
        
        text1 = tkinter.Label(self.top, text = "You won!")       
        text1.config(font = ("Courier", 22), fg = "green")
        text1.pack(pady = 5)
           
        text2 = tkinter.Label(self.top, text = ("Your time is " + str(math.ceil(time)) + " seconds"))        
        text2.config(font = ("Courier", 10))    
        text2.pack()
        
        
        b1 = tkinter.Button(self.top, text="Play again", height = 1, width = 10, command = lambda : Minesweeper.PlayAgain(self, parent, size, mines))
        b1.pack(side = tkinter.LEFT)    
                        
        b2 = tkinter.Button(self.top, text="Close", height = 1, width = 10, command = parent.destroy)
        b2.pack(side = tkinter.RIGHT)
        
        
          
class DialogLose:

    def __init__(self, parent, size, mines):

        self.top = tkinter.Toplevel(parent)
        center(self.top)
        
        text1 = tkinter.Label(self.top, text = "You lost!")
        text1.config(font = ("Courier", 22), fg = "red")
        text1.pack(pady = 5)

             
        b1 = tkinter.Button(self.top, text="Play again", height = 1, width = 10, command = lambda : Minesweeper.PlayAgain(self, parent, size, mines))
        b1.pack(side = tkinter.LEFT)    
                        
        b2 = tkinter.Button(self.top, text="Close", height = 1, width = 10, command = parent.destroy)
        b2.pack(side = tkinter.RIGHT)  
        


def center(win):
        
        win.update_idletasks()
        
        width = win.winfo_width()
        height = win.winfo_height()
        
        x = (win.winfo_screenwidth() // 3) - (width // 3)
        y = (win.winfo_screenheight() // 3) - (height // 3)
        
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))



def ConfigureGame(size, mines):
    
        game = tkinter.Tk()  
    
        center(game)
    
        Minesweeper(game, size, mines) 
    
        game.mainloop()
    



if __name__ == "__main__":
    
    if sys.argv[1] == "-small" or sys.argv[1] == "-s":
        ConfigureGame(9, 10)
    elif sys.argv[1] == "-medium" or sys.argv[1] == "-m":
        ConfigureGame(15, 33)   
    elif sys.argv[1] == "-big" or sys.argv[1] == "-b":
        ConfigureGame(20, 86)
    else:
        print("Wrong input parameters! Please try again")