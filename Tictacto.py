import tkinter as tk
from tkinter import messagebox as mb
import math
def new_game():
    global b, game_mode, current_player
    b = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        buttons[i].config(text=" ", state="normal")
    if game_mode == "Multiplayer":
        current_player = -1  
def get_winner(b):
    L = [[0, 1, 2], [3, 4, 5], [6, 7, 8],[0, 3, 6], [1, 4, 7], [2, 5, 8],[0, 4, 8], [2, 4, 6]]
    for i in L:
        if b[i[0]] == b[i[1]] == b[i[2]] and b[i[0]] != 0:
            return b[i[0]]
    return 0
def is_draw(b):
    return (0 not in b)

def evaluate_move(b):
    w= get_winner(b)
    if w== 1:
        return 1  
    elif w== -1:
        return -1  
    elif is_draw(b):
        return 0  
    return None  
def minimax(b, depth, m):
    result = evaluate_move(b)
    if result is not None:
        return result
    if m:
        best = -math.inf
        for i in range(9):
            if b[i] == 0:
                b[i] = 1  
                score = minimax(b, depth + 1, 0)
                b[i] = 0
                best = max(score, best)
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == 0:
                b[i] = -1  
                score = minimax(b, depth + 1, 1)
                b[i] = 0
                best = min(score, best)
        return best

def ai():
    best = -math.inf 
    move = None
    for i in range(9):
        if b[i] == 0:
            b[i] = 1
            score = minimax(b, 0, False)
            b[i] = 0
            if score > best:
                best = score
                move = i
    if move is not None:
        b[move] = 1
        buttons[move].config(text="O")
        check()

def button_click(i):
    global current_player
    if b[i] == 0:
        if game_mode == "AI" and current_player == -1:
            b[i] = -1
            buttons[i].config(text="X")
            check()
            if not is_draw(b) and get_winner(b) == 0:
                ai()
        elif game_mode == "Multiplayer":
            if b[i] == 0:
                b[i] = current_player
                buttons[i].config(text="X" if current_player == -1 else "O")
                check()
                if not is_draw(b) and get_winner(b) == 0:
                    current_player = -current_player

def check():
    w= get_winner(b)
    if w== 1:
        mb.showinfo("Game Over", "AI wins!")
        disable_buttons()
    elif w== -1:
        mb.showinfo("Game Over", "Player 1 wins!")
        disable_buttons()
    elif w== 1:
        mb.showinfo("Game Over", "Player 2 wins!")
        disable_buttons()
    elif is_draw(b):
        mb.showinfo("Game Over", "Draw!")
        disable_buttons()

def disable_buttons():
    for button in buttons:
        button.config(state="disabled")

def select_game_mode(mode):
    global game_mode, current_player
    game_mode = mode
    current_player = -1  
    new_game()
def UI():
    global buttons
    r = tk.Tk()
    r.title("TicTacToe Game")
    frame = tk.Frame(r)
    frame.pack()
    
    tk.Button(r, text="Single vs AI", command=lambda: select_game_mode("AI")).pack()
    tk.Button(r, text="Multiplayer", command=lambda: select_game_mode("Multiplayer")).pack()
    frame= tk.Frame(r)
    frame.pack()
    buttons = []
    for i in range(9):
        button= tk.Button(frame, text="", width=10, height=3,command=lambda i=i: button_click(i))
        button.grid(row=i//3, column=i%3)
        buttons.append(button)
    
    new_game_button = tk.Button(r, text="New Game", command=new_game)
    new_game_button.pack()
    r.mainloop()
b = [0,0,0,0,0,0,0,0,0]
game_mode= None
current_player= None
UI()
