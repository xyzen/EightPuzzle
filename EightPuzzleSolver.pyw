from queue import PriorityQueue

rows = 3
cols = 3

solved = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0),
)

label_pos = dict()
for row in range(rows):
    for col in range(cols):
        label_pos[solved[row][col]] = (row, col)

def uidToState(uid):
    state = [[0 for row in range(rows)] for col in range(cols)]
    temp = int(uid)
    for row in range(rows):
        for col in range(cols):
            state[row][col] = temp % 9
            temp = temp // 9
    return tuple([tuple(row) for row in state])
    
def stateToUID(state):
    val = 0
    for i in range(0, rows*cols):
        val += state[i//rows][i%rows]*9**i
    return val
    
solved_uid = stateToUID(solved)

def findZero(state):
    for row in range(rows):
        for col in range(cols):
            if state[row][col] == 0:
                return row, col

def move(state, row, col):
    new_state = [list(row) for row in state]
    row_e, col_e = findZero(state)
    if abs(row - row_e) + abs(col - col_e) != 1:
        return
    
    label = state[row][col]
    new_state[row_e][col_e] = label
    new_state[row][col] = 0
    
    return tuple([tuple(row) for row in new_state])

def successors(state):
    next_states = dict()
    for row in range(rows):
        for col in range(cols):
            new_state = move(state, row, col)
            if new_state != None:
                label = str(state[row][col])
                next_states[label] = new_state
    return next_states

def manhattanDist(state, row, col):
    label = state[row][col]
    if label == 0: return 0
    row_c, col_c = label_pos[label]
    return abs(row - row_c) + abs(col - col_c)

def heuristic(state):
    val = 0
    for row in range(rows):
        for col in range(cols):
            val += manhattanDist(state, row, col)
    return val

def AStarSearch(state):
    fringe = PriorityQueue()
    fringe.put(tuple([heuristic(state), 0, str(), stateToUID(state)]))
    visited = set()
    while fringe.qsize():
        parent = fringe.get()
        p_cost, p_path, p_uid = parent[1:]
        if p_uid == solved_uid:
            return p_path
        if p_uid in visited:
            continue
        visited.add(p_uid)
        p_state = uidToState(p_uid)
        for c_label, c_state in successors(p_state).items():
            c_cost = p_cost + 1
            f_cost = c_cost + heuristic(c_state)
            c_path = p_path + c_label + " "
            c_uid  = stateToUID(c_state)
            child = tuple([f_cost, c_cost, c_path, c_uid])
            fringe.put(child)
    return "No solution."
