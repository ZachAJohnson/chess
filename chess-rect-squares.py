#! /usr/bin/python

from PIL import ImageTk
import tkinter as tk
from PIL import Image
import numpy as np


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

class Piece():
    def __init__(self,image_file,square_size,start_coords=(450,350) ):
        #define class variables
        self.sq_w =square_size
        self.sq_h =square_size
        self.image_file=image_file
        self.mycanvas=board_canvas
        self.start_x=start_coords[0]
        self.start_y=start_coords[1]

        ##Now functions to create draggable pieces
        self.import_image()
        self.make_drag()

    def import_image(self):
        self.im=Image.open(self.image_file)
        im_w, im_h =self.im.size
        scale=self.sq_h/im_h
        self.im=self.im.resize(  (int(im_w*scale),int(im_h*scale)) )#scales based on height only
        self.ph= ImageTk.PhotoImage(self.im)
        self.Id= self.mycanvas.create_image(self.start_x,self.start_y,image=self.ph)
        self.mycanvas.image=self.ph

    def pickup(self,event):
        board_frame= tk.Frame(top,width=sqr_size*8,height=sqr_size*8)
        'print(event.x,event.y)'
        self.init_coords=self.mycanvas.coords(self.Id)

    def move(self,event):
        #print(event.x,event.y)
        x,y = (event.x,event.y)
        self.mycanvas.coords(self.Id,x,y)

    #drop for all pieces
    def drop(self,moveset,pos): #pos=position
        init_square=self.board.get_nboard(  tuple(self.init_coords) )
        moves=moveset+init_square

        #create small square to determine number of items at drop coords
        nearest_list=list(board_canvas.find_overlapping(pos[0]-1,pos[1]-1,pos[0]+1,pos[1]+1))
        nearest_list.remove(self.Id)
        if len(nearest_list)==1:
            nearest=nearest_list[0]
            nearest_coords=self.mycanvas.coords(nearest)
            new_x=(nearest_coords[0]+nearest_coords[2])/2
            new_y=(nearest_coords[1]+nearest_coords[3])/2
            new_coords=(new_x,new_y)
            new_n=self.board.get_nboard(new_coords)
            if new_n in moves:
                self.mycanvas.coords(self.Id,new_coords)
            else:
                self.mycanvas.coords(self.Id,self.init_coords)
                print("nope!!")

        else: self.mycanvas.coords(self.Id,self.init_coords)

class Board():

    def __init__(self):
        'do nothing'

    def create_board(self,pieces_set='merida'):
        pieces_files={'merida':'merida/320/'}
        x0, y0= (0,0)
        color=['salmon4','white']
        self.alpha=('','A','B','C','D','E','F','G','H')
        self.aboard={}
        self.nboard={}

        for r in range(8):
            for c in range(8):
                rect_coords=[x0 + c*sqr_size, y0+r*sqr_size,x0+(c+1)*sqr_size,y0+(r+1)*sqr_size]
                board_canvas.create_rectangle(rect_coords,width=2,fill=color[(r+c)%2])
                coords=( (rect_coords[0]+rect_coords[2])/2, (rect_coords[1]+rect_coords[3])/2 )
                self.aboard['{}{}'.format(self.alpha[c+1],8-r)]=coords
                self.nboard['{}{}'.format(8-r,c+1) ]=coords

    def layout_pieces(self):
        row=[1,8]
        side=['White','Black']
        p_row=[2,7]

        for i in range(2):
            r=row[i]
            c=side[i]
            p_r=p_row[i]

            bknight_file='{}/{}{}.png'.format(self.pieces_set,c ,'Knight')
            Piece(bknight_file,sqr_size,self.aboard['B{}'.format(r) ])
            Piece(bknight_file,sqr_size,self.aboard['G{}'.format(r) ])
            bbishop_file='{}/{}{}.png'.format(self.pieces_set,c,'Bishop')
            Piece(bbishop_file,sqr_size,self.aboard['C{}'.format(r)])
            Piece(bbishop_file,sqr_size,self.aboard['F{}'.format(r)])
            brook_file='{}/{}{}.png'.format(self.pieces_set,c,'Rook')
            Piece(brook_file,sqr_size,self.aboard['A{}'.format(r)])
            Piece(brook_file,sqr_size,self.aboard['H{}'.format(r)])
            bpawn_file='{}/{}{}.png'.format(self.pieces_set,c,'Pawn')
            for p in range(8):
                p_spot='{}{}'.format(self.alpha[p+1],p_r)
                Piece(bpawn_file,sqr_size,self.aboard[p_spot])
            bking_file='{}/{}{}.png'.format(self.pieces_set,c,'King')
            Piece(bking_file,sqr_size,self.aboard['E{}'.format(r)])
            bqueen_file='{}/{}{}.png'.format(self.pieces_set,c,'Queen')
            Piece(bqueen_file,sqr_size,self.aboard['D{}'.format(r)])

    def get_aboard(self,coords):
        inv_aboard={tuple(coord):sqr for sqr,coord in self.aboard.items() }
        return inv_aboard[tuple(coords)]

    def get_nboard(self,coords):
        inv_nboard={tuple(coord):sqr for sqr,coord in self.nboard.items() }
        return int(inv_nboard[tuple(coords)])

    def get_coords(self,square):
        if type(square)==str: return aboard(square)
        if type(square)==int: return nboard(square)

class Knight(Piece):
    def __init__(self,board,image_file,square_size,start_coords=(450,350) ):
        Piece.__init__(self,image_file,square_size,start_coords=(450,350) )#prevents overriding
        self.valid=True
        self.board=board  #should be instance of board class

    def k_validation(self,event): #validity of knight move after drop
        moves=np.array([+21,-21,-8,+8,-12,+12,-19,+19]) #valid places
        pos=(event.x,event.y)
        self.drop(moves,pos)


    def make_drag(self):
        self.mycanvas.tag_bind(self.Id,'<Button-1>',self.pickup)
        self.mycanvas.tag_bind(self.Id,'<B1-Motion>',self.move)
        self.mycanvas.tag_bind(self.Id,'<ButtonRelease-1>',self.k_validation)

class Bishop(Piece):


""" TO DO
-Create functions that print out various board types for all types of board input, coords
and n and alpha squares.

-Then do an actul validation for the knight
-By changing len(nearest_list) validation to include if spot is right???

"""


myboard=Board()
myboard.create_board()
knight=Knight(myboard,'merida/320/BlackKnight.png',100 )


top.mainloop()
