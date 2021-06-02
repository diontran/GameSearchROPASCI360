import itertools
import copy

class Board:
    """A class representing the board to the player, providing information for the player to make a decision"""

    def __init__(self, player_type):
        self.player_type = player_type
        self.game_state = {'R':[], 'P':[], 'S':[], 'r':[], 'p':[], 's':[]}
        self.upper_throw = 0
        self.lower_throw = 0

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

    @staticmethod
    def update_move(action, action_player, original_state):
        """Create a new board game state according to the action player passed into"""
        new_state = copy.deepcopy(original_state)
        #Add the token to the board
        if action[0] == 'THROW':
            if action_player == 'upper':
                new_state[action[1].upper()].insert(0,action[2])
            else:
                new_state[action[1]].insert(0,action[2])
        elif action[0] == 'SLIDE' or action[0] == 'SWING':
            original_pos = action[1]
            new_pos = action[2]
            #update list of key in game state accordingly
            if action_player == 'upper':
                     search_keys = ['R', 'P', 'S']
            else:
                    search_keys = ['r', 'p', 's']
            for key in search_keys:
                if original_pos in new_state.get(key):
                    updated_list = new_state.get(key)
                    updated_list.remove(original_pos)
                    updated_list.insert(0, new_pos)
                    new_state[key] = updated_list
        return new_state

    @staticmethod
    def token_battle(pos1, pos2, original_state):
        """Function checks if there are multiple tokens in the spots that tokens just moved to, and remove tokens that
        loses in battle"""
        new_state = copy.deepcopy(original_state)
        positions = [pos1,pos2]
        for affected_pos in positions:
            #Battle if there are other tokens in the spot
            tokens_in_pos = []
            for key in new_state.keys():
                for pos in new_state[key]:
                    if pos == affected_pos:
                        tokens_in_pos.insert(0, key)
            kill_types = Board.kill_tokens(tokens_in_pos)

            #Remove tokens in kill_types
            all_kill_types = []
            if kill_types != []:
                for type in kill_types:
                    all_kill_types.insert(0, type)
                    all_kill_types.insert(0, type.lower())

            if all_kill_types != []:
                for token in all_kill_types:
                    new = []
                    for pos in new_state[token]:
                        if pos != affected_pos:
                            new.append(pos)
                    new_state[token] = new

        return new_state

    @staticmethod
    def throw_area(throw_num, player_type):
        """Function returns a list of possible throw positions according to the turn number and player type"""
        if throw_num >= 9:
            return []
        if player_type == "upper":
            return list(itertools.chain(*Board.board_hex[:throw_num+1]))
        if player_type == "lower":
            reversed = Board.board_hex[::-1]
            return list(itertools.chain(*reversed[:throw_num+1]))


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

    @staticmethod
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

    @staticmethod
    def kill_tokens(tokens_in_pos):
        """Function receives a list of types of tokens in the same position, and remove the one which loses in battle"""
        capital = []
        for type in tokens_in_pos:
            if type.upper() not in capital:
                capital.insert(0, type.upper())
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