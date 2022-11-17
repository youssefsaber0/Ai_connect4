import math
from Node import Node, newState, validAction
import heapq
# --------------------------------- Array of goal position ---------------------------------
# used in heuristics calculation
goalPosition = {
    "9": [0, 0], "1": [0, 1], "2": [0, 2],
    "3": [1, 0], "4": [1, 1], "5": [1, 2],
    "6": [2, 0], "7": [2, 1], "8": [2, 2],
    "0": [0, 0]
}
# --------------------------------- Helping class in A star search ---------------------------------
# use to keep track of important functions


class Node_state:
    def __init__(self, node=None):
        self.node = node
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.node.state == other.node.state

    def __cmp__(self, other):
        return self.f < other.f

    def __lt__(self, other):
        return self.f < other.f
def manhattan_distance(current_x, current_y, number):
    if number=="0" or number=="9":
        return 0
    goal_x = goalPosition[number][0]
    goal_y = goalPosition[number][1]
    return abs(current_x - goal_x) + abs(current_y - goal_y)


def euclidean_distance(current_x, current_y, number):
    if number=="0" or number=="9":
        return 0
    goal_x = goalPosition[number][0]
    goal_y = goalPosition[number][1]
    return math.sqrt((current_x - goal_x)**2 + (current_y - goal_y)**2)


def heuristics(state, function):
    str_state = str(state)
    h = 0
    for i in range(0, len(str_state)):
        current_x = math.floor(i / 3)
        current_y = i % 3
        h += function(current_x, current_y, str_state[i])
    return h
    
def A_star(start_node, function= "manhattan_distance"):
    # keep track of new states that will be visit
    open = []
    max_depth=0
    start = Node_state(node=start_node)
    # set heuristic function to one of two required functions
    h_func = manhattan_distance if function == "manhattan_distance" else euclidean_distance
    start.h = heuristics(start.node.state, h_func)
    start.f = start.h
    heapq.heappush(open, start)
    # keep track of visited nodes
    visited = set()
    while len(open) > 0:
        current = heapq.heappop(open)
        if current.node.state in visited:
            continue
        visited.add(current.node.state)

        if current.node.depth > max_depth:
            max_depth = current.node.depth
        # check if goal reached
        if current.node.state == 912345678:
            return current.node, len(visited), max_depth
        # check all successor
        for i in range(0, 4):
            if validAction(current.node.state, i):
                new_state = newState(current.node.state, i)
                # print("i " + str(new_state)+" "+str(i))
                new_child = Node(parent=current.node,
                                 action=i, state=new_state)
                node_state = Node_state(new_child)
                node_state.h = heuristics(new_state, h_func)
                node_state.node.depth = current.node.depth + 1
                node_state.f = node_state.h + node_state.node.depth
                flag = False
                # check if visited or in open list if true didn't add it to open list
                if node_state.node.state in visited:
                    continue

                heapq.heappush(open, node_state)
    return None, None, None