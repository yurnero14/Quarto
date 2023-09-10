import extendedQuarto
import random
from quarto import Player 


class DumbAgent(Player):
  '''
  Agent that purposefully makes bad decisions
  '''
  def __init__(self, quarto: extendedQuarto.ExtendedQuarto) -> None:
        super().__init__(quarto)
        

  def choose_piece(self) -> int:
    '''
    If possible, chooses a piece that the opponent can win with,
    otherwise chooses a random one
    '''
    board = self.get_game() 
    
    unchosen_pieces = board.get_unchosen_pieces() #gets pieces that are left to choose

    
    if (len(unchosen_pieces) > 0): 

      for piece in unchosen_pieces:
        win = board.check_if_possible_to_win(piece) #checks if it's possible to win with said piece

        if (win == True):
          return piece
    
        else: #chosenPieces
          p = random.randint(0, len(unchosen_pieces) -1) # between 0 and 15 
          return unchosen_pieces[p]

    else:
      return -1 # In case the board is full
    

  def place_piece(self) -> tuple[int, int]:
    '''
    Place the piece in a random place
    '''
    return random.randint(0, 3), random.randint(0, 3)


  