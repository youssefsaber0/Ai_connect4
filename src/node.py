"""
This file represents the node class.
"""


class Node:
    def __init__(self, parent, turn, state, value=None):
        self.parent = parent
        self.turn = turn
        self.state = state
        self.value = value
