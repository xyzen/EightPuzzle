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
        divisor = self.rows * self.cols
        for row in range(self.rows):
            state.append([])
            for col in range(self.cols):
                state[row].append(temp % divisor)
                temp = temp // divisor
        return tuple([tuple(row) for row in state])
        
    def stateToUID(self, state):
        val = 0
        base = self.rows * self.cols
        for i in range(0, self.rows*self.cols):
            val += state[i//self.rows][i%self.rows]*base**i
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

    def resetZero(self, state):
        row, col = self.sim.findLabel(state, 0)
        while col < (self.cols - 1):
            state = self.sim.move(state, row, col + 1)
            col += 1
        while row < (self.rows - 1):
            state = self.sim.move(state, row + 1, col)
            row += 1
        return state

    def countParity(self, state):
        state = self.resetZero(state)
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                label_c = self.sim.solved[row][col]
                row_c, col_c = self.sim.findLabel(state, label_c)
                if (row_c, col_c) == (row, col) :
                    continue
                state = self.swap(state, row_c, col_c, row, col)
                count += 1
        return count

    def swap(self, state, row1, col1, row2, col2):
        new_state = [[val for val in row] for row in state]
        new_state[row1][col1] = state[row2][col2]
        new_state[row2][col2] = state[row1][col1]
        return tuple([tuple(row) for row in new_state])

    def solve(self, state):
        check_state = state
        if self.countParity(check_state) % 2 == 1:
            return "No solution."
        return self.AStarSearch(state)

    def readInput(self, path : str):
        chars = []
        with open(path) as file:
            for char in file.read():
                if char.isdigit():
                    chars.append(char)
        states = []
        new_state = [[0 for row in range(self.rows)] for col in range(self.cols)]
        num_items = self.rows * self.cols
        for counter in range(len(chars)//num_items):
            for row in range(self.rows):
                for col in range(self.cols):
                    new_state[row][col] = int(chars[num_items*counter + self.cols*row + col])
            states.append(tuple([tuple(r) for r in new_state]))
        return states

    def solveInput(self, input_path : str, output_path : str):
        states = self.readInput(input_path)
        solutions = [self.solve(state) for state in states]
        self.writeOutput(solutions, output_path)

    def writeOutput(self, solutions : list, path : str):
        with open(path, 'w') as file:
            for solution in solutions:
                file.write(solution + "\n\n")

if __name__ == "__main__":
    from EightPuzzleGUI import EightPuzzle
    EightPuzzle().solver.solveInput("program_1_data.txt", "program_1_solutions.txt")
