
import random

def generate_random_move(valid_moves):
    #random fct in python generates a number from a to b inclusive!!
    return valid_moves[random.randint(0, len(valid_moves) - 1)]