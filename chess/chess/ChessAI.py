from chess import ChessEngine
from chess import ChessMain
import random

def generate_random_move(valid_moves):
    #random fct in python generates a number from a to b inclusive!!
    return valid_moves[random.randint(0, len(valid_moves) - 1)]

def evaluate_simple(gs, max_color): #eval fct that simply returns material scores of white/black
    if max_color == 'w':
        return gs.white_material_score

def minimax(board, depth, max_player, max_color):
    pass

def evaluate_complex(): # more complex eval fct
    pass