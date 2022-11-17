"""
Constructs a tree in a pre-order motive.
Arguments:
    root: the root node of the tree.
Returns:
    tree representation.
"""


def construct_tree(root):
    tree = []
    preorder(tree, root)
    return tree


def preorder(tree, root):
    if root is None:
        return
    tree.append(root)
    for i in range(len(root.children)):
        preorder(tree, root.children[i])
