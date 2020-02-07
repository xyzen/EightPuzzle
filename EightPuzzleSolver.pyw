from queue import PriorityQueue

class Solver():

    rows = cols = 3
    
    def __init__(self, sim, solved):
        self.sim = sim
        self.goal_uid = self.stateToUID(solved)
        self.label_pos = dict()
        for row in range(self.rows):
            for col in range(self.cols):
                self.label_pos[solved[row][col]] = (row, col)
    
    def uidToState(self, uid):
        state = []
        temp = int(uid)
        for row in range(self.rows):
            state.append([])
            for col in range(self.cols):
                state[row].append(temp % 9)
                temp = temp // 9
        return tuple([tuple(row) for row in state])
        
    def stateToUID(self, state):
        val = 0
        for i in range(0, self.rows*self.cols):
            val += state[i//self.rows][i%self.rows]*9**i
        return val
    
    def successors(self, state):
        next_states = dict()
        for row in range(self.rows):
            for col in range(self.cols):
                new_state = self.sim.move(state, row, col)
                if new_state:
                    label = str(state[row][col])
                    next_states[label] = new_state
        return next_states
    
    def manhattanDist(self, state, row, col):
        label = state[row][col]
        if label == 0: return 0
        row_c, col_c = self.label_pos[label]
        return abs(row - row_c) + abs(col - col_c)
    
    def heuristic(self, state):
        val = 0
        for row in range(self.rows):
            for col in range(self.cols):
                val += self.manhattanDist(state, row, col)
        return val
    
    def AStarSearch(self, state):
        start_uid = self.stateToUID(state)
        start_path = ""
        start_cost = 0
        h_cost = self.heuristic(state)
        f_cost = start_cost + h_cost
        start = (f_cost, start_cost, start_path, start_uid)
    
        fringe = PriorityQueue()
        fringe.put(start)
        visited = set()
        
        while fringe.qsize():
            parent = fringe.get()
            p_cost, p_path, p_uid = parent[1:]
            if p_uid == self.goal_uid:
                return p_path
            if p_uid in visited:
                continue
            visited.add(p_uid)
            p_state = self.uidToState(p_uid)
            for c_label, c_state in self.successors(p_state).items():
                c_cost = p_cost + 1
                f_cost = c_cost + self.heuristic(c_state)
                c_path = p_path + c_label + " "
                c_uid  = self.stateToUID(c_state)
                child = (f_cost, c_cost, c_path, c_uid)
                fringe.put(child)
        return "No solution."
