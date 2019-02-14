import numpy as np
import random
from itertools import groupby
from math import inf

class Game:
    mat = np.zeros((6, 7))
    rows = 6
    cols = 7
    turn = 1
    wins = 4


game = Game()
# The first error check ensures that the input is an integer and that it is within the preset minimum and maximum value.
# Otherwise, an error message is printed.
def error_check(qns, minV, maxV, *cre):
    x = input(f'{qns} ({minV}-{maxV}) ')
    if x == '*':
        print(cre)
        raise SystemExit
    while not x.isdigit() or int(x) not in range(minV, maxV + 1):
        print(f'Error. The input should be in range of {minV} and {maxV}')
        x = input(f'{qns} ({minV}-{maxV}) ')
    return int(x)
# The second error check ensures that the input is not an integer
# and that it is the exact input required. Otherwise, an error message is printed.
def error_check_2(qns, valid1, valid2, *cre):
    x = input(f'{qns} ({valid1}/{valid2}) ')
    if x == '*':
        print(cre)
        raise SystemExit
    while x != valid1 and x != valid2:
        print('Error. You entered invalid input.')
        x = input(f'{qns} ({valid1}/{valid2}) ')
    return x

# This sets the game board to the default, which is 6 rows and 7 columns, with 4 consecutive discs required to win.
def set_default(game):
    game.mat = np.zeros((6, 7))
    game.rows = 6
    game.cols = 7
    game.wins = 4
    game.turn = 1

# TODO index of columns as well as color of two players' discs and recent dropped discs.
def display_board(game):
    for i in game.mat[::-1]: print(i)


def apply_move(game, col, pop):
    # This updates the board in a pop move, such that within the specified column, its index 0 takes the value of
    # index 1, index 1 takes the value of index 2 ... etc. The top row will be replaced by a 0.
    if pop:
        for i in range(game.rows-1): game.mat[i, col] = game.mat[i+1, col]
        game.mat[-1, col] = 0
    # This updates the board in a normal move by replacing the lowest 0 in a column by a player's turn.
    else:
        for i in range(game.rows):
            if game.mat[i, col] == 0:
                game.mat[i, col] = game.turn
                break
    # This updates the game turn.
    game.turn = 3 - game.turn
    return game
# Checks to ensure that the player did not specify a column that is outside the board size,
# and that the column is not fully filled up already. If the player chose a pop move,
# this checks the last row of that specified column to ensure that it belongs to the player making the move.
def check_move(game, col, pop):
    if col not in range(game.cols): return False
    elif pop:
        if game.mat[0, col] != game.turn: return False
        return True
    else:
        if game.mat[-1, col] != 0: return False
        return True

# This creates a board that will be used to identify the possible moves for the the lvl 2 computer.
def class_copy(game):
    class Game_2:
        mat = game.mat.copy()
        cols = game.cols
        turn = game.turn
        rows = game.rows
        wins = game.wins
    return Game_2()


def check_column(game, col, pop): # This is to check if A SPECIFIC MOVE leads to a victory situation for whoever makes that move.
    game_copy = class_copy(game)
    if not check_move(game_copy, col, pop): return False
    apply_move(game_copy, col, pop)
    if check_victory(game_copy) == 3 - game_copy.turn: return True
    else: return False


def win_avoid_move(game, level):
    all_move = []
    # This part is to check and return a move that leads to a direct win for the computer.
    for column in range(game.cols):
        for boolean in range(2):
            # This below line is to generate a list of all possible, valid moves of the computer through the iteration.
            if check_move(game, column, boolean): all_move.append((column, boolean))
            # If a victory situation can be reached, return the move.
            if check_column(game, column, boolean): return column, boolean

    all_move_ = all_move[::]
    for move in all_move_:
        game_copy = class_copy(game)
        # Apply a random move and if that move doesnt lead to victory for the opponent, return that move.
        apply_move(game_copy, move[0], move[1])
        ans = [check_column(game_copy, column, boolean) for column in range(game.cols) for boolean in range(2)]
        if any(ans): all_move.remove(move)
    # Otherwise, when all moves lead to the victory for the opponent, then simply pick a random move (level 2),
    # or return all possible, valid moves (level 3)
    if level == 2:
        return random.choice(all_move_ if all_move == [] else all_move)
    # Return all possible, valid moves that does NOT lead to win of the opponent, if such move exists.
    elif level == 3:
        return -1, all_move_ if all_move == [] else all_move

# All consecutive discs in the board, with respect to the turn.
def all_consecutive(game, index, turn, pop=None):
    cols, rows, wins = game.cols, game.rows, game.wins
    re, minimum = [0, 0, 0, 0], min(cols, rows)
    r, c = index[0], index[1]
    # If not a pop move, then proceed to check vertical line, with respect to the recent move.
    if pop is None:
        for i in range(1, rows):
            if r + i >= rows or game.mat[r + i, c] != turn or re[1] == wins: break
            re[1] += 1
        for i in range(1, rows):
            if r - i < 0 or game.mat[r - i, c] != turn or re[1] == wins: break
            re[1] += 1
    # Check horizontally.
    for i in range(1, cols):
        if c+i >= cols or game.mat[r, c+i] != turn or re[0] == wins: break
        re[0] += 1
    for i in range(1, cols):
        if c-i < 0 or game.mat[r, c-i] != turn or re[0] == wins: break
        re[0] += 1
    # Check diagonally, from bottom left to top right.
    for i in range(1, minimum):
        if r+i >= rows or c+i >= cols or game.mat[r+i, c+i] != turn or re[2] == wins: break
        re[2] += 1
    for i in range(1, minimum):
        if r-i < 0 or c-i < 0 or game.mat[r-i, c-i] != turn or re[2] == wins: break
        re[2] += 1
    # Check diagonally, from bottom right to top left.
    for i in range(1, minimum):
        if r+i >= rows or c-i < 0 or game.mat[r+i, c-i] != turn or re[3] == wins: break
        re[3] += 1
    for i in range(1, minimum):
        if r-i < 0 or c+i >= cols or game.mat[r-i, c+i] != turn or re[3] == wins: break
        re[3] += 1

    return re

# Return the grade of that move.
def grading(test, marks, turn):
    grade = 1
    for i in test:
        if i > 0: grade *= marks[i+1][turn]
    return grade


def index(game, col):
    for i in range(game.rows):
        if game.mat[i, col] == 0: return i, col
    return -1, col


def compute_points(game, all_move, marks, depth=None):
    ans, turn = [], game.turn
    for move in all_move:
        # Generate index of the recent dropped disc.
        i = index(game, move[0])
        grade, grade_1, grade_2 = 1, 1, 1
        # If that move is a pop move.
        if move[1]:
            game_copy = class_copy(game)
            apply_move(game_copy, move[0], move[1])
            for r in range(i[0] - 1):
                ind = (r, i[1])
                if game_copy.mat[ind] == turn and game.mat[ind] == 3-turn:
                    grade_1 *= grading(all_consecutive(game_copy, ind, 3-turn, 1), marks, 0)
                    grade_2 *= grading(all_consecutive(game_copy, ind, turn, 1), marks, 1)
                elif game_copy.mat[ind] == 3-turn and game.mat[ind] == turn:
                    grade_1 /= grading(all_consecutive(game_copy, ind, 3-turn, 1), marks, 0)
                    grade_2 /= grading(all_consecutive(game_copy, ind, turn, 1), marks, 1)
        else:
            grade_1 = grading(all_consecutive(game, i, 1), marks, 1)
            grade_2 = grading(all_consecutive(game, i, 2), marks, 0)
            grade = grade_1 * grade_2
        ans.append((grade, move))
    ans.sort()
    if depth is None:
        for i in range(len(ans)-1):
            if ans[-i-2][0] != ans[-1][0]: return random.choice(ans[-i-1:])[1]
    else: return ans[-1][0], depth, ans[-1][1]


# TODO execution (thinking) time and number of iterations.
def computer_move(game, level, marks):
    if level == 1:
        col, pop = random.randint(0, game.cols - 1), random.randint(0, 1)
        while not check_move(game, col, pop):
            col, pop = random.randint(0, game.cols - 1), random.randint(0, 1)
        return col, pop

    elif level == 2:
        return win_avoid_move(game, 2)

    if level == 3:
        all_move = win_avoid_move(game, 3)
        if all_move[0] == -1:
            all_move = all_move[1]
            return compute_points(game, all_move, marks)
        else: return all_move
# This checks if a specific number of consecutive discs is met, as well as checking if the game has drawn by checking
# if there is at least one 0 remaining in the game board.
def consecutive(game, lis):
    ans = []
    for player, counter in groupby(lis):
        p = int(player)
        if (sum(1 for _ in counter) >= game.wins and p in [1, 2]) or p == 0: ans.append(p)
    return ans


# Based on the chosen number of consecutive discs to win, check if either player has won the game, or if the game has drawn.
def check_victory(game):
    result, diag_mat, diag_mat_2 = [], [], []
    minimum = min(game.cols, game.rows)

    for r in game.mat: result.extend(consecutive(game, r))
    for c in zip(*game.mat): result.extend(consecutive(game, c))
    # Generate two diagonal matrices, in which the diagonals are re-arranged to the verticals, filling with -1
    for counter, r in enumerate(game.mat):
        diag_mat.append([-1]*(minimum-1-counter) + r.tolist() + [-1]*counter)
        diag_mat_2.append([-1]*counter + r.tolist() + [-1]*(minimum-1-counter))
    # Check victory situations for the diagonal matrices
    for diag in zip(*diag_mat): result.extend(consecutive(game, diag))
    for diag_2 in zip(*diag_mat_2): result.extend(consecutive(game, diag_2))

    final_res = sorted(set(result))

    if final_res == [0, 1, 2]: return 3-game.turn # Rare situation mentioned in the guidelines.
    elif final_res == []: return 3 # Draw, where there is no winner and there is no 0 left in the board.
    else: return final_res[-1]


def menu():
    # Credits
    cre = '''Thanks for playing this game.
Authors: Hoang Nghia Tuyen, Yuelin, Brendon.'''
    # Main menu, which also shows the current values of row, column and discs required to win.
    main = '''
\t\t== CONNECT FOUR ===
\t\t==== MAIN MENU ====

1. Play game (Human vs. Human)
2. Play game (Human vs. Computer)
3. Change the board size (Current: {}x{})
4. Change the number of discs required to win (Current: {})
5. Exit
At any time, you can enter \'*\' to quit the game.
'''

    # Initialize game.
    set_default(game)
    again = 'y'
    while again == 'y':
        print(main.format(game.rows, game.cols, game.wins))
        inp = error_check('Please select an option.', 1, 5, cre)
        # option 3: change the board size.
        if inp == 3:
            game.rows = error_check('How many rows do you want?', 3, 10, cre)  # minimum and maximum number of rows is 3 and 10 respectively.
            game.cols = error_check('How many columns do you want?', 3, 10, cre)  # minimum and maximum number of columns is 3 and 10 respectively.
        # option 4: change the number of consecutive discs required to win.
        elif inp == 4:
            m = max(game.cols, game.rows)
            game.wins = error_check('How many consecutive number of discs to win?', 3, m if m < 6 else 5, cre)
        # option 5: exit.
        elif inp == 5:
            again = 'n'
        # option 1 or 2: play a game.
        elif inp in [1, 2]:
            game.mat = np.zeros((game.rows, game.cols))
            game.turn = 1
            if inp == 2:
                level = error_check('Which level of computer do you want to play with?', 1, 4, cre)
                # Grading system.
                marks = {2: [8, 10], 3: [16, 20], 4: [32, 40], 5: [64, 80], 6: [128, 160]}
                if level == 3:
                    for i in range(game.wins, 7): marks[i] = [inf, inf]
                elif level == 4:
                    for i in range(game.wins, 7): marks[i] = [-inf, inf]

                game.turn = 2 - (error_check_2('Do you want to make the move first?', 'y', 'n', cre) == 'y')
                print()
            display_board(game)
            while check_victory(game) == 0:
                if inp == 1 or game.turn == 1:
                    print()
                    print(f'Player {game.turn}\'s turn.')
                    pop = error_check_2('Do you want to pop out your disc? ', 'y', 'n', cre) == 'y'
                    col = error_check('Which column do you want to make your move? ', 1, game.cols, cre) - 1
                    print()
                    while not check_move(game, col, pop):
                        print('Error. Your move is impossible.')
                        pop = error_check_2('Do you want to pop out your disc? ', 'y', 'n', cre) == 'y'
                        col = error_check('Which column do you want to make your move? ', 1, game.cols, cre) - 1
                        print()
                    apply_move(game, col, pop)
                else:
                    print()
                    print('Computer\'s turn')
                    comp_move = computer_move(game, level, marks)
                    apply_move(game, comp_move[0], comp_move[1])
                display_board(game)

            vic = check_victory(game)
            print()
            if vic == 3:
                print('The board is full! The game is a draw!!')
            else:
                if inp == 1: print(f'Congratulations!! Player {vic} is the winner!')
                # if inp != 1, which means Human vs. Computer mode, then...
                elif vic == 1: print(f'Congratulations!! You have beaten the computer level {level}')
                else: print(f'Oops. You have been defeated by the computer level {level}. Good luck next time!')
            again = error_check_2('Do you want to play again?', 'y', 'n', cre)
    else: print(cre)