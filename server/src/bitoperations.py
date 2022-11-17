from gmpy2 import xmpz

# from 0 to 41 is our board
# from 42 to 63 each three bits represent column [6,7]
"""
Performs the play move for the AI agent.

Arguments:
    col: the column number to insert the agent piece in.
    state: the game state.
    player: the value of it is 0 by default, indicating the turn of the AI agent.
    
Returns:
    Tuple of boolean and state data types.
"""


def play(col, state=xmpz(), player=0):
    # Take the current state. Player = 0 indicates the AI agent. Player = 1 indicates the human.
    # State of the game reached the end, calculate the score.
    if check_end(state):
        return get_score(bits_to_matrix(state))
    # If the next row violates the bounds, refuse the move.
    elif col > 6 or col < 0:
        return False, state

    start_index = 42 + col * 3
    end_index = start_index + 3

    if state[start_index:end_index] == 6:
        return False, state

    # If the move is legal, do it.
    elif state[start_index:end_index] < 6:
        required_bit = col * 6 + state[start_index:end_index]
        if player == 0:
            state = state.bit_clear(required_bit)
        else:
            state = state.bit_set(required_bit)
        req_sum = xmpz()
        req_sum = req_sum.bit_set(start_index)
        state = req_sum + state
        return True, state
    return False, state


"""
Takes the current state of the game and checks whether the game has come up to an end or not.
Arguments:
    state: the current state of the game.
Returns:
    Boolean: indicating the game has reached an end or not.
"""


def check_end(state):
    # If all columns are full, return true. Return false otherwise.
    return state[42:63] == 1797558


"""
Converts the game state from bits to 2D matrix.
Arguments:
    state: the current game state.
Returns:
    array[][].
"""


def bits_to_matrix(state):
    # An auxiliary function to help the GUI and the heuristics.
    board = [[0 for i in range(7)] for j in range(6)]
    for i in range(0, 7):
        start_index = 42 + i * 3
        end_index = start_index + 3
        last_row = state[start_index:end_index]
        last_row = last_row.numerator
        for j in range(0, last_row):
            if state[i * 6 + j] == 0:
                board[j][i] = 1
            else:
                board[j][i] = 2
    return board


"""
Calculates the scores of each player given a certain state.
Arguments:
    state: the game state that needs the score calculation.
Returns:
    Tuple of the scores of the 2 players.
"""


def get_score(state):
    board = bits_to_matrix(state)
    score_one = 0
    score_two = 0
    score = 0

    for i in range(0, 6):
        for j in range(0, 7):
            # If the user chose to end the game with free places in the board, we ignore its calculations.
            if board[i][j] == 0:
                continue

            if i + 3 < 6 and vertical_four(board, i, j):
                score += 1
                if j + 3 < 7 and diagonal_four(board, i, j, True):
                    score += 1
                if j - 3 > -1 and diagonal_four(board, i, j, False):
                    score += 1
            if j + 3 < 7 and horizontal_four(board, i, j):
                score += 1

            if board[i][j] == 1:
                score_one += score
            elif board[i][j] == 2:
                score_two += score
            score = 0

    return score_one, score_two


"""
Auxiliary functions to help get_score function.
"""


def horizontal_four(board, i, j):
    return board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3]


def vertical_four(board, i, j):
    return board[i][j] == board[i+1][j] == board[i+2][j] == board[i + 3][j]


def diagonal_four(board, i, j, east):
    if east:
        return board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]
    return board[i][j] == board[i - 1][j - 1] == board[i - 2][j - 2] == board[i - 3][j - 3]