"""
This file represents the node class.
"""


class Node:
    def __init__(self, children, turn, state, value=None):
        self.children = children
        self.turn = turn
        self.state = state
        self.value = value
