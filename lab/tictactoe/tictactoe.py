"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cntX = cntO = 0

    for row in board:
        for cell in row:
            if cell == X:
                cntX += 1
            elif cell == O:
                cntO += 1

    return X if cntX <= cntO else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError(f"Invalid action: {action}")

    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if terminal(board):
        for row in range(3):
            if all(board[row][col] == X for col in range(3)):
                return X
            elif all(board[row][col] == O for col in range(3)):
                return O

        for col in range(3):
            if all(board[row][col] == X for row in range(3)):
                return X
            elif all(board[row][col] == O for row in range(3)):
                return O

        if all(board[i][i] == X for i in range(3)):
            return X
        elif all(board[i][i] == O for i in range(3)):
            return O

        if all(board[i][2 - i] == X for i in range(3)):
            return X
        elif all(board[i][2 - i] == O for i in range(3)):
            return O
        
        return None
    else:
        return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    for row in range(3):
        if all(board[row][col] == X for col in range(3)) or all(board[row][col] == O for col in range(3)):
            return True

    for col in range(3):
        if all(board[row][col] == X for row in range(3)) or all(board[row][col] == O for row in range(3)):
            return True

    if all(board[i][i] == X for i in range(3)) or all(board[i][i] == O for i in range(3)):
        return True

    if all(board[i][2 - i] == X for i in range(3)) or all(board[i][2 - i] == O for i in range(3)):
        return True

    return not any(cell is EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    winner_value = winner(board)
    if winner_value == X:
        return 1
    elif winner_value == O:
        return -1
    else:
        return 0


def max_value(board, beta = 2):
    if terminal(board):
        return (utility(board), None)
    v = (-2, None)
    for action in actions(board):
        min_value_result = min_value(result(board, action), v[0])
        if min_value_result[0] > beta:
            return (min_value_result[0], action)
        if min_value_result[0] > v[0]:
            v = (min_value_result[0], action)
    return v

def min_value(board, alpha = -2):
    if terminal(board):
        return (utility(board), None)
    v = (2, None)
    for action in actions(board):
        max_value_result = max_value(result(board, action), v[0])
        if max_value_result[0] < alpha:
            return (max_value_result[0], action)
        if max_value_result[0] < v[0]:
            v = (max_value_result[0], action)
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if (terminal(board)):
        return None
    
    player_turn = player(board)
    if player_turn == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]
