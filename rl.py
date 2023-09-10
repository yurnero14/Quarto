import logging
import random
from quarto import Player
import extendedQuarto
import numpy as np
import pickle
from testQuarto import TestQuarto


class QTableKey(object):
    '''
    Class to use as Key for the q-table
    '''
    def __init__(self, board, selected_piece):
        self.board = board
        self.selected_piece = selected_piece

    def __hash__(self):
        '''
        Hash defined to be possible using it as a key in a dictionary
        '''
        return hash((hash(self.board.tostring()), self.selected_piece))

    def __eq__(self, other): 
        '''
        Eq defined to be possible using it as a key in a dictionary
        '''
        return ((self.board & other.board).any()) and (self.selected_piece == other.selected_piece)

    def get_board_str(self):
        '''
        Gets board as string
        '''
        board_string = "["
        for y, row in enumerate(self.board):
            board_string += "["
            for x, index_at_place in enumerate(row):
                board_string += str(index_at_place)
                board_string += " "
            board_string += "]"
        board_string += "]"
        return board_string

    def get_selected_piece_str(self):
        '''
        Gets selected piece as string
        '''
        return str(self.selected_piece)

class RLPlayer(Player):
    '''
    Reinforcement Learning Agent
    '''
    REWARD = 1 #Reward value for winning the game
    PENALTY = -1 #Penalty value for losing the game
    DRAW_REWARD = 0.5 #Reward value for drawing the game
    previous_state = None
    previous_move = None


    def __init__(self, quarto: extendedQuarto.ExtendedQuarto, learning_rate: float, discount_rate: float, exploration_rate: float) -> None:
        super().__init__(quarto)
        q = {}  # {(QTableKey(board, selected piece), move) -> value}
        self.q = q
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        self.place_chosen = None # x,y
        self.chosen_piece = None # id
       

    def choose_piece(self) -> int:
        '''
        Function that returns the chosen piece
        ''' 
        if (self.chosen_piece == None): # q-learner is starting
            self.chosen_piece = random.randint(0, 15)
           
        return self.chosen_piece

    def place_piece(self) -> tuple[int, int]: 
        '''
        Function that returns the place to put the piece
        '''       
        x,y = self.place_chosen[0], self.place_chosen[1]
        return x,y

    def clear_previous_vars(self) -> None:
        '''
        Clears the variables to start a different game
        '''
        self.previous_state = None
        self.previous_move = None
        self.place_chosen = None # x,y
        self.chosen_piece = None # id

    def get_q_length(self) -> int:
        '''
        Gets size of the q-table
        '''
        return len(self.q)
    

    def generate_possible_moves(self) -> list:
        """
        Return a list of possible moves, [(x,y,id),(x,y,id),...,(x,y,id)]
        """
      
        current_state = self.get_game()
        board = current_state.get_board_status()
        selected_piece = current_state.get_selected_piece()
        
        empty_places = [] # list of empty places which are (x, y)
        not_selected_pieces = list(range(16)) #generates a list with values 0 to 15

        if (selected_piece != -1): # why are we doing this. 
            not_selected_pieces.remove(selected_piece) 
            
        for y, row in enumerate(board):
            for x, index_at_place in enumerate(row): # for all places in row, index_on_place = -1 if no piece on place
                                                     #otherwise the index of the piece
                if (index_at_place == -1):
                    empty_places.append((x,y)) #adds the empty place to the list

                else: # if there is a piece at the place, remove it from not_selected_pieces
                   not_selected_pieces.remove(index_at_place) 

        possible_moves = []

        # add all possible moves
        for empty_place in empty_places:
            if len(not_selected_pieces) > 0:
                for piece in not_selected_pieces:
                    possible_moves.append((empty_place[0], empty_place[1], piece))
            else:
                possible_moves.append((empty_place[0], empty_place[1], -1)) #when there is only one piece left
        
        return possible_moves
        

    def add_new_state_move(self) -> None:
        '''
        Adds new state, move combinations to the q-learner table
        '''
        possible_moves = self.generate_possible_moves() 
        current_state = self.get_game() # type -> ExtendedQuarto
        board = current_state.get_board_status() # the list with the board
        selected_piece = current_state.get_selected_piece()
        
        
        for move in possible_moves: # adds the combination state, move to the q
            
            current_key = QTableKey(board, selected_piece) #creates key

            if (current_key, move) not in self.q:
                self.q[(current_key, move)] = np.random.uniform(
                    0.0, 0.01)  # attribute a small random value


    def policy(self) -> tuple:
        '''
        Gets the move to apply
        '''
        possible_moves = self.generate_possible_moves()
        current_state = self.get_game() # type -> ExtendedQuarto
        board = current_state.get_board_status() # the list with the board
        selected_piece = current_state.get_selected_piece()
        
        if np.random.random() > self.exploration_rate: # Exploitation

            q_val_list = [self.q[(QTableKey(board, selected_piece), move)]
                          for move in possible_moves] # list of the values of state and action
                          
            max_val_index = np.argmax(q_val_list)   # returns the index of the max element of the array

            return possible_moves[max_val_index] # returns the move with the biggest q_value

        else:  # Exploration - returns a random possible move
            return random.sample(possible_moves, 1)[0]  


    def set_move(self, move) -> None:
        '''
        Sets the move for chosen and place piece
        '''
        if(move != None): 
            self.chosen_piece = move[2]
            self.place_chosen = move[0], move[1]

    def update_when_draw(self) -> None:
        '''
        Updates the q-table when the game draws
        '''
        q_value = self.q[(self.previous_state, self.previous_move)]
        #self.q[(self.previous_state, self.previous_move)] += \
                    #self.learning_rate * (self.DRAW_REWARD -
                                          #self.q[(self.previous_state, self.previous_move)])
        self.q[(self.previous_state, self.previous_move)] += \
                    self.learning_rate * (self.DRAW_REWARD + (self.discount_rate * q_value) -
                                        self.q[(self.previous_state, self.previous_move)])
        
        self.clear_previous_vars()

    def update_when_lost(self)->None:
        '''
        Updates the q-table when the agent loses
        '''
        self.q[(self.previous_state, self.previous_move)] += \
            self.learning_rate * \
            (self.PENALTY -
            self.q[(self.previous_state, self.previous_move)])

        self.clear_previous_vars()


    def update_q(self) -> tuple:
        """
        Updated the q-table and returns the chosen piece and the coordinates for the piece that
        should be placed in a tuple (chosen_piece: int, x: int, y: int)
        """
        current_move = None
        current_state = self.get_game()
        board = current_state.get_board_status() # the list with the board
        selected_piece = current_state.get_selected_piece() # gets the selected piece of the board


        self.add_new_state_move()  # adds the new state, moves
           
        current_move = self.policy()  # gets the move that we want to use

        if self.previous_move is not None:  # if it is not the first move
              
            game = self.get_game()
            b = game.get_board_status()
            next_state = TestQuarto(b)
            

            next_state.select(game.get_selected_piece()) # set the selected piece in the copied board to the same one in the original one
                
            next_state.place(current_move[0], current_move[1]) #apply move
             
            reward = 0
            
            # check winner or draw -> change reward. 
            if (next_state.check_finished() and (next_state.check_winner() == -1)): # check if draw
                reward = self.DRAW_REWARD


            if (next_state.check_winner() >= 0): # check if winner
                reward = self.REWARD
    
            
            possible_moves = self.generate_possible_moves()
                
            max_q = max([self.q[(QTableKey(board, selected_piece), move)]
                        for move in possible_moves]) # max qvalue from the possible moves of the current_state

            self.q[(self.previous_state, self.previous_move)] += \
                    self.learning_rate * (reward + (self.discount_rate * max_q) -
                                        self.q[(self.previous_state, self.previous_move)])
                            

        self.set_move(current_move)
            
        self.previous_state, self.previous_move = QTableKey(board, selected_piece), current_move

        return current_move

    def save_q_table(self):
        '''
        Save q-table in a file
        '''
        with open('q_table_3.pickle', 'wb') as handle:
            pickle.dump(self.q, handle, protocol=pickle.HIGHEST_PROTOCOL)
        

        f = open("doc_path.txt", "w")
        state = 0
        move = 1
        for key, value in self.q.items():
            elem = ""
            elem += key[state].get_board_str() + ";"
            elem += key[state].get_selected_piece_str() + ";"
            for i in range(3):
                elem += str(key[move][i]) + ";"
            elem += str(value) + "\n"
            f.write(elem)
        f.close()




