import array


# --------------------------------- Helping functions ---------------------------------
# swap 2 elements in array
def swap(arr, a, b):
    temp = arr[a]
    arr[a] = arr[b]
    arr[b] = temp


# convert state to array , define the index of zero
# return zero index and state array
def getIndOfZero(state):
    arr = array.array('i', [])
    indexOfZero = 0
    for i in range(0, 9):
        arr.append(int(state % 10))
        state /= 10
        if arr[i] == 0 or arr[i] == 9:
            indexOfZero = 8 - i
    arr[8 - indexOfZero] = 9  # replace 0 with 9 to make calculations easier
    arr.reverse()
    return indexOfZero, arr


# ---------------------------------- Core functions -----------------------------------
# get a new state from current state and action
def newState(state, action):
    indexOfZero, arr = getIndOfZero(state)
    if action == 0:  # Move up
        swap(arr, indexOfZero, indexOfZero - 3)
    elif action == 1:  # Move down
        swap(arr, indexOfZero, indexOfZero + 3)
    elif action == 2:  # Move right
        swap(arr, indexOfZero, indexOfZero + 1)
    elif action == 3:  # Move down
        swap(arr, indexOfZero, indexOfZero - 1)
    state = 0
    arr.reverse()
    for i in range(0, 9):
        state += arr[i] * pow(10, i)
    return int(state)


# check if action is valid or not
def validAction(state, action):
    indexOfZero, arr = getIndOfZero(state)
    if (action == 0 and 0 <= indexOfZero - 3 <= 8) or (action == 1 and 0 <= indexOfZero + 3 <= 8) or (
            action == 2 and 0 <= indexOfZero + 1 <= 8 and (indexOfZero + 1) % 3 != 0) or (
            action == 3 and 0 <= indexOfZero - 1 <= 8 and (indexOfZero) % 3 != 0):
        return True
    else:
        return False


# -------------------------------------  Classes ---------------------------------------

class Node:
    def __init__(self, state, parent=None, action=None, depth = 0):
        self.state = state  # int
        self.parent = parent  # node
        self.action = action  # 0 .. 3 ..0 up , 1 down ,2 right , 3 left
        self.depth = depth
        
def solution(final_node):
    explored = 0
    states = []
    actions = []
    curr_node = final_node
    while curr_node.parent is not None:
        explored += 1
        states.append(curr_node.state)
        actions.append(curr_node.action)
        curr_node = curr_node.parent
    states.append(curr_node.state)
    actions.append(-1)
    states.reverse()
    actions.reverse()
    # print("states: " + str(states))
    for i in range(len(actions)):
        if actions[i] == 0:  # Move up
            actions[i] = "UP"
        elif actions[i] == 1:  # Move down
            actions[i] = "DOWN"
        elif actions[i] == 2:  # Move right
            actions[i] = "RIGHT"
        elif actions[i] == 3:  # Move down
            actions[i] = "LIFT"
        elif actions[i] == -1:  # Move down
            actions[i] = "Intial state"
    # print("actions: " + str(actions))
    return explored, states, actions
