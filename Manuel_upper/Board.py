import itertools

class Board:
    """A class representing the board to the player, providing information for the player to make a decision"""

    def __init__(self, player_type):
        self.player_type = player_type
        self.game_state = {'R':[], 'P':[], 'S':[], 'r':[], 'p':[], 's':[]}

    #A list of list of hex, where each list represents one row on the board
    board_hex = [[(4, -4),(4, -3),(4, -2),(4, -1),(4, -0)],
                [(3, -4),(3, -3),(3, -2),(3, -1),(3, 0),(3, 1)],
                [(2, -4),(2, -3),(2, -2),(2, -1),(2, 0),(2, 1),(2, 2)],
                [(1, -4),(1, -3),(1, -2),(1, -1),(1, 0),(1, 1),(1, 2),(1, 3)],
                [(0, -4),(0, -3),(0, -2),(0, -1),(0, 0),(0, 1),(0, 2),(0, 3),(0, 4)],
                [(-1, -3),(-1, -2),(-1, -1),(-1, 0),(-1, 1),(-1, 2),(-1, 3),(-1, 4)],
                [(-2, -2),(-2, -1),(-2, 0),(-2, 1),(-2, 2),(-2, 3),(-2, 4)],
                [(-3, -1),(-3, 0),(-3, 1),(-3, 2),(-3, 3),(-3, 4)],
                [(-4, 0),(-4, 1),(-4, 2),(-4, 3),(-4, 4)]]



    def get_row(self,row_num):
        """Function returns the list of hex corresponding to row number from top to bottom, row 0 being the first row"""
        return self.board_hex[4-row_num]

    def update_move(self,action,player_side):
        """Update the board's game state according to the action player passed into"""
        #Add the token to the board
        if action[0] == 'THROW':
            self.game_state[action[1]].insert(0,action[2])
        if action[0] == 'SLIDE' or action[0] == 'SWING':
            original_pos = action[1]
            new_pos = action[2]
            #update list of key in game state accordingly
            if self.player_type == 'upper' and player_side == 'player':
                    search_keys = ['R', 'P', 'S']
            elif self.player_type == 'upper' and player_side == 'opponent':
                    search_keys = ['r', 'p', 's']
            elif self.player_type == 'lower' and player_side == 'player':
                    search_keys = ['r', 'p', 's']
            elif self.player_type == 'lower' and player_side == 'opponent':
                    search_keys = ['R', 'P', 'S']
            for key in search_keys:
                if original_pos in self.game_state.get(key):
                    updated_list = self.game_state.get(key)
                    updated_list.remove(original_pos)
                    updated_list.insert(0, new_pos)
                    self.game_state[key] = updated_list

        #Battle if there are other tokens in the spot
        tokens_in_pos = []
        for key in self.game_state.keys():
            for pos in self.game_state[key]:
                if pos == action[2]:
                    tokens_in_pos.insert(0, key)
        kill_types = self.kill_tokens(tokens_in_pos)

        #Remove tokens in kill_types
        all_kill_types = []
        if kill_types != []:
            for type in kill_types:
                all_kill_types.insert(0, type)
                all_kill_types.insert(0, type.lower())

        if all_kill_types != []:
            for token in all_kill_types:
                self.game_state[token].remove(action[2])




    def get_player_token(self):
        """Function returns a dictionary of player's tokens"""
        if self.player_type == 'upper':
            included_keys = ['R', 'P', 'S']
        else:
            included_keys = ['r', 'p', 's']
        return {k:v for k,v in self.game_state.items() if k in included_keys}


    def generate_possible_move(self,pos):
        """Function returns a list of possible new positions that the current token in pos can move to"""
        possible_positions = []
        #Positions for swinging
        directions = [(0,-1),(1,-1),(1,0),(0,1),(-1,1),(-1,0)]
        for tuple in directions:
            new_pos = ((pos[0] + tuple[0]) , (pos[1] + tuple[1]))
            if new_pos in list(itertools.chain(*self.board_hex)):
                possible_positions.insert(0,new_pos)
        return possible_positions

    def token_win(type1, type2):
        """Function that returns if token type 1 beats token type 2"""
        t1 = type1.upper()
        t2 = type2.upper()
        if t1 == 'R':
            if t2 == 'S':
                return True
            else:
                return False

        if t1 == 'P':
            if t2 == 'R':
                return True
            else:
                return False

        if t1 == 'S':
            if t2 == 'P':
                return True
            else:
                return False

    def kill_tokens(self,tokens_in_pos):
        """Function receives a list of types of tokens in the same position, and remove the one which loses in battle"""
        capital = []
        for type in tokens_in_pos:
            if type.upper() not in capital:
                capital.insert(0, type.upper)
        #Case where all three types in same position
        if 'R' in capital and 'P' in capital and 'S' in capital:
            return capital #All tokens removed
        #Cases where two token types battle
        elif 'R' in capital and 'P' in capital:
            return ['R']
        elif 'P' in capital and 'S' in capital:
            return ['P']
        elif 'S' in capital and 'R' in capital:
            return ['S']
        else:
            return []

    def player_no_token(self):
        if self.player_type == 'upper':
            keys = ['R', 'P', 'S']
        else:
            keys = ['r', 'p', 's']
        number_of_tokens = 0
        for key in keys:
            number_of_tokens += len(self.game_state[key])
        if number_of_tokens == 0:
            return True
        else:
            return False