"""
This file represents the node class.
"""


class Node:
    def __init__(self, children, turn, state, action=None, value=None):
        self.children = children
        self.turn = turn
        self.state = state
        self.action = action
        self.value = value
