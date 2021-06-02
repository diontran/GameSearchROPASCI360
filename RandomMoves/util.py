"""Class includes utility functions that help calculate heurstics of boards etc.
All functions suited to calculate for the upper player, reverse and flip the input in order to calculate for the lower
player"""

from team_name.Board import *
import team_name.player as pl
from team_name.gametheory import *
import copy
import random

def state_heuristic(board_state):
    heuristic = 0
    
    """ Heuristic Based on number of total teammates against enemies"""
    # heuristic -= len(board_state['S'])
    # heuristic -= len(board_state['R'])
    # heuristic -= len(board_state['P'])
    # heuristic += len(board_state['s'])
    # heuristic += len(board_state['r'])
    # heuristic += len(board_state['p'])

    """ Heuristic Based on number of total victims against predators"""
    # for token_pos in board_state['R']:
    #     heuristic += token_vps('R', token_pos, board_state)
    # for token_pos in board_state['S']:
    #     heuristic += token_vps('S', token_pos, board_state)
    # for token_pos in board_state['P']:
    #     heuristic += token_vps('P', token_pos, board_state)

    # for token_pos in board_state['r']:
    #     heuristic -= token_vps('r', token_pos, board_state)
    # for token_pos in board_state['s']:
    #     heuristic -= token_vps('s', token_pos, board_state)
    # for token_pos in board_state['p']:
    #     heuristic -= token_vps('p', token_pos, board_state)

    """ Heuristic Based on wellbeing of token"""
    for token_pos in board_state['R']:
        heuristic += token_value('R', token_pos, board_state)
    for token_pos in board_state['S']:
        heuristic += token_value('S', token_pos, board_state)
    for token_pos in board_state['P']:
        heuristic += token_value('P', token_pos, board_state)

    for token_pos in board_state['r']:
        heuristic -= token_value('r', token_pos, board_state)
    for token_pos in board_state['s']:
        heuristic -= token_value('s', token_pos, board_state)
    for token_pos in board_state['p']:
        heuristic -= token_value('p', token_pos, board_state)
    return heuristic

def token_vps(token_type, token_pos, board_state):
    """Function returns the number of a victims minus the number of predators the token has"""
    victim_num = len(get_victims(token_type, board_state))
    predator_num = len(get_predators(token_type, board_state))
    return  predator_num - victim_num

def token_value(token_type, token_pos, board_state):
    """Function returns the "wellbeing" of a token which is a part of the heurstic of the whole board.
    Defined as [distance to victims - distance to predators]
    The smaller this value, the better the "wellbeing" of the token"""
    victim_distance = distance_from_tokens(token_pos, get_victims(token_type, board_state))
    predator_distance = distance_from_tokens(token_pos, get_predators(token_type, board_state))
    #Trying to minimize value of victim_distance
    #Trying to maximize value of predator_distance
    return  predator_distance - victim_distance

def distance_from_tokens(token_pos, token_list):
    """Returns the total manhattan distance from the given token to the list of tokens provided"""
    total = 0
    if token_list != None:
        for pos in token_list:
            total += manhattan_distance(token_pos, pos)
    return total

def get_victims(token_type, board_state):
    """Function gets victims of token type"""
    if token_type == 'R':
        return board_state['s']
    elif token_type == 'P':
        return board_state['r']
    elif token_type == 'S':
        return board_state['p']
    elif token_type == 'r':
        return board_state['S']
    elif token_type == 'p':
        return board_state['R']
    elif token_type == 's':
        return board_state['P']

def get_predators(token_type, board_state):
    """Function gets predators of token type"""
    if token_type == 'R':
        return board_state['p']
    elif token_type == 'P':
        return board_state['s']
    elif token_type == 'S':
        return board_state['r']
    elif token_type == 'r':
        return board_state['P']
    elif token_type == 'p':
        return board_state['S']
    elif token_type == 's':
        return board_state['R']

def get_z(pos):
    """Function to change coordinate from offset system to cube coordinates, returning the z coordinate which is
    in relation to the r and q coordinate."""
    return (-pos[0]) - pos[1]

def manhattan_distance(pos1, pos2):
    """Function to calculate the manhattan distance between two positions"""
    z1 = get_z(pos1)
    z2 = get_z(pos2)
    return int((abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + abs(z1 - z2)) / 2)

def get_children_states(game_state, upper_throws, lower_throws):
    """Function returns a list of game states that can be reached from the game state provided as an input"""
    upper_moves = get_player_moves(game_state, 'upper', upper_throws)
    lower_moves = get_player_moves(game_state, 'lower', lower_throws)
    good_upper = filter_good_moves(upper_moves, game_state, 'upper')
    good_lower = filter_good_moves(lower_moves, game_state, 'lower')
    #A list of combination of moves, one from each player
    #combined_moves = list(itertools.product(good_upper, good_lower))
    combined_moves = []
    for umove in good_upper:
        row = []
        for lmove in good_lower:
            row.append((umove, lmove))
        combined_moves.append(row)


    children = []
    # Create a game state from the pair of moves
    for row in combined_moves:
        children_row = []
        for pair in row:
            new_state = pl.Player.update_board(game_state, 'upper', pair[1], pair[0])
            new_uthrow = upper_throws + 1 if pair[0][0] == 'THROW' else upper_throws
            new_lthrow = lower_throws + 1 if pair[1][0] == 'THROW' else lower_throws
            children_row.append((new_state, new_uthrow, new_lthrow))
        children.append(children_row)
    # print(good_upper)
    # print(good_lower)
    return children, good_upper, good_lower

def create_matrix(original_state, upper_throws, lower_throws):
    """Function uses game theory to return the best move to choose next, with the search depth of 1 only"""
    #Initialize dummy variables to create new board states and calculate heuristics
    empty_board = Board('upper')
    dummy = pl.Player('upper')
    dummy.board_representation = empty_board
    empty_board.game_state = original_state

    upper_moves = get_player_moves(original_state, 'upper', upper_throws)
    lower_moves = get_player_moves(original_state, 'lower', lower_throws)

    # CHOOSE GOOD MOVES HERE
    good_upper_moves = filter_good_moves(upper_moves, original_state, 'upper')
    good_lower_moves = filter_good_moves(lower_moves, original_state, 'lower')


    matrix = []
    for lmove in good_lower_moves:
        matrix_row = []
        for umove in good_upper_moves:
            state = copy.deepcopy(original_state)
            new_state = pl.Player.update_board(state, 'upper', lmove, umove)
            #insert at end of matrix row list
            matrix_row.append(state_heuristic(new_state))
        matrix.append(matrix_row)
    return matrix, good_upper_moves, good_lower_moves

def get_best_move(matrix, upper_moves, lower_moves):
    """Function gets chooses the best move"""
    #Upper is the column player
    answer = solve_game(matrix, maximiser= False, rowplayer= False)
    #A list of positions of the max values, only one in most cases
    max_answers = [i for i, x in enumerate(answer[0]) if x == max(answer[0])]

    #Choose a random max value and return it
    i = random.choice(max_answers)
    if type(upper_moves[i][1]) is tuple:
        return (upper_moves[i][0],upper_moves[i][1],upper_moves[i][2])
    else:
        return (upper_moves[i][0],upper_moves[i][1].lower(),upper_moves[i][2])



def get_player_moves(game_state, player_type, player_throws):
    """Function gets a list of move that the player with player_type can make"""
    moves = []
    #Throws
    type = ['R','P','S']
    temp_board = Board('upper')
    throws = temp_board.throw_area(player_throws, player_type)
    for throw_pos in throws:
        for token in type:
            moves.insert(0, ('THROW', token, throw_pos))
    #Slides
    if player_type == 'upper':
        keys = ['R','P','S']
    else:
        keys = ['r','p','s']
    empty_board = Board('upper')
    for key in keys:
        for original_pos in game_state[key]:
            neighbours = empty_board.generate_possible_move(original_pos)
            for new_pos in neighbours:
                moves.insert(0, ('SLIDE', original_pos, new_pos))
    return moves

def flip_board(board_state):
    """Function flips a board on the row axis so functions suited to compute for upper player can be used to compute
    for lower player as well, by flipping the board for computation and flipping the return value"""
    flipped_board = copy.deepcopy(board_state)
    keys = list(flipped_board.keys())
    for key in keys:
        flipped_board[key] = [flip_pos(pos) for pos in flipped_board[key]]
    #switch upper and lower tokens
    new_r = flipped_board['R']
    new_p = flipped_board['P']
    new_s = flipped_board['S']
    flipped_board['R'] = flipped_board['r']
    flipped_board['P'] = flipped_board['p']
    flipped_board['S'] = flipped_board['s']
    flipped_board['r'] = new_r
    flipped_board['p'] = new_p
    flipped_board['s'] = new_s
    return flipped_board

def flip_pos(pos):
    """Function flips position along r = 0"""
    return (-pos[0], pos[0] + pos[1])

def filter_good_moves(original_list, board_state, player_type):
    """Function takes a list of moves and filter out the good ones for backward induction algorithm to reduce compute
    time"""

    if player_type == 'upper':
        enemy_type = 'lower'
    else:
        enemy_type = 'upper'

    good_moves = []
    for move in original_list:
        if move[0] == 'SLIDE':
            #Only consider a move if it gets closer to a target or gets further away from a predator
            token_type = get_token_type(board_state, move[1], player_type)
            victims = get_victims(token_type, board_state)
            predators = get_predators(token_type, board_state)
            original_distance = distance_from_tokens(move[1], victims) - distance_from_tokens(move[1], predators)
            new_distance = distance_from_tokens(move[2], victims) - distance_from_tokens(move[2], predators)
            if new_distance < original_distance:
                good_moves.insert(0, move)
        if move[0] == 'THROW':
            include = True
            #Only consider throwing token when:
            token_type = move[1]
            if len(get_victims(token_type, board_state)) == 0: #If there is no target
                include = False
            elif get_token_type(board_state, move[2], player_type) != 'X': #An ally is on the pos
                include = False
            elif Board.token_win(get_token_type(board_state, move[2], enemy_type), move[1]): #Throwing a token onto a predator aka suiciding
                include = False
            elif distance_from_tokens(move[2], get_predators(move[1], board_state)) != 0 and token_value(move[1], move[2], board_state) >= 0:
                #Throwing a token closer to a predator than a victim
                include = False
            if include:
                good_moves.insert(0,move)
    if len(good_moves) == 0:
        return original_list
    elif len(good_moves) < 10:
        return good_moves
    else:
        return random.sample(good_moves,10)

def get_token_type(board_state, pos, player):
    """Function gets the token type in the position given"""
    for key in board_state:
        for tokenpos in board_state[key]:
            if tokenpos == pos:
                #Check if it is the player's token in case both upper and lower has a token in the grid
                if player == 'upper' and key.isupper() == True:
                    return key
                if player == 'lower' and key.islower() == True:
                    return key
    return 'X' #return X if there isn't a token in given spot


