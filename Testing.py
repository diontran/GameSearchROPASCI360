from team_name import util
from team_name.Board import *
from RandomMoves.player import *

empty_board = {'R':[], 'P':[], 'S':[], 'r':[], 'p':[], 's':[]}
# <<<<<<< HEAD
# board_state1 = {'R':[(-2, 0)], 'P':[], 'S':[], 'r':[(-3,-1)], 'p':[(-3, 4)], 's':[]}
# =======
# board_state1 = {'R':[(1, -1)], 'P':[], 'S':[], 'r':[], 'p':[(4, -1)], 's':[]}
# >>>>>>> 35a015a56809fc0ae6866c9c09799fe8bfeb702b
board_state2 = {'R':[(0, -2)], 'P':[(0, 2)], 'S':[], 'r':[(-1, 0)], 'p':[], 's':[(3, 0)]}
board_state3 = {'R':[(0, -2)], 'P':[(0, 2)], 'S':[(-3, 2)], 'r':[(-1, 0)], 'p':[], 's':[(3, 0), (-1, 3)]}
board_state5 = {'R':[(1, -1)], 'P':[], 'S':[], 'r':[], 'p':[], 's':[(-4, 3)]}
board_state6 = {'R':[(0, -4)], 'P':[], 'S':[], 'r':[], 'p':[(-2, -2)], 's':[]}
board_state7 = {'R':[(0, -3)], 'P':[], 'S':[], 'r':[], 'p':[(-1, -3)], 's':[]}
board_state8 = {'R':[(0, -3)], 'P':[], 'S':[], 'r':[], 'p':[(0, -3)], 's':[]}
board_state9 = {'R':[], 'P':[], 'S':[(2, -2)], 'r':[], 'p':[(-2, 2)], 's':[]}
board_state10 = {'R': [(4, 0), (4, 0)], 'P': [(-3, 4), (4, -4)], 'S': [(4, -1), (4, -1)], 'r': [(-2, 4), (-2, 4)], 'p': [(-1, 4), (-3, -1)], 's': []}





test0_lower = {'R':[], 'P':[(4, -2)], 'S':[], 'r':[], 'p':[], 's':[(4, -4)]}

if __name__ == "__main__":
# <<<<<<< HEAD
#     upper_moves = util.get_player_moves(board_state1, 'upper', 1)
#     print(util.filter_good_moves(upper_moves, board_state1, 'upper'))
# =======
#     dummy = Player('lower')
#     tempboard = Board('lower')
#     tempboard.game_state = test0_lower
#     dummy.board_representation = tempboard
#
#     opponent_action = ('THROW', 'p', (4, 0))
#     player_action = ('THROW', 'p', (-4, 0))
#
#     print("===BEFORE ACTION===")
#     print(dummy.board_representation.game_state)
#     dummy.action()
#     print("===AFTER ACTION===")
#     print(dummy.board_representation.game_state)
# >>>>>>> 35a015a56809fc0ae6866c9c09799fe8bfeb702b


    upperplayer = Player('upper')
    upperplayer.board_representation.game_state = board_state5
    upperplayer.board_representation.upper_throw = 1
    upperplayer.board_representation.lower_throw = 1
    print(upperplayer.action())
    print(upperplayer.action())
    print(upperplayer.action())
