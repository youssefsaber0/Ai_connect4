from agent import apply_algorithm
from bitoperations import play as do, bits_to_matrix as convert, get_score, check_end
from node import Node
from gmpy2 import xmpz
import treebuilder

"""
All the code here is for testing purposes.
"""


def play():
    root = Node([], 0, xmpz())
    heuristic = True
    pruning = True
    alpha = float('-inf')
    beta = float('inf')

    while True:
        apply_algorithm(heuristic, root, 4, pruning, alpha, beta)

        # Now the root is modified.
        for i in range(len(root.children)):
            if root.value is root.children[i].value:
                valid, state = do(i, root.state, root.turn)
                if valid:
                    print(state)
                root = Node([], root.children[i].turn, root.children[i].state)
                heuristic = not heuristic
                break

        board = convert(state)
        for i in range(len(board) - 1, -1, -1):
            print(board[i])

        if check_end(state):
            break

    board = convert(state)
    for i in range(len(board) - 1, -1, -1):
        print(board[i])
    print(get_score(state))


play()

# root1 = Node([], 0, xmpz(), None)
# apply_algorithm(True, root1, 1, False)
# root2 = Node([], 0, xmpz(), None)
# apply_algorithm(False, root2, 1, False)
#
#
# print(root1.value)
# print(len(root1.children))
#
# for i in range(len(root1.children)):
#     print(root1.children[i].value)
#     print(root1.children[i].turn)
#     print(root1.children[i].state)
#     print()
#
# print("###########################")
# print()
#
# print(root2.value)
# print(len(root2.children))
# for i in range(len(root2.children)):
#     print(root2.children[i].value)
#     print(root2.children[i].turn)
#     print(root2.children[i].state)
#     print()
#
# treebuilder.construct_tree(root1)
# for i in range(len(treebuilder.tree)):
#     print(str(treebuilder.tree[i].value), end=", ")
# treebuilder.tree.clear()
#
# print()
#
# treebuilder.construct_tree(root2)
# for i in range(len(treebuilder.tree)):
#     print(str(treebuilder.tree[i].value), end=", ")
# treebuilder.tree.clear()
