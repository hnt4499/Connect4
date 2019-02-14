import numpy as np
from connect4_level4 import *

def check():
    game.rows = 6
    game.cols = 7
    game.wins = 4
    game.turn = 2
    marks = {2: 1, 3: 10, 4: 100}
    #######
    ar = [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 1, 1, 0, 0, 0]]
    game.mat = np.array(ar[::-1])
    print(computer_move(game, 5, marks))
check()