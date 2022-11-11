from BitOperations import play, check_end, calculate_final_score, heuristic
from node import Node

"""
This file represents the agent playing against the player.
    The class should implement:
        - Minimax algorithm without pruning.
        - Minimax algorithm with pruning.
"""

leaf_nodes = []

# Function to apply the minimax algorithm without pruning
def minimax(turn, state, depth):
    best_move = None
    if check_end(state):
        return calculate_final_score(state)
    if depth == 0:
        # TODO: HEURISTIC FUNCTION IS YET TO BE IMPLEMENTED
        return heuristic(state)

    # Player turn decides whether the function is max (turn = 0) or min (turn = 1).
    if turn == 0:
        value = float('-inf')
        for i in range(7):
            next_state = play(i, state, 0)
            if value < minimax(1, next_state, depth - 1):
                best_move = next_state
                value = minimax(1, next_state, depth - 1)
        return value, best_move
    else:
        value = float('inf')
        for i in range(7):
            next_state = play(i, state, 1)
            if value > minimax(0, next_state, depth - 1):
                best_move = next_state
                value = minimax(0, next_state, depth - 1)
        return value, best_move

# Function to apply the minimax algorithm with pruning.
def pruningminimax(turn, state, depth, alpha, beta):
    best_move = None
    if check_end(state):
        return calculate_final_score(state)
    if depth == 0:
        # TODO: HEURISTIC FUNCTION IS YET TO BE IMPLEMENTED
        return heuristic(state)

    if turn == 0:
        value = float('-inf')
        for i in range(7):
            next_state = play(i, state, 0)
            if value < pruningminimax(1, next_state, depth - 1, alpha, beta):
                best_move = next_state
                value = pruningminimax(1, next_state, depth - 1, alpha, beta)
            if beta < value:
                return value
            alpha = max(alpha, value)
        return value, best_move
    else:
        value = float('inf')
        for i in range(7):
            next_state = play(i, state, 1)
            if value > pruningminimax(0, next_state, depth - 1, alpha, beta):
                best_move = next_state
                value = pruningminimax(0, next_state, depth - 1, alpha, beta)
            if alpha > value:
                return value
            beta = min(beta, value)
        return value, best_move


# Function to apply the minimax algorithm without pruning on a tree of nodes
def minimax(root, depth):
    # If encountered any terminal case, add the child to the leaf nodes
    if check_end(root.state):
        leaf_nodes.append(root)
        return calculate_final_score(root.state)
    if depth == 0:
        leaf_nodes.append(root)
        # TODO: HEURISTIC FUNCTION IS YET TO BE IMPLEMENTED
        return heuristic(root.state)

    # Player turn decides whether the function is max (turn = 0) or min (turn = 1).
    if root.turn == 0:
        root.value = float('-inf')
        for i in range(7):
            valid, next_state = play(i, root.state, 0)
            child = Node(root, 1, next_state)
            child.value = max(root.value, minimax(child, depth - 1))
        return child.value
    else:
        root.value = float('inf')
        for i in range(7):
            valid, next_state = play(i, root.state, 1)
            child = Node(root, 0, next_state)
            child.value = min(root.value, minimax(child, depth - 1))
        return child.value


# Functions to apply the minimax algorithm with pruning on a tree of nodes
def pruningminimax(root, depth, alpha, beta):
    if check_end(root.state):
        leaf_nodes.append(root)
        return calculate_final_score(root.state)
    if depth == 0:
        leaf_nodes.append(root)
        # TODO: HEURISTIC FUNCTION IS YET TO BE IMPLEMENTED
        return heuristic(root.state)

    if root.turn == 0:
        root.value = float('-inf')
        for i in range(7):
            valid, next_state = play(i, root.state, 0)
            child = Node(root, 1, next_state)
            child.value = max(root.value, pruningminimax(child, depth - 1, alpha, beta))
            if beta < child.value:
                return child.value
            alpha = max(alpha, child.value)
        return child.value
    else:
        root.value = float('inf')
        for i in range(7):
            valid, next_state = play(i, root.state, 1)
            child = Node(root, 0, next_state)
            child.value = min(root.value, pruningminimax(child, depth - 1, alpha, beta))
            if alpha > child.value:
                return child.value
            beta = min(beta, child.value)
        return child.value
