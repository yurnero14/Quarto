from rl import QTableKey
from quarto import Quarto
from quarto import Player
import numpy as np
import pickle
import random

class TrainedRL(Player):
  '''
  Class with the trained RL
  '''
  def __init__(self, quarto: Quarto) -> None:
    super().__init__(quarto)
    self.q = {}
    self.place_chosen = None
    self.chosen_piece = None

    self.build_q()  # when this agent is inited -> q-table is created

    
  def choose_piece(self) -> int:
      if (self.chosen_piece == None): # we are starting
        return random.randint(0, 15)
      else:
        return self.chosen_piece
        

  def place_piece(self) -> tuple[int, int]:
      possible_moves = self.generate_possible_moves() 
      current_state = self.get_game() # type -> Extended Quarto
      board = current_state.get_board_status() # the list with the board
      selected_piece = current_state.get_selected_piece()

      state = QTableKey(board, selected_piece)  # list of the values of state and action
     
      for move in possible_moves:  # list of the values of state and action
            
            current_key = QTableKey(board, selected_piece) # adds the combination state, move to the q
          
            if (current_key, move) not in self.q:
              self.q[(current_key, move)] = np.random.uniform(
                    0.0, 0.01)  # attribute a small random value

              
      q_val_list = [self.q[(state, move)]
            for move in possible_moves]
      
      max_val_index = np.argmax(q_val_list) # returns the index of the max element of the array
      
      move = possible_moves[max_val_index] # returns the move with the biggest q_value
      
      x = move[0]
      y = move[1]

      self.place_chosen = x, y
      self.chosen_piece = move[2]

      return x, y

  def build_q(self):
      '''
      Builds q-table from document
      '''
      file_to_read = open("q_table_3.pickle", "rb")

      self.q = pickle.load(file_to_read)


      f = open("doc_path.txt", "r")
      for row in f:
        elems = row.split(";")
        board_str = elems[0]
        BOARD_SIDE = 4
        
        board_str = board_str.replace("[", "")
        board_str = board_str.replace("]", "")
        numbers = board_str.split(" ")


        board = np.ones(
            shape=(BOARD_SIDE, BOARD_SIDE), dtype=int)

        i = 0
        for y in range(4):
            for x in range(4):
                board[y,x] = int(numbers[i])
                i += 1
        
         
        given_piece = int(elems[1])
        x = int(elems[2])
        y = int(elems[3])
        selected_piece = int(elems[4])
        q_value = float(elems[5])
        key = QTableKey(board, given_piece)
        move = (x,y,selected_piece)
        self.q[(key,move)] = q_value
      f.close()


   

    
  def generate_possible_moves(self) -> list:
      """
      Return a list of possible moves, [(x,y,id),(x,y,id),...,(x,y,id)]
      """
      current_state = self.get_game() # type -> ExtendedQuarto
      board = current_state.get_board_status() # the list with the board
      selected_piece = current_state.get_selected_piece()
   
      empty_places = []  # list of empty places which are (x, y)
      not_selected_pieces = list(range(16)) #generates a list fom 0 to 15
      if (selected_piece != -1): 
          not_selected_pieces.remove(selected_piece) 

      for y, row in enumerate(board):
          for x, index_at_place in enumerate(row): # for all places in row, index_on_place = -1 if no piece on place 
                                                   #otherwise the index of the piece
              if (index_at_place == -1):
                  empty_places.append((x,y))
              else: # if there is a piece at the place, remove it from not_selected_pieces
                  not_selected_pieces.remove(index_at_place)

      possible_moves = []

      for empty_place in empty_places: # add all possible moves
          if len(not_selected_pieces) > 0:
              for piece in not_selected_pieces:
                  possible_moves.append((empty_place[0], empty_place[1], piece))
          else:
              possible_moves.append((empty_place[0], empty_place[1], -1)) #when there is only one piece left
      
      return possible_moves
      
  
