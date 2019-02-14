from connect4 import error_check, error_check_2, check_victory, class_copy, index, display_board, game
from math import inf


def check_move(game, col):
    if game.mat[-1, col] != 0: return False
    return True


def apply_move(game, col):
    for i in range(game.rows):
        if game.mat[i, col] == 0:
            game.mat[i, col] = game.turn
            break
    game.turn = 3 - game.turn

# TODO independent on game.win
def grading(move_point, marks):
    if sum(1 for _ in move_point if sum(_) > 0) == 0: return -1
    grade = 0
    for i in move_point:
        if i[0] > 0 and sum(i) > 3: grade += marks[i[0]+1]
    return grade

# TODO independent on game.win.
def all_consecutive(game, index, turn=1):
    cols, rows, wins = game.cols, game.rows, game.wins
    # The first value represents the number of consecutive discs, whereas the second value represents
    # the number of 0 which is aligned to that line, if it exists. This is to check whether the 3-consecutive-disc is
    # able to be 4-in-a-row.
    re, minimum = [[0, 0], [0, 0], [0, 0], [0, 0]], min(cols, rows)
    r, c, op = index[0], index[1], 3-turn
    # Check vertically.
    for i in range(1, rows):
        if r+i >= rows or game.mat[r+i, c] == op or sum(re[1]) == wins: break
        if game.mat[r+i, c] == turn: re[0][0] += 1
        else: re[0][1] += 1
    for i in range(1, rows):
        if r-i < 0 or game.mat[r-i, c] == op or sum(re[0]) == wins: break
        re[0][0] += 1
    # Check horizontally.
    for i in range(1, cols):
        if c+i >= cols or game.mat[r, c+i] == op or sum(re[0]) == wins: break
        if game.mat[r, c+i] == turn: re[1][0] += 1
        else: re[1][1] += 1
    for i in range(1, cols):
        if c-i < 0 or game.mat[r, c-i] == op or sum(re[0]) == wins: break
        if game.mat[r, c-i] == turn: re[1][0] += 1
        else: re[1][1] += 1
    # Check diagonally, from bottom left to top right.
    for i in range(1, minimum):
        if r+i >= rows or c+i >= cols or game.mat[r+i, c+i] == op or re[2] == wins: break
        if game.mat[r+i, c+i] == turn: re[2][0] += 1
        else: re[2][1] += 1
    for i in range(1, minimum):
        if r-i < 0 or c-i < 0 or game.mat[r-i, c-i] == op or re[2] == wins: break
        if game.mat[r-i, c-i] == turn: re[2][0] += 1
        else: re[2][1] += 1
    # Check diagonally, from bottom right to top left.
    for i in range(1, minimum):
        if r+i >= rows or c-i < 0 or game.mat[r+i, c-i] == op or re[3] == wins: break
        if game.mat[r+i, c-i] == turn: re[3][0] += 1
        else: re[3][1] += 1
    for i in range(1, minimum):
        if r-i < 0 or c+i >= cols or game.mat[r-i, c+i] == op or re[3] == wins: break
        if game.mat[r-i, c+i] == turn: re[3][0] += 1
        else: re[3][1] += 1

    return re


def generate_move(game):
    return [col for col in range(game.cols) if game.mat[-1, col] == 0]


def compute_points(game, all_move, marks, depth):
    ans = []
    for move in all_move:
        # Generate index of the recent dropped disc.
        i = index(game, move)
        grade = grading(all_consecutive(game, i), marks)
        ans.append((grade, move))
    ans.sort()
    return ans[-1][0], depth, ans[-1][1]


def recursive(game, depth, marks, maxi, move=None):
    if move is not None:
        game = class_copy(game)
        apply_move(game, move)
    all_move = generate_move(game)
    # If reached terminal depth or terminal game.
    if depth < 2 and maxi: return compute_points(game, all_move, marks, depth)
    # ...
    elif maxi:
        ans = []
        for i in all_move:
            grade = grading(all_consecutive(game, index(game, i), 1), marks)
            # Terminal game, i.e. there is no move possible.
            if grade >= 100: ans.append((grade, depth-1, grade//100, i))
            # Otherwise, continues searching into deeper depth.
            else: ans.append(recursive(game, depth-1, marks, 0, i))
        return (*max(ans)[:2], move)
    else:
        ans = []
        for i in all_move:
            grade = grading(all_consecutive(game, index(game, i), 2), marks)
            # Terminal game, i.e. no move is possible.
            if grade >= 100: ans.append((-grade, depth-1, grade//100, i))
            # Otherwise, continues searching into deeper depth.
            else: ans.append(recursive(game, depth-1, marks, 1, i))
        if depth == 5: return min(ans)
        return (*min(ans)[:2], move)


def computer_move(game, depth, marks):
    return recursive(game, depth, marks, 0)[2]


def menu():
    # TODO independent on game.win.
    marks = {2: 1, 3: 10, 4: 100}
    again = 'y'
    while again == 'y':
        game.turn = 2 - (error_check_2('Do you want to make the move first?', 'y', 'n') == 'y')
        print()
        display_board(game)
        while check_victory(game) == 0:
            if game.turn == 1:
                print()
                print(f'Player {game.turn}\'s turn.')
                col = error_check('Which column do you want to make your move? ', 1, game.cols) - 1
                print()
                while not check_move(game, col):
                    print('Error. Your move is impossible.')
                    col = error_check('Which column do you want to make your move? ', 1, game.cols) - 1
                    print()
                apply_move(game, col)
            else:
                print()
                print('Computer\'s turn')
                comp_move = computer_move(game, 4, marks)
                apply_move(game, comp_move)
            display_board(game)

        vic = check_victory(game)
        print()
        if vic == 3:
            print('The board is full! The game is a draw!!')
        else:
            if vic == 1:
                print(f'Congratulations!! You have beaten the computer level 4')
            else:
                print(f'Oops. You have been defeated by the computer level 4. Good luck next time!')
        again = error_check_2('Do you want to play again?', 'y', 'n')