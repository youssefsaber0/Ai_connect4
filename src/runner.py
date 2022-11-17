from agent import apply_algorithm
from bitoperations import play as do, bits_to_matrix as convert, get_score, check_end
from node import Node
from gmpy2 import xmpz
import treebuilder

"""
All the code here is for testing purposes.
"""


def input(col,current_state,heuristic,max_depth,pruning):
    """
    TODO: Take user input (col#), Perform the move and return the state.
    Hint: Use the treebuilder.py. use construct_tree(root) and the tree is saved within the class.
    Hint: Do not forget to clear the tree when drawing a new one. use treebuilder.tree.clear().

    :parameter: col                 (int)
    :parameter: current_state       (xmpz)
    :parameter: user_turn           (int)
    :parameter: heuristic           (boolean)
    :parameter: maximum_depth       (int)
    :parameter: pruning             (boolean)
    :parameter: ai_only             (boolean)

    :return: next_state             (xmpz)
    """

    """
    User Inputs.
    """
    col = None  # Store user input here
    current_state = None  # Store current state here
    heuristic = None  # Store chosen heuristic here
    max_depth = None  # Store maximum depth here
    pruning = None  # Store pruning here
    ai_only = None  # Store whether the user wants the game to be played between 2 AI agents or not.

    # Perform the move
    valid, next_state = do(col, xmpz(current_state), 0)
    if valid:
        play(next_state, heuristic, max_depth, pruning, ai_only)
    else:
        input()  # Ask the user for a valid move.
    return int(next_state), get_score(next_state)


def print_board(state):
    board = convert(state)
    for i in range(len(board) - 1, -1, -1):
        print(board[i])


def play(current_state, heuristic, max_depth, pruning, ai_only):
    root = Node([], 1, current_state, None)
    if pruning:
        alpha = float('-inf')
        beta = float('inf')

    if ai_only:
        states = []

    while True:
        apply_algorithm(heuristic, root, max_depth, pruning, alpha, beta)

        # Now the root is modified.
        for i in range(len(root.children)):
            if root.value is root.children[i].value:
                valid, state = do(root.children[i].action, root.state, root.turn)
                if valid:
                    print("Player Turn = " + str(root.turn) + ", State = " + str(state))
                    print_board(state)
                    root = Node([], root.children[i].turn, root.children[i].state)
                    heuristic = not heuristic
                    break

        if check_end(state):
            break

        if not ai_only:
            return state

        states.append(state)


# Test Case
play(xmpz(), True, 5, True, True)
