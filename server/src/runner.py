import time
import sys

from src.agent import apply_algorithm
from src.bitoperations import play as do, bits_to_matrix as convert, get_score, check_end
from src.node import Node
from gmpy2 import xmpz
from src.treebuilder import construct_tree

"""
Main runner and tester.
"""


def input(col, current_state, max_depth, heuristic=True, pruning=False, ai_only=False):
    """
    :parameter: col                 (int)
    :parameter: current_state       (xmpz)
    :parameter: user_turn           (int)
    :parameter: maximum_depth       (int)
    :parameter: heuristic           (boolean)
    :parameter: pruning             (boolean)
    :parameter: ai_only             (boolean)

    :return: next_state             (xmpz)
    """

    # Perform the move
    valid, next_state = do(int(col), xmpz(current_state), 0)
    if valid:
        next_state, action = play(next_state, heuristic, max_depth, pruning, ai_only)
    else:
        input()  # Ask the user for a valid move.
    return int(next_state), action, get_score(next_state)


def print_board(state):
    board = convert(state)
    for i in range(len(board) - 1, -1, -1):
        print(board[i])


def play(current_state, heuristic, max_depth, pruning, ai_only):
    alpha = float('-inf')
    beta = float('inf')

    if not ai_only:  # Player vs AI mode
        root = Node([], 1, current_state, None)
        apply_algorithm(heuristic, root, max_depth, pruning, alpha, beta)

        tree = construct_tree(root)
        print("THE PRE-ORDERED TREE:")
        for i in range(len(tree)):
            if i != len(tree) - 1:
                print(tree[i].value, end=', ')
            else:
                print(tree[i].value, end='\n')

        for i in range(len(root.children)):
            if root.value is root.children[i].value:
                return root.children[i].state, root.children[i].action

    else:  # AI only mode
        if pruning:
            sys.stdout = open('with-pruning.txt', 'w')
        else:
            sys.stdout = open('without-pruning.txt', 'w')
        states = []

        root = Node([], 0, current_state, None)
        while True:
            start = time.time()

            if check_end(root.state):
                sys.stdout.close()
                return states

            expansions = apply_algorithm(heuristic, root, max_depth, pruning, alpha, beta)

            for i in range(len(root.children)):
                if root.value is root.children[i].value:
                    states.append(root.children[i].state)
                    root = Node([], root.children[i].turn, root.children[i].state)
                    heuristic = not heuristic
                    break

            print(str(expansions.expansions) + ', ' + str(time.time() - start))


# if __name__ == "__main__":
    # play(xmpz(), True, 5, True, True)
    # play(xmpz(), True, 5, True, True)
    # play(xmpz(), True, 5, False, True)
