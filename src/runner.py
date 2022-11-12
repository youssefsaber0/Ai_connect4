from agent import apply_algorithm
from node import Node
from gmpy2 import xmpz
import treebuilder

"""
All the code here is for testing purposes.
"""

root1 = Node([], 0, xmpz(), None)
apply_algorithm(True, root1, 1, False)
root2 = Node([], 0, xmpz(), None)
apply_algorithm(False, root2, 1, False)


print(root1.value)
print(len(root1.children))

for i in range(len(root1.children)):
    print(root1.children[i].value)
    print(root1.children[i].turn)
    print(root1.children[i].state)
    print()

print("###########################")
print()

print(root2.value)
print(len(root2.children))
for i in range(len(root2.children)):
    print(root2.children[i].value)
    print(root2.children[i].turn)
    print(root2.children[i].state)
    print()

treebuilder.construct_tree(root1)
for i in range(len(treebuilder.tree)):
    print(str(treebuilder.tree[i].value), end=", ")
treebuilder.tree.clear()

print()

treebuilder.construct_tree(root2)
for i in range(len(treebuilder.tree)):
    print(str(treebuilder.tree[i].value), end=", ")
treebuilder.tree.clear()
