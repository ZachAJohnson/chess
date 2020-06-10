#! /usr/bin/python
from PIL import Image
from PIL import ImageTk
from PIL import ImageFilter
import tkinter as tk
import numpy as np


class Piece():
    def __init__(self,board,board_canvas, game, color,image_file,square_size=100,start_coords=(450,350) ):
        #define class variables
        self.board=board
        self.board_canvas=board_canvas
        self.sq_w =square_size
        self.sq_h =square_size
        self.image_file=image_file
        self.start_x=start_coords[0]
        self.start_y=start_coords[1]
        self.color=color #White or Black
        self.game=game #the class of the game played

        ##Now functions to create draggable pieces
        self.import_image()
        self.make_drag()

    def import_image(self):
        self.im=Image.open(self.image_file)
        im_w, im_h =self.im.size
        scale=self.sq_h/im_h
        self.im=self.im.resize(  (int(im_w*scale),int(im_h*scale)),resample=Image.BICUBIC )#scales based on height only
        self.ph= ImageTk.PhotoImage(self.im)
        self.Id= self.board_canvas.create_image(self.start_x,self.start_y,image=self.ph)
        self.board_canvas.image=self.ph

    def make_drag(self):
        self.board_canvas.tag_bind(self.Id,'<Button-1>',self.pickup_validity)
        self.board_canvas.tag_bind(self.Id,'<B1-Motion>',self.move_validity)
        self.board_canvas.tag_bind(self.Id,'<ButtonRelease-1>',self.drop_validity) # defined in each child class

    def is_turn(self):
        return self.game.turn==self.color

    def pickup_validity(self,event):
        if self.is_turn(): self.pickup(event)

    def move_validity(self,event):
        if self.is_turn(): self.move(event)

    def drop_validity(self,event):
        if self.is_turn(): self.drop_validation(event)

    def pickup(self,event):
        self.init_coords=self.board_canvas.coords(self.Id)

    def move(self,event):
        #print(event.x,event.y)
        x,y = (event.x,event.y)
        self.board_canvas.coords(self.Id,x,y)

    def drop_success(self,new_coords,other_piece=0):
        self.board_canvas.coords(self.Id,new_coords)
        if other_piece!=0:
            self.board_canvas.delete(other_piece)
        self.game.add_turn()

    def drop_fail(self):
        self.board_canvas.coords(self.Id,self.init_coords)

    def path_open(self,path):
        occupied_squares=0
        for square in path:
            square=int(square)
            try:
                objects= self.board.objects_at_loc(square)
                if len(objects)==1:
                    'do nothing'
                else:
                    occupied_squares+=1
            except KeyError as key:
                print("Cannot find key on path to drop location, key: ", key)
                print("And the dictionary is", self.board.nboard)

        if occupied_squares>=1:
            return False
        elif occupied_squares==0:
            return True

    def remove_and_drop(self,new_coords, other_piece):
        rmv_piece = self.board.get_piece(other_piece)
        drop_piece= self.board.get_piece(self.Id)
        c_rmv = rmv_piece.color
        c_drop = drop_piece.color
        if (c_drop-c_rmv)%2==1 :
            self.drop_success(new_coords,other_piece)
        else: self.drop_fail()

    def available_path(self, drop_square, init_square):
        diff= drop_square-init_square
        diags=[11,9]

        for n in diags:
            if diff%n==0:
                path=np.arange(1,abs(int(diff/n)) )*np.sign(diff)*n+init_square
                return self.path_open(path)

        if diff%10==0:
            path=np.arange(1, abs(int(diff/10)) )*np.sign(diff)*10+init_square
            return self.path_open(path)
        elif 1<=abs(diff)<=8:
            path=np.arange(1,abs(int(diff)))*np.sign(diff)+init_square
            return self.path_open(path)

    #drop for all pieces
    def drop(self,moveset,pos): #pos=position
        init_square=self.board.get_nboard(  tuple(self.init_coords) )
        moves=moveset+init_square

        #create small square to determine number of items at drop coords
        nearest_list=self.board.objects_at_loc(pos)
        nearest_list.remove(self.Id)

        try:
            new_n=self.board.get_square_from_rect(nearest_list[0]) #gets number of this square from specific rectangle ID
            new_coords=self.board.get_coords(new_n)
        except KeyError:
            self.board.coords(self.Id,self.init_coords)

        if new_n in moves and self.available_path(new_n, init_square):
            if len(nearest_list)==1:
                self.drop_success(new_coords)
            if len(nearest_list)==2:
                self.remove_and_drop(new_coords, nearest_list[1])
        else:
            self.drop_fail()

        #else: self.board_canvas.coords(self.Id,self.init_coords)

class Knight(Piece):
    def __init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=(450,350) ):
        Piece.__init__(self,board,board_canvas, game, color,image_file,square_size=square_size,start_coords=start_coords )#prevents overriding
        self.start_coords=start_coords
        self.name ='{} knight'.format(['White','Black'][color])

    def available_path(self, foo, bar):
        return True

    def drop_validation(self,event): #validity of knight move after drop
        moves=np.array([+21,-21,-8,+8,-12,+12,-19,+19]) #valid places
        pos=(event.x,event.y)
        self.drop(moves,pos)

class Bishop(Piece):
    def __init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=(450,350) ):
        Piece.__init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=start_coords )#prevents overriding
        self.start_coords=start_coords
        self.name='bishop'


    def drop_validation(self,event): #validity of bishop move after drop
        init_square=self.board.get_nboard(  tuple(self.init_coords) )
        tr=11*np.arange(1,9) #top-right diag
        tl=9*np.arange(1,9) #top-left diag
        moves=np.concatenate((tl,-tl,tr,-tr))+init_square
        valid_squares=np.array([[i*10+j for i in range(0,9)] for j in range(1,9)]).flatten()
        moves=np.array( [x for x in moves if x in valid_squares] )
        #notusfficient..
        print('possible destinations are  ',moves)
        pos=(event.x,event.y)
        self.drop(moves-init_square,pos)

class Rook(Piece):
    def __init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=(450,350) ):
        Piece.__init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=start_coords )#prevents overriding
        self.start_coords=start_coords
        self.name='rook'

    def drop_validation(self,event): #validity of Rook move after drop
        init_nboard=self.board.get_nboard(self.init_coords)
        init_c =int( str(init_nboard)[1] )
        init_r =int( str(init_nboard)[0] )
        row_moves=10*init_r+np.arange(1,9)-init_nboard
        col_moves=10*np.arange(1,9) + init_c -init_nboard
        moves=np.concatenate((row_moves,col_moves))
        moves= np.array([x for x in moves if x!=0])
        pos=(event.x,event.y)
        self.drop(moves,pos)

class Queen(Piece):
    def __init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=(450,350) ):
        Piece.__init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=start_coords )#prevents overriding
        self.start_coords=start_coords
        self.name='queen'

    def drop_validation(self,event): #validity of queen move after drop
        init_nboard=self.board.get_nboard(self.init_coords)
        init_c =int( str(init_nboard)[1] )
        init_r =int( str(init_nboard)[0] )
        row_moves=10*init_r+np.arange(1,9)-init_nboard
        col_moves=10*np.arange(1,9) + init_c -init_nboard
        tr=11*np.arange(1,9) #top-right diag
        tl=9*np.arange(1,9) #top-left diag
        moves=np.concatenate((row_moves,col_moves,tl,-tl,tr,-tr))
        moves= np.array([x for x in moves if x!=0])
        pos=(event.x,event.y)
        self.drop(moves,pos)

class King(Piece):
    def __init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=(450,350) ):
        Piece.__init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=start_coords )#prevents overriding
        self.start_coords=start_coords
        self.name='king'

    def drop_validation(self,event): #validity of king move after drop
        moves=np.array((1,-1,10,-10,11,-11,9,-9))
        pos=(event.x,event.y)

        init_square=self.board.get_nboard(  tuple(self.init_coords) )
        nearest_list=self.board.objects_at_loc(pos)
        nearest_list.remove(self.Id)
        drop_square=self.board.get_square_from_rect(nearest_list[0])

        if self.color==0:
            castle_squares=[17,13]
            adder=0
        else:
            castle_squares=[87,83]
            adder=70
        if drop_square in castle_squares:# and rook is there...
            'find rook and move it and the king'
            if self.available_path(drop_square, init_square):
                #need to add blacks conditions now!
                #Perhaps make this a separate funciton in this class
                if drop_square==17+adder:
                    kr_square=self.board.objects_at_loc(18+adder)
                    new_rook_square=16+adder
                elif drop_square==13+adder:
                    kr_square=self.board.objects_at_loc(11+adder)
                    new_rook_square=14+adder
                try:
                    piece=self.board.get_piece(kr_square[1])
                    if piece.__class__.__name__=='Rook':
                        rook=kr_square[1]
                        self.drop_success(self.board.get_coords(drop_square))
                        new_rook_coords=self.board.get_coords(new_rook_square)
                        self.board_canvas.coords(rook,new_rook_coords)
                    else: self.drop_fail()
                except KeyError as key:
                    print("Cannot recognize piece with key ",key )
                    self.drop_fail()
                except IndexError:
                    print("Cannot find any piece here")
                    self.drop_fail()

        else:
            self.drop(moves,pos)

class Pawn(Piece):
        def __init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=(450,350) ):
            Piece.__init__(self,board,board_canvas, game, color,image_file,square_size,start_coords=start_coords )#prevents overriding
            self.start_coords=start_coords
            self.name='pawn'

        def drop_validation(self,event):
            init_square=self.board.get_nboard(  tuple(self.init_coords) )
            #create small square to determine number of items at drop coords
            pos=(event.x,event.y)
            nearest_list=self.board.objects_at_loc(pos)
            nearest_list.remove(self.Id)
            try:
                new_n=self.board.get_square_from_rect(nearest_list[0]) #gets number of this square from specific rectangle ID
                new_coords=self.board.get_coords(new_n)

            except KeyError as error:
                print("Not recognized- error is: ",error)
                self.board_canvas.coords(self.Id,self.init_coords)

            drop_piece= self.board.get_piece(self.Id)
            c_drop = drop_piece.color
            sgn = -c_drop*2+1 #sign for black vs white movement

            if len(nearest_list)==2:
                w_take=np.array(( sgn*9,sgn*11))
                moves=init_square+w_take
                new_n=self.board.get_nboard(new_coords)

                self.remove_and_drop(new_coords, nearest_list[1])

            elif len(nearest_list)==1:
                "CHECK en-pessant!!"
                if 2*int(init_square/10)+sgn*5==9: #on initial column
                     w_moves=np.array((sgn*10,sgn*20))
                else: w_moves=np.array((sgn*10))
                moves=np.array(w_moves+init_square)
                if new_n in moves:
                    self.drop_success(new_coords)
                else: self.drop_fail()
            else:
                 self.drop_fail()
