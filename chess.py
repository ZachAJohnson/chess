#! /usr/bin/python

import tkinter as tk
from PIL import Image
from PIL import ImageTk

top = tk.Tk()
top.title("Chess Board!!")

#Create frame for board and pieces on board
board_frame= tk.Frame(top,width=500,height=500)
board_frame.pack(side='right')

board_canvas= tk.Canvas(board_frame,width=500,height=500)
board_canvas.grid(row=0,column=0)

#board_canvas.config(bg=' ')
#board_canvas.pack(fill='both', expand=1)

pieces_canvas=tk.Canvas(board_frame,width=500,height=500)
pieces_canvas.grid(row=0,column=0)
#pieces_canvas.pack(fill='both', expand=1)

#Create frame on the left
left_frame=tk.Frame(top,width=100)
left_frame.pack(side='left',fill='both',expand=1)

#perhaps add clause here --if near some object, THEN bind to clicker    
mycanvas = tk.Canvas(left_frame,bg='white')
mycanvas.pack(fill='both',expand=1)

class Piece():
    def __init__(self,image_file,square_size):
        #define class variables
        self.sq_w =square_size[0]
        self.sq_h =square_size[1]
        self.image_file=image_file
        self.mycanvas=pieces_canvas

        ##Now functions to create draggable pieces
        self.import_image()
        self.make_drag()
        
    def import_image(self,x=100,y=100):
        self.im=Image.open(self.image_file)
        im_w, im_h =self.im.size
        scale=self.sq_h/im_h
        self.im=self.im.resize(  (int(im_w*scale),int(im_h*scale)) )#scales based on height only
        self.ph= ImageTk.PhotoImage(self.im)
        self.Id= self.mycanvas.create_image(x,y,image=self.ph)
        self.mycanvas.image=self.ph
        
    def make_drag(self):
        self.mycanvas.tag_bind(self.Id,'<Button-1>',self.pickup)
        self.mycanvas.tag_bind(self.Id,'<B1-Motion>',self.move)
        self.mycanvas.tag_bind(self.Id,'<ButtonRelease-1>',self.drop)

    def pickup(self,event):
        print(event.x,event.y)
        
    def move(self,event):
        #print(event.x,event.y)
        x,y = (event.x,event.y)
        self.mycanvas.coords(self.Id,x,y)
        
    def drop(self,event):
        'print(event.x,event.y)'

square_size=[100,100]
color=['salmon4','white']
alpha=('','A','B','C','D','E','F','G','H')
for r in range(8+1):
    for c in range(8+1):
        if   c==0 and r!=8: w = tk.Label(board_canvas,text="{}".format(8-r))
        elif r==8: w = tk.Label(board_canvas,text="{}".format(alpha[c]))
        else: w = tk.Canvas(board_canvas, bg=color[(r+c)%2], relief='sunken',width=square_size[0],height=square_size[1])       
        top.lower(w)        
        w.grid(row=r, column=c)


        

        
b_knight=Piece('merida/320/Black{}.png'.format('Knight'),square_size)


'''
b_bishop=Piece('merida/320/Black{}.png'.format('Bishop'),square_size)
b_pawn=Piece('merida/320/Black{}.png'.format('Pawn'),square_size)
b_king=Piece('merida/320/Black{}.png'.format('King'),square_size)
b_queen=Piece('merida/320/Black{}.png'.format('Queen'),square_size)
b_Rook=Piece('merida/320/Black{}.png'.format('Rook'),square_size)
'''

#top.lift(pieces_canvas)
top.lift(board_canvas)


top.mainloop()
