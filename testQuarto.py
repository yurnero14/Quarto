import quarto
import numpy as np


class TestQuarto(quarto.Quarto):
    '''
    Extended version of Quarto for move testing
    '''
    def __init__(self, board: np):
        super(TestQuarto, self).__init__()    
        self._board = board
        
    def get_test_board_status(self):
        '''
        gets the board
        '''
        return self._board
