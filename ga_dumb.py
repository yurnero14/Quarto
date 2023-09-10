import random
import quarto

class UntrainedGAAgent(quarto.Player):
    '''Evolved agent using the GA approach'''

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)
        self.board = quarto
        self.active_pieces = [i for i in range(16)]

        # Generate the probability of picking each rule for picking and placing
        pick_prob_not_normalized = [random.random() for i in range(3)]
        pick_prob = [x/sum(pick_prob_not_normalized) for x in pick_prob_not_normalized]
        self.pick_probability_1 = pick_prob[0]
        self.pick_probability_2 = pick_prob[1]
        self.pick_probability_3 = pick_prob[2]

        place_probability_not_normalized = [random.random() for i in range(6)]
        place_prob = [x/sum(place_probability_not_normalized) for x in place_probability_not_normalized]
        self.place_probability_1 = place_prob[0]
        self.place_probability_2 = place_prob[1]
        self.place_probability_3 = place_prob[2]
        self.place_probability_4 = place_prob[3]
        self.place_probability_5 = place_prob[4]
        self.place_probability_6 = place_prob[5]

        # Create a dictionary containing the attributes of each piece
        self.piece_dict = self.piece_attribute_dict()

        # Create a dictionary containing the dominating lines of each length
        self.dom_line_dict = {}

    def get_pick_prob(self):
        return (self.pick_probability_1, self.pick_probability_2, self.pick_probability_3)

    def get_place_prob(self):
        return (self.place_probability_1, self.place_probability_2, self.place_probability_3, \
            self.place_probability_4, self.place_probability_5, self.place_probability_6)

    def set_pick_prob_1(self, val):
        self.pick_probability_1 = val

    def set_pick_prob_2(self, val):
        self.pick_probability_2 = val

    def set_pick_prob_3(self, val):
        self.pick_probability_3 = val

    def set_place_prob_1(self, val):
        self.place_probability_1 = val
    
    def set_place_prob_2(self, val):
        self.place_probability_2 = val

    def set_place_prob_3(self, val):
        self.place_probability_3 = val

    def set_place_prob_4(self, val):
        self.place_probability_4 = val

    def set_place_prob_5(self, val):
        self.place_probability_5 = val

    def set_place_prob_6(self, val):
        self.place_probability_6 = val

    def choose_piece(self) -> int:
        '''Decides what rule to be played when picking a piece by the agent'''

        self.dominating_line()

        '''# If there are 3 pieces on the same line with at least 1 common attribute and a 4th free slot
        if len(self.dom_line_dict['3']) > 0:
            return self.desired_piece(self.dom_line_dict['3'])'''

        # Genereate the random value to decide what simple rule to play
        val = random.random()

        # Play rule 1 
        if val <= self.pick_probability_1:
            #print("Rule 1")
            return self.pick_rule_1()
        # Play rule 2
        elif val <= self.pick_probability_1 + self.pick_probability_2:
            #print("Rule 2")
            return self.pick_rule_2()
        # Play rule 3
        else:
            #print("Rule 3")
            return self.pick_rule_3()

    def place_piece(self) -> tuple([int, int]):
        '''Decides where to place the piece given by the opponent'''

        self.dominating_line()

        '''# If there are 3 pieces on the same line with at least 1 common attribute and a 4th free slot
        # and the selected piece shares one of the common attributes
        if len(self.dom_line_dict['3']) > 0:
            for line in self.dom_line_dict['3']:
                for j,k in zip(line[2], list(self.piece_dict[str(self.board.get_selected_piece())])):
                    if j != None and j == k:
                        return self.place_piece_specified_line(line)'''

        # Genereate the random value to decide what simple rule to play
        val = random.random()

        # Play rule 1 
        if val <= self.place_probability_1:
            #print("Rule 1")
            return self.place_rule_1()
        # Play rule 2
        elif val <= self.place_probability_1 + self.place_probability_2:
            #print("Rule 2")
            return self.place_rule_2()
        # Play rule 3
        elif val <= self.place_probability_1 + self.place_probability_2 + self.place_probability_3:
            #print("Rule 3")
            return self.place_rule_3()
        # Play rule 4
        elif val <= self.place_probability_1 + self.place_probability_2 + self.place_probability_3 + self.place_probability_4:
            #print("Rule 4")
            return self.place_rule_4()
        # Play rule 5
        elif val <= self.place_probability_1 + self.place_probability_2 + self.place_probability_3 + self.place_probability_4 + self.place_probability_5: 
            #print("Rule 5")
            return self.place_rule_5()
        # Play rule 6
        else:
            #print("Rule 6")
            return self.place_rule_6()

    def piece_attribute_dict(self) -> dict:
        piece_dict = {}

        for i in range(16):
            piece = self.board.get_piece_charachteristics(i)
            piece_dict[str(i)] = (piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE)
        return piece_dict

    def dominating_line(self):
        '''Store each row/column/diagonal with at least one shared attribute in the dom_line_dict based on how long they are.
        Each row, column and diagonal have been assigned a number, where the rows from top to bottom are
        0 - 3, columns from left to right are 4-7, diagonal 8 and off-diagonal 9.'''
        board = self.board.get_board_status()

        self.dom_line_dict['1'] = []
        self.dom_line_dict['2'] = []
        self.dom_line_dict['3'] = []
        self.dom_line_dict['4'] = []

        # Check horizontal 
        line_counter = 0
        for row in board:
            dominating_result = self.dominating(row, line_counter)
            if dominating_result != None:
                self.dom_line_dict[str(dominating_result[0])].append(dominating_result)
            line_counter += 1

        # Check vertical 
        for i in range(self.board.BOARD_SIDE):
            dominating_result = self.dominating(board[:,i], line_counter)
            if dominating_result != None:
                self.dom_line_dict[str(dominating_result[0])].append(dominating_result)
            line_counter += 1

        # Check diagonal
        diag = []
        off_diag = []
        for i in range(len(board)):
            diag.append(board[i,i])
            off_diag.append(board[self.board.BOARD_SIDE-1-i, i])

        dominating_result = self.dominating(diag, line_counter)
        if dominating_result != None:
            self.dom_line_dict[str(dominating_result[0])].append(dominating_result)
        dominating_result = self.dominating(off_diag, line_counter+1)
        if dominating_result != None:
            self.dom_line_dict[str(dominating_result[0])].append(dominating_result)
        return dominating_result

    def dominating(self, line, line_counter: int) -> list:
        '''Calculate if the current line has a longer line of pieces with at least one shared attribute
        (higher score) than the previously calculated dominating line. If the lines contains the same number
        of pieces with at least one shared attribute (same score), then store both.'''

        line_attributes = []

        # Remove all the empty slots with no piece on it
        if -1 in line:
            line = list(dict.fromkeys(line))
            line.remove(-1)

        # Store the attributes of each piece in the current line
        for elem in line:
            piece = self.board.get_piece_charachteristics(elem)
            line_attributes.append([piece.HIGH, piece.COLOURED, piece.SOLID, piece.SQUARE])

        # If there are more than 1 piece in the line, check what attributes are reccuring.
        # Result is a boolean vector where True/False represent the attributes that are common in the line
        # and None represent an attribute that is not shared. The order is [High Coloured Solid Square]
        if len(line_attributes) > 1:
            old_result = line_attributes[0]
            for i in range(len(line_attributes)-1):
                result = []
                for j,k in zip(old_result, line_attributes[i+1]):
                    if j==k:
                        result.append(j)
                    else:
                        result.append(None)
                old_result = result
        elif len(line_attributes) == 1:
            # If the line is only 1 piece, all attributes of that piece are the lines attributes.
            result = line_attributes[0]
        else: 
            result = []
        
        # Check whether the result vector has an element that is not None, thus yielding a possible new 
        # dominating line
        if any(map(lambda x: not x is None, result)):
            return [len(line_attributes), line_counter, result]
        return None

    def check_attributes(self) -> list:
        '''Calculate the number of each attribute on the board.'''

        board = self.board.get_board_status()
        attribue_values = {}
        attribue_values['High'] = 0
        attribue_values['Low'] = 0
        attribue_values['Color'] = 0
        attribue_values['Noncolor'] = 0
        attribue_values['Solid'] = 0
        attribue_values['Hollow'] = 0
        attribue_values['Square'] = 0
        attribue_values['Circle'] = 0

        for row in board:
            for elem in row:
                if elem >= 0:
                    if self.board.get_piece_charachteristics(elem).HIGH:
                        attribue_values['High'] += 1
                    else:
                        attribue_values['Low'] += 1
                    if self.board.get_piece_charachteristics(elem).COLOURED:
                        attribue_values['Color'] += 1
                    else:
                        attribue_values['Noncolor'] += 1
                    if self.board.get_piece_charachteristics(elem).SOLID:
                        attribue_values['Solid'] += 1
                    else: 
                        attribue_values['Hollow'] += 1
                    if self.board.get_piece_charachteristics(elem).SQUARE:
                        attribue_values['Square'] += 1
                    else:
                        attribue_values['Circle'] += 1
        return attribue_values

    def rank_pieces(self, attribute_values: list) -> list:
        '''Ranks the pieces according to their shared attriutes with the board'''
        val = []

        for i in range(16):
            cur_val = 0
            piece = self.board.get_piece_charachteristics(i)
            
            if piece.HIGH:
                cur_val += attribute_values['High']
            else:
                cur_val += attribute_values['Low']
            if piece.COLOURED:
                cur_val += attribute_values['Color']
            else:
                cur_val += attribute_values['Noncolor']
            if piece.SOLID:
                cur_val += attribute_values['Solid']
            else:
                cur_val += attribute_values['Hollow']
            if piece.SQUARE:
                cur_val += attribute_values['Square']
            else:
                cur_val += attribute_values['Circle']
            val.append(cur_val)
        return val

    def desired_piece(self, dom_lines: list) -> list:
        '''This function determines what attributes the piece we choose should have to avoid a loss'''

        dom_line_attributes = self.dominant_attributes(dom_lines)
        
        # If one of the attributes and it's corresponding opposite leads to a win, then we lose no matter what piece we select.
        # E.g. both high and low. 
        # If the above is not the case, store the inverse of the attributes in order to obtain a vector of what attributes 
        # we are searching for in a piece. If there's no condition on the specific attribute, i.e. the piece can be either high or low, 
        # store both True and False for the desirec piece in this attribute spot. 
        desired_piece = [[], [], [], []]
        for i in range(len(dom_line_attributes)):
            if len(dom_line_attributes[i]) == 2:
                #print("Lose no matter what")
                return self.pick_rule_3()
            elif len(dom_line_attributes[i]) == 1:
                desired_piece[i].append(not(dom_line_attributes[i][0]))
            else:
                desired_piece[i].append(True)
                desired_piece[i].append(False)

        # Now we look for a piece with the desired attributes
        found, piece_val = self.find_piece_attribute(desired_piece)
        if found:
            #print("Found a desired piece")
            return piece_val
        else:                    
        # If such a piece does not exist (have been played already), play a piece at random
            #print("No desired piece left. Picking a piece at random")
            return self.pick_rule_3()

    def dominant_attributes(self, dominant_lines) -> list:
        '''The function returns what are the common attributes in the dominating lines'''

        dom_line_attributes = [[], [], [], []]
        for i in range(4):
            for elem in dominant_lines:
                if elem[2][i] != None and elem[2][i] not in dom_line_attributes[i]:
                    dom_line_attributes[i].append(elem[2][i])
        return dom_line_attributes

    def find_piece_attribute(self, desired_piece) -> tuple:
        '''The function looks for a piece with the desired attributes and returns True and the piece value if found, otherwise
        it returns false and None'''

        for i in range(16):
            if i not in self.board.get_board_status():
                piece = self.board.get_piece_charachteristics(i)
                if piece.HIGH in desired_piece[0] and piece.COLOURED in desired_piece[1] \
                    and piece.SOLID in desired_piece[2] and piece.SQUARE in desired_piece[3]:
                    return (True, i)
        return (False, None)

    def place_piece_specified_line(self, line) -> tuple([int, int]):
        '''This function checks if the selected piece can be placed such that the agent wins'''
        board = self.board.get_board_status()

        # Check if the piece should be placed in a row
        if line[1] >= 0 and line[1] <= 3:
            # look for an empy spot in the row
            for i in range(4):
                if board[line[1]][i] == -1:
                    return (i, line[1])
        # Check if the piece should be placed in a column
        elif line[1] >= 4 and line[1] <= 7:
            for i in range(4):
                if board[i, line[1]-4] == -1:
                    return (line[1]-4, i)
        # Check if the piece should be placed on the diagonal
        elif line[1] == 8:
            for i in range(4):
                if board[i, i] == -1:
                    return (i, i)
        # Check if the piece should be placed on the off-diagonal
        elif line[1] == 9:
            for i in range(4):
                if board[3-i, i] == -1:
                    return (i, 3-i)

    def count_shared_attributes_in_line(self, piece) -> list:
        '''This function counts the number of shared attributes in the line with the selected piece. If the piece
        is high and the line contains 2 high pieces, this will count as 2 shared attributes. Thus, longer lines will
        therefore have an advantage in being picked'''
        board = self.board.get_board_status()
        line_val = []

        # For each row
        for row in board:
            line_val.append(self.count_line(row, piece))

        # For each column
        for i in range(self.board.BOARD_SIDE):
            line_val.append(self.count_line(board[:,i], piece))

        # Diagonals
        diag = []
        off_diag = []
        for i in range(len(board)):
            diag.append(board[i,i])
            off_diag.append(board[self.board.BOARD_SIDE-1-i, i])

        line_val.append(self.count_line(diag, piece))
        line_val.append(self.count_line(off_diag, piece))

        return line_val
            
                
    def count_line(self, line, piece) -> int:
        '''Count the number of shared attributes in the line. If there's no empty spots left in the line, return -1 in order
        to avoid selecting this line'''
        val = -1
        if -1 in line:
            val  = 0
            line = list(dict.fromkeys(line))
            line.remove(-1)

            for elem in line:
                high, color, solid, square = self.piece_dict[str(elem)]
                if high == self.board.get_piece_charachteristics(piece).HIGH:
                    val += 1
                if color == self.board.get_piece_charachteristics(piece).COLOURED:
                    val += 1
                if solid == self.board.get_piece_charachteristics(piece).SOLID:
                    val += 1
                if square == self.board.get_piece_charachteristics(piece).SQUARE:
                    val += 1
        return val
    
    def length_of_board_lines(self) -> list:
        '''Counts the lengths of all lines with at least 1 free spot'''

        board = self.board.get_board_status()
        length = []

        for row in board:
            length.append(self.length_of_line(row))
        
        for i in range(self.board.BOARD_SIDE):
            length.append(self.length_of_line(board[:,i]))

        diag = []
        off_diag = []
        for i in range(len(board)):
            diag.append(board[i,i])
            off_diag.append(board[self.board.BOARD_SIDE-1-i, i])

        length.append(self.length_of_line(diag))
        length.append(self.length_of_line(off_diag))

        return length

    def length_of_line(self, line) -> int:
        '''Counts the lenght of the current line'''
        if -1 in line:
            line = list(dict.fromkeys(line))
            line.remove(-1)
            return len(line)
        else:
            return self.board.BOARD_SIDE

    def pick_rule_1(self) -> int:
        '''Pick the piece with the most common attributes with the current board'''
        attribute_values = self.check_attributes()
        piece_ranking = self.rank_pieces(attribute_values)
        max_pos = piece_ranking.index(max(piece_ranking))
        while max_pos in self.board.get_board_status():
            piece_ranking[max_pos] = -1
            max_pos = piece_ranking.index(max(piece_ranking))
        return max_pos
                

    def pick_rule_2(self) -> int:
        '''Pick the piece with the least common attributes with the current board'''
        attribute_values = self.check_attributes()
        piece_ranking = self.rank_pieces(attribute_values)
        min_pos = piece_ranking.index(min(piece_ranking))
        while min_pos in self.board.get_board_status():
            piece_ranking[min_pos] = 100
            min_pos = piece_ranking.index(min(piece_ranking))
        return min_pos

    def pick_rule_3(self) -> int:
        '''Pick a piece at random'''
        random_piece = random.randint(0, 15)
        while random_piece in self.board.get_board_status():
            random_piece = random.randint(0, 15)
        return random_piece

    def place_rule_1(self) -> tuple([int, int]):
        '''Place the piece on the longest uninterrupted line that has no shared attributes with the current piece'''

        # If there is a dominating line with 3 elements in it, we always place the piece there if it generates a win. 
        # Thus, we have already checked that we have no common attributes with all 3-length dominating lines and can therefore place
        # the piece in this line
        if len(self.dom_line_dict['3']) > 0:
            return self.place_piece_specified_line(self.dom_line_dict['3'][0])
        
        # For dominating lines of length less than 3 there first need to be a check to confirm that there are no shared attributes
        # between the selected piece and the line in order to block it. 
        for length in ['2', '1']:
            for line in self.dom_line_dict[length]:
                call = True
                for j,k in zip(line[2], list(self.piece_dict[str(self.board.get_selected_piece())])):
                    if j != None and j == k:
                        call = False
                        break
                if call:
                    return self.place_piece_specified_line(line)

        # If there are no dominating lines of any lenght we can block, place it randomly 
        return self.place_rule_6()

    def place_rule_2(self):
        '''Place the piece on the longest uninterrupted line with a shared attribute, might not be the dominating line'''

        # There cannot be a uninterrupted line with 3 elements with a shared attribute with out piece, if that was the 
        # case, the piece would already have been placed there! 
        # Thus we only need to check uninterrupted lines of length 2 and 1 and see where our piece has a shared attribute

        for length in ['2', '1']:
            for line in self.dom_line_dict[length]:
                for j,k in zip(line[2], list(self.piece_dict[str(self.board.get_selected_piece())])):
                    if j != None and j == k:
                        return self.place_piece_specified_line(line)
        
        # If there are no uninterrupted lines with a shared attribute, place it randomly
        return self.place_rule_6()

    def place_rule_3(self):
        '''Places the piece on the line with the most shared attributes independent of length'''

        piece = self.board.get_selected_piece()
        line_values = self.count_shared_attributes_in_line(piece)
        return self.place_piece_specified_line([0, line_values.index(max(line_values))])

    def place_rule_4(self):
        '''Place the piece on the shortest line, independent of attributes'''

        lengths_on_board = self.length_of_board_lines()
        return self.place_piece_specified_line([0, lengths_on_board.index(min(lengths_on_board))])

    def place_rule_5(self):
        '''Place the piece on the longest line, independent of attributes'''

        lengths_on_board = self.length_of_board_lines()

        # Replace all the lines of length 4 with a -1 as we cannot place a piece on these lines
        if 4 in lengths_on_board:
            for i in range(len(lengths_on_board)):
                if lengths_on_board[i] == 4:
                    lengths_on_board[i] = -1
        return self.place_piece_specified_line([0, lengths_on_board.index(max(lengths_on_board))])

    def place_rule_6(self):
        '''Place the piece at random'''
        board = self.board.get_board_status()

        x = random.randint(0, 3)
        y = random.randint(0, 3)

        while board[x,y] != -1:
            x = random.randint(0, 3)
            y = random.randint(0, 3)

        return (y, x)