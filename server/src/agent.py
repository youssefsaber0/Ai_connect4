from bitoperations import play, check_end, get_score
from node import Node
from heuristics import heuristic_one, heuristic_two

"""
This file represents the agent playing against the player.
    The class should implement:
        - Minimax algorithm without pruning.
        - Minimax algorithm with pruning.
        
The main runner of this file is apply_algorithm.
    Arguments:
        heuristic: the heuristic to be applied as we have 2 heuristics.
        root: the root of the tree.
        depth: the maximum depth.
        pruning: apply pruning or not.
        alpha (optional): the alpha value if pruning is applied.
        beta (optional): the beta value if pruning is applied.
    Returns:
        Minimax tree with weighted values.
"""


def apply_algorithm(heuristic, root, depth, pruning, alpha=None, beta=None):
    if heuristic and pruning:
        pruning_minimax(heuristic_one, root, depth, alpha, beta)
    elif heuristic and not pruning:
        minimax(heuristic_one, root, depth)
    elif not heuristic and pruning:
        pruning_minimax(heuristic_two, root, depth, alpha, beta)
    else:
        minimax(heuristic_two, root, depth)


# Function to apply the minimax algorithm without pruning on a tree of nodes
def minimax(heuristic, root, depth):
    # If encountered any terminal case, add the child to the leaf nodes
    if check_end(root.state):
        score_one, score_two = get_score(root.state)
        return score_one - score_two
    if depth == 0:
        return heuristic(root.state)

    # Player turn decides whether the function is max (turn = 0) or min (turn = 1).
    if root.turn == 0:
        root.value = float('-inf')
        valid_moves = 7
        # 0 --> 6
        for i in range(7):
            valid, next_state = play(i, root.state, 0)
            if valid:
                root.children.append(Node([], 1, next_state, i))
                root.children[len(root.children)-1].value = max(root.value,
                                                                minimax(heuristic,
                                                                        root.children[len(root.children)-1],
                                                                        depth - 1))
            else:
                valid_moves -= 1
        for i in range(len(root.children)):
            root.value = max(root.value, root.children[i].value)
        return root.value
    else:
        root.value = float('inf')
        valid_moves = 7
        for i in range(7):
            valid, next_state = play(i, root.state, 1)
            if valid:
                root.children.append(Node([], 0, next_state, i))
                root.children[len(root.children)-1].value = min(root.value,
                                                                minimax(heuristic,
                                                                        root.children[len(root.children)-1],
                                                                        depth - 1))
            else:
                valid_moves -= 1
        for i in range(len(root.children)):
            root.value = min(root.value, root.children[i].value)
        return root.value


# Functions to apply the minimax algorithm with pruning on a tree of nodes
def pruning_minimax(heuristic, root, depth, alpha, beta):
    if check_end(root.state):
        score_one, score_two = get_score(root.state)
        return score_one - score_two
    if depth == 0:
        return heuristic(root.state)

    if root.turn == 0:
        root.value = float('-inf')
        valid_moves = 7
        for i in range(valid_moves):
            valid, next_state = play(i, root.state, 0)
            if valid:
                root.children.append(Node([], 1, next_state, i))
                root.children[len(root.children) - 1].value = max(root.value,
                                                                  pruning_minimax(heuristic,
                                                                                  root.children[len(root.children) - 1],
                                                                                  depth - 1, alpha, beta))
                if beta < root.children[len(root.children)-1].value:
                    return root.children[len(root.children)-1].value
                alpha = max(alpha, root.children[len(root.children)-1].value)
            else:
                valid_moves -= 1
        for i in range(len(root.children)):
            root.value = max(root.value, root.children[i].value)
        return root.value
    else:
        root.value = float('inf')
        valid_moves = 7
        for i in range(valid_moves):
            valid, next_state = play(i, root.state, 1)
            if valid:
                root.children.append(Node([], 0, next_state, i))
                root.children[len(root.children) - 1].value = min(root.value,
                                                                  pruning_minimax(heuristic,
                                                                                  root.children[len(root.children)-1],
                                                                                  depth - 1, alpha, beta))
                if alpha > root.children[len(root.children)-1].value:
                    return root.children[len(root.children)-1].value
                beta = min(beta, root.children[len(root.children)-1].value)
            else:
                valid_moves -= 1
        for i in range(len(root.children)):
            root.value = min(root.value, root.children[i].value)
        return root.value


# Function to apply the minimax algorithm without pruning. (This is not used)
def minmax(turn, state, depth):
    best_move = None
    if check_end(state):
        return get_score(state)
    if depth == 0:
        return heuristic_one(state)

    # Player turn decides whether the function is max (turn = 0) or min (turn = 1).
    if turn == 0:
        value = float('-inf')
        for i in range(7):
            next_state = play(i, state, 0)
            if value < minmax(1, next_state, depth - 1):
                best_move = next_state
                value = minmax(1, next_state, depth - 1)
        return value, best_move
    else:
        value = float('inf')
        for i in range(7):
            next_state = play(i, state, 1)
            if value > minmax(0, next_state, depth - 1):
                best_move = next_state
                value = minmax(0, next_state, depth - 1)
        return value, best_move


# Function to apply the minimax algorithm with pruning. (This is not used)
def pruning_minmax(turn, state, depth, alpha, beta):
    best_move = None
    if check_end(state):
        return get_score(state)
    if depth == 0:
        return heuristic_one(state)

    if turn == 0:
        value = float('-inf')
        for i in range(7):
            next_state = play(i, state, 0)
            if value < pruning_minmax(1, next_state, depth - 1, alpha, beta):
                best_move = next_state
                value = pruning_minmax(1, next_state, depth - 1, alpha, beta)
            if beta < value:
                return value
            alpha = max(alpha, value)
        return value, best_move
    else:
        value = float('inf')
        for i in range(7):
            next_state = play(i, state, 1)
            if value > pruning_minmax(0, next_state, depth - 1, alpha, beta):
                best_move = next_state
                value = pruning_minmax(0, next_state, depth - 1, alpha, beta)
            if alpha > value:
                return value
            beta = min(beta, value)
        return value, best_move
