from Node import Node, newState, validAction


# xfs method determines which method to run according to type passed.
def xfs(type, root):
    if (type == "dfs"):
        return dfs(root, 912345678)
    elif (type == "bfs"):
        return bfs(root, 912345678)
    else:
        return None         # Error protection


# dfs is a function that solves the 8 puzzle using DFS.
def dfs(root, goalState):
    # Establishing our data structures.
    searchdepth = 0
    frontier = []
    sfrontier = set()
    explored = set()
    frontier.append(root)
    sfrontier.add(root)
    # Expand the frontier list till nothing is left.
    while len(frontier) > 0:
        # Traversing the frontier list in a DFS manner.
        current = frontier.pop()
        sfrontier.remove(current)
        if searchdepth < current.depth:
            searchdepth = current.depth
        explored.add(current.state)

        # If goal state reached, return.
        if current.state == goalState:
            return current, len(explored), searchdepth

        # Else, we go down the state tree.
        expand(current, explored, frontier, sfrontier)
    return None, None, None

# bfs is a function that solves the 8 puzzle using BFS.
def bfs(root, goalState):
    # Establishing our data structures.
    searchdepth = 0
    frontier = []
    sfrontier = set()
    explored = set()
    frontier.append(root)
    sfrontier.add(root)
    # Expand the frontier list till nothing is left.
    while len(frontier) > 0:
        # Traversing the frontier list in a DFS manner.
        current = frontier.pop(0)
        sfrontier.remove(current)
        if searchdepth < current.depth:
            searchdepth = current.depth
        explored.add(current.state)

        # If goal state reached, return.
        if current.state == goalState:
            return current, len(explored), searchdepth

        # Else, we go down the state tree.
        expand(current, explored, frontier, sfrontier)
    return None, None,None

# expand function is used to expand a node in the frontier list and
# add its successors to the frontier list. 
def expand(current, explored, frontier, sfrontier):
    for action in range(3, -1, -1):  # Check up, right, down and left actions if valid
        if validAction(current.state, action):
            # If the action is valid, set up the next state.
            nextState = newState(current.state, action)
            nextNode = Node(
                parent = current,
                action = action,
                state = nextState,
                depth = current.depth + 1
            )

            # Check if the new state has been explored or is already in the frontier list.
            if nextState not in explored and nextState not in sfrontier:
                frontier.append(nextNode)
                sfrontier.add(nextNode)

