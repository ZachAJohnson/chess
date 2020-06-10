#! /usr/bin/python
import pieces as pcs

class Board():
    def __init__(self,board,sqr_size=100,pieces_set='merida'):
        self.pieces_set=pieces_set
        self.sqr_size=sqr_size
        self.board=board #The canvas!
        self.pieces_files={'merida':'merida/320/','standard':'wiki-SVG'}# dict for pieces files

    def create_board(self):
        x0, y0= (0,0)
        color=['blanched almond','salmon4'] #white, black
        color=['#edddb3','#b28665']

        self.alpha=('','A','B','C','D','E','F','G','H')
        self.aboard={}
        self.nboard={}

        for r in range(8):
            for c in range(8):
                rect_coords=[x0 + c*self.sqr_size, y0+r*self.sqr_size,x0+(c+1)*self.sqr_size,y0+(r+1)*self.sqr_size]
                self.board.create_rectangle(rect_coords,width=2,fill=color[(r+c)%2],outline='')
                coords=( (rect_coords[0]+rect_coords[2])/2, (rect_coords[1]+rect_coords[3])/2 )
                self.aboard['{}{}'.format(self.alpha[c+1],8-r)]=coords
                self.nboard['{}{}'.format(8-r,c+1) ]=coords

    def layout_pieces(self,game_class): #Probably make this take in a pgn file later!!
        game=game_class
        row=[1,8]
        side=['White','Black'] #0 is white, 1 is black
        p_row=[2,7]
        KN=[0,0]; QN=[0,0];
        KB =[0,0]; QB =[0,0];
        KR=[0,0]; QR=[0,0]
        king=[0,0]; queen=[0,0];
        self.piece_dict={} #Ties canvas Id to pointer to class instance

        for i in range(2):
            r=row[i]
            c=side[i]
            p_r=p_row[i]
            pc_file=self.pieces_files[self.pieces_set]

            knight_file='{}/{}{}.png'.format(pc_file,c ,'Knight')
            #Board class, canvas, color, image, size, coords
            QN[i]=pcs.Knight(self, self.board,game,i , knight_file, self.sqr_size, start_coords=self.get_coords('B{}'.format(r)) )
            self.piece_dict[QN[i].Id]= QN[i]
            KN[i]=pcs.Knight(self,self.board,game,i,knight_file,self.sqr_size,  start_coords=self.get_coords('G{}'.format(r)) )
            self.piece_dict[KN[i].Id]= KN[i]
            bishop_file='{}/{}{}.png'.format(pc_file,c,'Bishop')
            QB[i]=pcs.Bishop(self,self.board,game,i,bishop_file,self.sqr_size, start_coords=self.get_coords('C{}'.format(r)))
            self.piece_dict[QB[i].Id]= QB[i]
            KB[i]=pcs.Bishop(self,self.board,game,i,bishop_file,self.sqr_size, start_coords=self.get_coords('F{}'.format(r)))
            self.piece_dict[KB[i].Id]= KB[i]
            rook_file='{}/{}{}.png'.format(pc_file,c,'Rook')
            QR[i]=pcs.Rook(self,self.board,game,i,rook_file,self.sqr_size, start_coords=self.get_coords('A{}'.format(r)))
            self.piece_dict[QR[i].Id]= QR[i]
            KR[i]=pcs.Rook(self,self.board,game,i,rook_file,self.sqr_size, start_coords=self.get_coords('H{}'.format(r)))
            self.piece_dict[KR[i].Id]= KR[i]
            king_file='{}/{}{}.png'.format(pc_file,c,'King')
            king[i]=pcs.King(self,self.board,game,i,king_file,self.sqr_size, start_coords=self.get_coords('E{}'.format(r)))
            self.piece_dict[king[i].Id]= king[i]
            queen_file='{}/{}{}.png'.format(pc_file,c,'Queen')
            queen[i]=pcs.Queen(self,self.board,game,i,queen_file,self.sqr_size, start_coords=self.get_coords('D{}'.format(r)))
            self.piece_dict[queen[i].Id]= queen[i]

            pawn_file='{}/{}{}.png'.format(pc_file,c,'Pawn')
            for p in range(8): #CHANGE TO PAWN!!!
                p_spot='{}{}'.format(self.alpha[p+1],p_r)
                pawn=pcs.Pawn(self,self.board,game,i,pawn_file,self.sqr_size,start_coords=self.get_coords(p_spot))
                self.piece_dict[pawn.Id]=pawn

    def get_square_from_rect(self,Id):
        nearest_coords=self.board.coords(Id)
        new_x=(nearest_coords[0]+nearest_coords[2])/2
        new_y=(nearest_coords[1]+nearest_coords[3])/2
        new_coords=(new_x,new_y)
        return self.get_nboard(new_coords)

    def objects_at_loc(self,loc): #either coords or square
        if type(loc)==str or type(loc)==int:
            loc=self.get_coords(loc)
            return list(self.board.find_overlapping(loc[0]-1,loc[1]-1,loc[0]+1,loc[1]+1))

        elif len(loc)==2:
            return list(self.board.find_overlapping(loc[0]-1,loc[1]-1,loc[0]+1,loc[1]+1))

    def get_piece(self,id): #gives class instantiation
        return self.piece_dict[id]

    def get_coords(self,coords): #Completely usless now?!
        inv_aboard={tuple(coord):sqr for sqr,coord in self.aboard.items() }
        return inv_aboard[tuple(coords)]

    def get_nboard(self,coords): #gives n square from coords-- no get_aboard???
        inv_nboard={tuple(coord):sqr for sqr,coord in self.nboard.items() }
        return int(inv_nboard[tuple(coords)])

    def get_coords(self,square):
        if type(square)==str: return self.aboard[square]
        if type(square)==int: return self.nboard[str(square)]
