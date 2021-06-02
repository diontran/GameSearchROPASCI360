from team_name.Board import *
import team_name.util as ut
import random
import itertools
import copy
from team_name.gametheory import *

class Player:
    TOKEN_TYPE = ['r','p','s']

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
        if self.player_type == 'upper':
            self.opponent_type = 'lower'
        else:
            self.opponent_type = 'upper'
        self.turn = 0
        self.throw_num = 0


    def action(self):
            """
            Called at the beginning of each turn. Based on the current state
            of the game, select an action to play this turn.
            """
            # put your code here

            #update to new turn
            self.turn += 1
            if self.turn == 1:
                return 'THROW',random.choice(['r', 's', 'p']),random.choice(Board.throw_area(0, self.player_type))


            if self.player_type == 'upper':
                # tuple = ut.create_matrix(self.board_representation.game_state, self.board_representation.upper_throw, self.board_representation.lower_throw)
                # return ut.get_best_move(tuple[0], tuple[1], tuple[2])
                result = self.backward_induction(self.board_representation.game_state, 1, self.board_representation.upper_throw, self.board_representation.lower_throw)
                if result[1][0] == 'THROW':
                    return (result[1][0],result[1][1].lower(), result[1][2])
                else:
                    return result[1]
            else:
                # tuple = ut.create_matrix(ut.flip_board(self.board_representation.game_state), self.board_representation.lower_throw, self.board_representation.upper_throw)
                # answer = ut.get_best_move(tuple[0],tuple[1],tuple[2])
                result = self.backward_induction(ut.flip_board(self.board_representation.game_state), 1, self.board_representation.lower_throw, self.board_representation.upper_throw)

                if result[1][0] == 'THROW':
                    return(result[1][0], result[1][1].lower(), ut.flip_pos(result[1][2]))
                else:
                    return(result[1][0], ut.flip_pos(result[1][1]), ut.flip_pos(result[1][2]))
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # print("===BEFORE UPDATE====")
        # print(self.board_representation.game_state)
        print(ut.eval_func(self.board_representation.game_state, [0.1, 1, 1, 0.1, 0.1, 10, 1, 0.5]))
        # put your code here
        if opponent_action[0] == 'THROW':
            opponent_action = self.process_throw(opponent_action,self.opponent_type)
        if player_action[0] == 'THROW':
            player_action = self.process_throw(player_action,self.player_type)
        self.board_representation.game_state = self.update_board(self.board_representation.game_state, self.player_type, opponent_action, player_action)
        print("=====================")
        print(self.board_representation.game_state)
        print("=====================")

    @staticmethod
    def update_board(original_state, player_type, opponent_action, player_action):
        if player_type == 'upper':
            opponent_type = 'lower'
        else:
            opponent_type = 'upper'
        new_state = copy.deepcopy(original_state)
        new_state = Board.update_move(player_action, player_type, new_state)
        new_state = Board.update_move(opponent_action, opponent_type, new_state)
        new_state = Board.token_battle(player_action[2], opponent_action[2], new_state)
        return new_state

    def throw_string(self, type, pos):
        return ("THROW", type, pos)

    def slide_string(self, pos1, pos2):
        return ("SLIDE", pos1, pos2)

    def swing_string(self, pos1, pos2):
        return ("SWING", pos1, pos2)


    def process_throw(self, action, player):
        """Function capitalizes THROW action's string if action done by upper player"""
        if player == 'upper':
            self.board_representation.upper_throw += 1
            return (action[0], action[1].upper(), action[2])
        else:
            self.board_representation.lower_throw += 1
            return action

    def choose_random_action(self):
        return random.choices(
            population = ['THROW', 'SWING'],
            weights = [1,3],
            k = 1
        )[0]

    @staticmethod
    def backward_induction(state, depth, upper_throws, lower_throws):
        """Function uses backward induction algorithm to decide on the move chosen based on looking a certain number
        of moves ahead denoted by depth"""
        if depth == 1:
            tuple = ut.create_matrix(state, upper_throws, lower_throws)
            answer = solve_game(tuple[0], maximiser= False, rowplayer= False)
            max_ans = max(answer[0])
            i = 0
            index = []
            while i < len(answer[0]):
                if answer[0][i] == max_ans:
                    index.append(i)
                i += 1

            return answer[1], tuple[1][random.choice(index)]
            #return ut.state_heuristic(state)
        else:
            children_data = ut.get_children_states(state, upper_throws, lower_throws)

            # print(len(children_data[1]))
            # print(len(children_data[2]))

            children = children_data[0]


            hlist = [] #A list containing heuristics for children nodes
            for row in children:
                heur_row = []
                for child in row:
                    heur_row.append(Player.backward_induction(child[0], depth - 1, child[1], child[2])[0])
                hlist.append(heur_row)

            # for row in hlist:
            #     print(row)


            answer = solve_game(hlist, maximiser= False, rowplayer= True)
            max_ans = max(answer[0])

            # print(answer[0])
            # print(max_ans)

            i = 0
            index = []
            while i < len(answer[0]):
                if answer[0][i] == max_ans:
                    index.append(i)
                i += 1

            # print(children_data[1])
            # print(len(children_data[1]))
            # print(children_data[2])
            # print(len(children_data[2]))
            # print(index)


            decided_move = children_data[1][random.choice(index)]
            if decided_move[0] == 'THROW':
                return_move = (decided_move[0], decided_move[1].lower(), decided_move[2])
            else:
                return_move = decided_move

        return answer[1], return_move
