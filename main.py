#! /usr/bin/python

from PIL import ImageTk
import tkinter as tk
from PIL import Image
import numpy as np

import pieces as pcs
import board as bd
import game as game


top = tk.Tk()
top.title("Chess Board!!")

#Create frame for board and pieces on board
sqr_size=100
board_frame= tk.Frame(top,width=sqr_size*8,height=sqr_size*8)
board_frame.pack(side='right')

board_canvas= tk.Canvas(board_frame,width=sqr_size*8,height=sqr_size*8)
board_canvas.pack(fill='both', expand=1)

#Create frame on the left
left_frame=tk.Frame(top,width=100)
left_frame.pack(side='left',fill='both',expand=1)

#perhaps add clause here --if near some object, THEN bind to clicker
mycanvas = tk.Canvas(left_frame,bg='white')
mycanvas.pack(fill='both',expand=1)


""" TO DO
-En passant
-line of sight implementation for bishop/rook/queen
-castling
-The full game (check, turns, etc.)
"""

myboard=bd.Board(board_canvas,sqr_size)
myboard.create_board()
first_game = game.Player_Game("Zach","Other",myboard)
first_game.new_game()

#knight=pcs.Knight(myboard,board_canvas,'merida/320/BlackKnight.png',sqr_size)
#bishop=pcs.Bishop(myboard,board_canvas,'merida/320/BlackBishop.png',sqr_size)
#rook=pcs.Rook(myboard,board_canvas,'merida/320/BlackRook.png',sqr_size)
#queen=pcs.Queen(myboard,board_canvas,'merida/320/BlackQueen.png',sqr_size)
#king=pcs.King(myboard,board_canvas,'merida/320/BlackKing.png',sqr_size)



top.mainloop()
