#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from random import randint

app=tk.Tk()
app.title("Puissance 4")
canvas = tk.Canvas(app, width=288, height=250, bg="navy blue")
canvas.grid(row=1, column=0, columnspan=8)
case=288/7
onClick = tk.BooleanVar()
onClick.set(False)

##Game board initialisation
def init_game () :
        global board,player_1,player_2,player
        print()
        print("===============")
        print("New Game")
        print("===============")
        player_1 = 1
        player_2 = -1
        player = -1
        board = [[0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],]
        
        y0=10
        y1=40
        y2=15
        y3=35
        for j in range(6) :
                x0=10
                x1=40
                x2=170
                x3=190
                for i in range(7) :
                    canvas.create_oval(x0,y0,x1,y1,fill="white",tags=str(int(x0/case))+"-"+str(int(y0/case)))
                    x0+=40
                    x1+=40
                    x2+=30
                    x3+=30
                y0+=40
                y1+=40
                y2+=40
                y3+=40
        play_with_ai(board)

##Click recuperation
def click (event, color):
        global onClick, turn, player
        onClick.set(True)
        i=5
        col=int(event.x/case)
        row=int(event.y/case)
        while i >= 0 :
                if board[i][col]== 0 :
                        board[i][col]=1
                        canvas.itemconfig(str(col)+"-"+str(i), fill=color)
                        break
                elif board[i][col] != 0 and i == 0:
                        tk.messagebox.showinfo("Oooh... :( ","You're trying to play in a full column...")
                        onClick.set(False)
                        player=player_turn()
                        break
                else :
                        i = i - 1
                        
new_game=tk.Button(app, text="New game", command=init_game, width=41)
new_game.grid(row=0, column=0, columnspan=8, sticky=tk.W)

##Pawn coloration 
def click_bt (event) :
        return click(event,"red")

##Winner messagebox              
def end_game(winner):
        if winner == "Player 1" :
                tk.messagebox.showinfo("You win !", "Congratulation, you win !")
        if winner == "Player 2" :
                tk.messagebox.showinfo("You lose ! :( ","Try again, you lose !")
        
##Player determination 
def player_turn () :
        global player, player_1, player_2, onClick, board
        if player == -1 :
                player = player_1
        else :
                player = player_2
        return player

##Pawn placing 
def pawn_placing(col, player, board):
        i = 5
        while i >= 0 :
                if board[i][col]== 0 :
                        board[i][col]=player
                        canvas.itemconfig(str(col)+"-"+str(i), fill="yellow")
                        return i
                elif board[i][col] != 0 and i == 0:
                        break
                i = i - 1


##Board verification 
def verification(board) :
        global winner
        winner = ""
    ###Column
        for j in range(7):
                for i in range(3):
                        if board[i][j]+board[i+1][j]+board[i+2][j]+board[i+3][j] == 4 :
                                winner = "Player 1"
                        
                        elif board[i][j]+board[i+1][j]+board[i+2][j]+board[i+3][j] == -4 :
                                winner = "Player 2"
                                        
                        
    ###Line
        for i in range(6):
                for j in range(4):
                        if board[i][j]+board[i][j+1]+board[i][j+2]+board[i][j+3] == 4 :
                              winner = "Player 1"
                              
                        elif board[i][j]+board[i][j+1]+board[i][j+2]+board[i][j+3] == -4 :
                              winner = "Player 2"


    ###Rising diagonale
        for i in range(3):
                for j in range(4):
                        if board[i][j]+board[i+1][j+1]+board[i+2][j+2]+board[i+3][j+3] == 4 :
                              winner = "Player 1"
                              
                        elif board[i][j]+board[i+1][j+1]+board[i+2][j+2]+board[i+3][j+3] == -4 :
                              winner = "Player 2"

    ###Descending diagonale
        for i in range(3):
                for j in range(3,7):
                        if board[i][j]+board[i+1][j-1]+board[i+2][j-2]+board[i+3][j-3] == 4 :
                              winner = "Player 1"
                              
                        elif board[i][j]+board[i+1][j-1]+board[i+2][j-2]+board[i+3][j-3] == -4 :
                              winner = "Player 2"
        if winner != "" :
                return True, winner
        else :
                return False

### AI move evaluating 
def eval_col_ai (board):
        global score, cols,col, col_j
        col_j = -1
        score = 0
        player_score = 0
        cols = []
        col = -1
        ##Column
        for j in range(7):
                for i in range(3):
                        if board[i][j]+board[i+1][j]+board[i+2][j]+board[i+3][j] < score :
                                cols = [board[i][j],board[i+1][j],board[i+2][j],board[i+3][j]]
                                if 1 not in cols :
                                        score = board[i][j]+board[i+1][j]+board[i+2][j]+board[i+3][j]
                                        col = j
                        if board[i][j]+board[i+1][j]+board[i+2][j]+board[i+3][j]>player_score : 
                                player_score = board[i][j]+board[i+1][j]+board[i+2][j]+board[i+3][j]
                                col_j = j

        ##Line
        for i in range(6):
                for j in range(4):
                        if board[i][j]+board[i][j+1]+board[i][j+2]+board[i][j+3] < score :
                                cols = [board[i][j],board[i][j+1],board[i][j+2],board[i][j+3]]
                                if 1 not in cols :
                                        score = board[i][j]+board[i][j+1]+board[i][j+2]+board[i][j+3]
                                        k = 0
                                        while k < len(cols):
                                                if cols[k] == 0 :
                                                        col = j + k
                                                k += 1
                        if board[i][j]+board[i][j+1]+board[i][j+2]+board[i][j+3] > player_score :
                                player_score = board[i][j]+board[i][j+1]+board[i][j+2]+board[i][j+3]
                                col_j = j
        ##Rising diagonal
        for i in range(3):
                for j in range(4):
                        if board[i][j]+board[i+1][j+1]+board[i+2][j+2]+board[i+3][j+3] < score :
                                cols = [board[i][j],board[i+1][j+1],board[i+2][j+2],board[i+3][j+3]]
                                if 1 not in cols :
                                        score = board[i][j]+board[i+1][j+1]+board[i+2][j+2]+board[i+3][j+3]
                                        k = 0
                                        while k < len(cols):
                                                if cols[k] == 0 :
                                                        col = j + k
                                                k += 1
                                        
        ##Descending diagonal
        for i in range(3):
                for j in range(3,7):
                        if board[i][j]+board[i+1][j-1]+board[i+2][j-2]+board[i+3][j-3] < score :
                                cols = [board[i][j],board[i+1][j-1],board[i+2][j-2],board[i+3][j-3]]
                                if 1 not in cols :
                                        score = board[i][j]+board[i+1][j-1]+board[i+2][j-2]+board[i+3][j-3]
                                        k = 0
                                        while k < len(cols):
                                                if cols[k] == 0 :
                                                        col = j + k
                                                k += 1
        if score > -3 and player_score == 3 :
                return col_j
        if col == -1 :
                col = randint(0,6)
        return col

##Launch a game
def play_with_ai(game_board):
        global onClick
        while verification(game_board)== False :
                player = player_turn()
                if player == player_1 :
                                canvas.bind("<Button-1>", click_bt)
                                app.wait_variable(onClick)
                                verification(game_board)
                else :
                                pawn_placing(eval_col_ai(game_board),player_2,game_board)
                                verification(game_board)
        end_game(winner)

init_game()
app.resizable(False,False)
app.mainloop()
