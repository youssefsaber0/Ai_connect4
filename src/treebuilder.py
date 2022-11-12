"""
Constructs a tree in an in-order ordering.
Arguments:
    root: the root node of the tree.
Returns:
    tree representation.
"""

tree = []   # This array contains the tree nodes in an in-order way.


def construct_tree(root):
    if root is None:
        return
    for i in range(len(root.children)):
        construct_tree(root.children[i])
    tree.append(root)
