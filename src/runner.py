from agent import apply_algorithm
from bitoperations import play as do, bits_to_matrix as convert, get_score, check_end
from node import Node
from gmpy2 import xmpz
import treebuilder

"""
All the code here is for testing purposes.
"""

def input():
    """
    TODO: Take user input (col#), Perform the move and return the state.
    Hint: Use the treebuilder.py. use construct_tree(root) and the tree is saved within the class.
    Hint: Do not forget to clear the tree when drawing a new one. use treebuilder.tree.clear()
    :return: the new state
    """

def print_board(state):
    board = convert(state)
    for i in range(len(board)-1, -1, -1):
        print(board[i])


def play():
    root = Node([], 0, xmpz(), None)
    heuristic = True
    pruning = True
    max_depth = 5
    alpha = float('-inf')
    beta = float('inf')

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

    print("Game ended. Board is displayed below.")
    print(state)
    print(get_score(state))


play()
