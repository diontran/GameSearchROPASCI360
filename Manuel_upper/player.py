from team_name.Board import *
import random
import itertools

class Player:
    player_type = ''
    turn = 0
    throw_num = 0
    board_representation = None
    TOKEN_TYPE = ['r','p','s']


    #Manual move list

    manual_move = [
        ('THROW','r',(4,-4)),
        ('SLIDE',(4,-4),(3,-3)),
        ('SLIDE',(3,-3),(2,-2)),
        ('SLIDE',(2,-2),(1,-1)),
        ('SLIDE',(1,-1),(0,0)),
    ]


    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here
        self.player_type = player
        self.board_representation = Board(player)

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here

        #update to new turn
        self.turn += 1
        return self.manual_move[self.turn-1]
        # if self.turn == 5:
        #     return 'nope'
        #Choose random action
        #Must throw if first round or no tokens left for player
        
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # put your code here
        if opponent_action[0] == 'THROW':
            opponent_action = self.process_throw(opponent_action, player_action)[0]
        if player_action[0] == 'THROW':
            player_action = self.process_throw(opponent_action, player_action)[1]
        self.board_representation.update_move(opponent_action,'opponent')
        self.board_representation.update_move(player_action, 'player')
        self.board_representation.token_battle(player_action[2],opponent_action[2])
        print("=====================")
        print(self.board_representation.game_state)
        print("=====================")


    def throw_string(self, type, pos):
        return ("THROW", type, pos)

    def slide_string(self, pos1, pos2):
        return ("SLIDE", pos1, pos2)

    def swing_string(self, pos1, pos2):
        return ("SWING", pos1, pos2)

    def throw_area(self, throw_num, player_type):
        """Function returns a list of possible throw positions according to the turn number and player type"""
        if player_type == "upper":
            return list(itertools.chain(*Board.board_hex[:throw_num+1]))
        if player_type == "lower":
            reversed = Board.board_hex[::-1]
            return list(itertools.chain(*reversed[:throw_num+1]))

    def process_throw(self,opponent_action, player_action):
        """Function capitalizes THROW action's string if action done by upper player"""
        #In case nothing needs to be changed
        new_opponent_action = opponent_action
        new_player_action = player_action
        #change Token to upper if is upper player
        if self.player_type == 'upper':
            if player_action[0] == 'THROW':
                updated_type = player_action[1].upper()
                new_player_action = ('THROW', updated_type, player_action[2])
                new_opponent_action = opponent_action
        else:
            if opponent_action[0] == 'THROW':
                updated_type = opponent_action[1].upper()
                new_opponent_action = ('THROW', updated_type, opponent_action[2])
                new_player_action = player_action
        return new_opponent_action, new_player_action

    def choose_random_action(self):
        return random.choices(
            population = ['THROW', 'SWING'],
            weights = [1,0],
            k = 1
        )[0]
