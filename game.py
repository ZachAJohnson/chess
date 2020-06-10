#! /usr/bin/python

class Player_Game():

    def __init__(self, player1, player2,board_class):
            self.myboard=board_class
            self.player1=player1
            self.player2=player2
            self.turn=0 #White=0

    def new_game(self):
        self.myboard.layout_pieces(self)
        color=['White','Black']
        over=False
        #while over==False:
        #    print("It is {}'s turn!".format(color[self.turn]))

    def add_turn(self):
        self.turn=(self.turn+1)%2
        #self.turn=0
