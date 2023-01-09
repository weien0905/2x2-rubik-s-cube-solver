"""
Find the optimal solution of 2x2 Rubik's cube using Breadth-First Search
"""

import copy

W = "W"
G = "G"
R = "R"
O = "O"
Y = "Y"
B = "B"

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class QueueFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

def result(state, action):
    if action not in ["R", "R'", "B", "B'", "D", "D'"]:
        raise Exception("Invalid action")

    result = copy.deepcopy(state)

    if action == "R":
        tmp = (result[1][1], result[1][3])
        result[1][1], result[1][3] = result[2][1], result[2][3]
        result[2][1], result[2][3] = result[3][1], result[3][3]
        result[3][1], result[3][3] = result[5][2], result[5][0]
        result[5][0], result[5][2] = tmp[1], tmp[0]

        tmp = result[4][0]
        result[4][0] = result[4][2]
        result[4][2] = result[4][3]
        result[4][3] = result[4][1]
        result[4][1] = tmp

    elif action == "R'":
        tmp = (result[1][1], result[1][3])
        result[1][1], result[1][3] = result[5][2], result[5][0]
        result[5][0], result[5][2] = result[3][3], result[3][1]
        result[3][1], result[3][3] = result[2][1], result[2][3]
        result[2][1], result[2][3] = tmp[0], tmp[1]

        tmp = result[4][0]
        result[4][0] = result[4][1]
        result[4][1] = result[4][3]
        result[4][3] = result[4][2]
        result[4][2] = tmp

    elif action == "B":
        tmp = (result[1][0], result[1][1])
        result[1][0], result[1][1] = result[4][1], result[4][3]
        result[4][1], result[4][3] = result[3][3], result[3][2]
        result[3][2], result[3][3] = result[0][0], result[0][2]
        result[0][0], result[0][2] = tmp[1], tmp[0]

        tmp = result[5][0]
        result[5][0] = result[5][2]
        result[5][2] = result[5][3]
        result[5][3] = result[5][1]
        result[5][1] = tmp

    elif action == "B'":
        tmp = (result[1][0], result[1][1])
        result[1][0], result[1][1] = result[0][2], result[0][0]
        result[0][0], result[0][2] = result[3][2], result[3][3]
        result[3][2], result[3][3] = result[4][3], result[4][1]
        result[4][1], result[4][3]= tmp[0], tmp[1]

        tmp = result[5][0]
        result[5][0] = result[5][1]
        result[5][1] = result[5][3]
        result[5][3] = result[5][2]
        result[5][2] = tmp

    elif action == "D":
        tmp = (result[0][2], result[0][3])
        result[0][2], result[0][3] = result[5][2], result[5][3]
        result[5][2], result[5][3] = result[4][2], result[4][3]
        result[4][2], result[4][3] = result[2][2], result[2][3]
        result[2][2], result[2][3] = tmp[0], tmp[1]

        tmp = result[3][0]
        result[3][0] = result[3][2]
        result[3][2] = result[3][3]
        result[3][3] = result[3][1]
        result[3][1] = tmp

    elif action == "D'":
        tmp = (result[0][2], result[0][3])
        result[0][2], result[0][3] = result[2][2], result[2][3]
        result[2][2], result[2][3] = result[4][2], result[4][3]
        result[4][2], result[4][3] = result[5][2], result[5][3]
        result[5][2], result[5][3] = tmp[0], tmp[1]

        tmp = result[3][0]
        result[3][0] = result[3][1]
        result[3][1] = result[3][3]
        result[3][3] = result[3][2]
        result[3][2] = tmp

    return result

def goal(state):
    return True if all(len(set(row)) == 1 for row in state) else False

def solve(cube):
    num_explored = 0

    start = Node(state=cube, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = []

    while True:
        if frontier.empty():
            print("No solution")
            return

        node = frontier.remove()
        explored.append(node.state)

        for action in ["R", "R'", "B", "B'", "D", "D'"]:
            num_explored += 1
            state = result(node.state, action)

            if goal(state):
                solution = []
                while node.parent is not None:
                    solution.append(node.action)
                    node = node.parent
                solution.reverse()
                solution.append(action)
                print("Number explored:", num_explored)
                print("Solution: ", end="")
                for step in solution:
                    print(step, end=" ")
                return

            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)
