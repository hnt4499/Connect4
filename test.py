import numpy as np
from connect4_2 import *

def a():
    
    game = Game()
    game.rows = 6
    game.cols = 7
    game.wins = 4
    game.turn = 1
    game.mat = np.zeros((game.rows, game.cols))
    
    # ***************** first test ***************** #
    if check_move(game,0,False): 
        print("test 1: OK !")
    else: 
        print("test 1: Fail of the check_move function !")
    
    # ***************** second test ***************** #
    if not check_move(game,0,True): 
        print("test 2: OK !")
    else: 
        print("test 2: Fail of the check_move function !")
        
    # ***************** third test ***************** #
    game_board_test3 = [[ 1,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]]
    game = apply_move(game,0,False)
    if (game_board_test3 == game.mat).all() : 
        print("test 3: OK !")
    else: 
        print("test 3: Fail of the apply_move function !")
    
    # ***************** fourth test ***************** #
    if check_victory(game) == 0:
        print("test 4: OK !")
    else:
        print(check_victory(game))
        print("test 4: Fail of the check_victory function !")
     
    # ***************** fifth test ***************** #
    game.turn = 1
    game.mat = np.array([[1,1,2,2,1,1,2], [1,1,2,2,1,1,2], [2,2,1,1,2,2,1], [2,2,1,1,2,2,1], [1,1,2,2,1,1,2], [1,1,0,2,1,1,2]])
    if computer_move(game,1) in [(2,False),(0,True),(1,True),(4,True),(5,True)]:
        print("test 5: OK !")
    else: 
        print("test 5: Fail of the computer_move function !")
        
a()