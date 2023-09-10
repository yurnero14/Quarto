import quarto
from copy import deepcopy
import numpy as np
import testQuarto

class ExtendedQuarto(quarto.Quarto):
    '''
    Extended version of Quarto for more function implementation
    '''
    def __init__(self):
        super().__init__()

    def set_current_player(self, player: int):
        '''
        Function to set current player in the board
        '''
        self._current_player = player
    

    def get_unchosen_pieces(self) -> list:
        '''
        Get a list of all unchosen pieces
        '''
        unchosen_pieces = list(range(16))
        
        for y, row in enumerate(self._board):
            for x, index_at_place in enumerate(row):
                if index_at_place == -1: #empty place
                    continue
                else:
                    unchosen_pieces.remove(index_at_place) #piece already played

        return unchosen_pieces
        
    def check_if_possible_to_win(self, piece_idx: int) -> bool:
        '''
        Given a piece, checks if it's possible to win with that piece
        ''' 
        for y, row in enumerate(self._board):
            for x, index_at_place in enumerate(row):
                if index_at_place == -1:  

                    new_arr_board = deepcopy(self._board)
                    new_board = testQuarto.TestQuarto(new_arr_board) #creates a test quarto to apply the possible move
                    
                    new_board.select(piece_idx) # select the piece we want to place
                    new_board.place(x,y) # place the piece 

                    if (new_board.check_finished() or new_board.check_winner() != -1): #if the game is over and it's not a tie
                        return True
                
        return False

