#!/usr/bin/env python
"""
Name of the author(s):
- Hadrien Allegaert   <hadrien.allegaert@student.uclouvain.be>
- Alexandre Caro
"""
import time
import sys
from copy import deepcopy
from search import *


#################
# Problem class #
#################
class TowerSorting(Problem):
    
    def actions(self, state):
        moves = {}
        for i in range(state.number):
            for j in range(state.number):
                if i != j  and len(state.grid[j]) < state.size:
                    moves[(i,j)] = 0 # use key to value, because of usage as list but no real improvement
        return moves
       

    def result(self, state, action):
        new_grid = deepcopy(state.grid)
        src, target = action
        new_grid[target].append(new_grid[src].pop())
        return State(state.number, state.size, grid=new_grid, move=f'tower{src} -> tower{target}')

    def goal_test(self, state):
        second = False
        for row in state.grid:
            length = len(row)
            # if their is more than one tower with less than SIZE token
            # to understand this, take the simple case 3 towers 3 tokens (2 colors), 
            # if their is two towers with 2 tokens or less it's enough to conclude a NO GOAL 
            if length != state.size:
                if second: 
                    return False
                else:
                    second = True
                    continue
            # avoid empty row because state.size != 0
            # compare only full row, because you need full rows to complete the game
            else: 
                # compare elem in a same row to the first, if one differe, we reject
                first = row[0]
                for i in range(1, length):
                    if row[i] != first:
                        return False
        return True 


###############
# State class #
###############
class State:

    def __init__(self, number, size, grid, move="Init"):
        self.number = number #number of row
        self.size = size  # number of places in a row
        self.grid = grid
        self.move = move
        self.hash = hash(str(grid))

    def __str__(self):
        s = self.move + "\n"
        for i in reversed(range(self.size)):
            for tower in self.grid:
                if len(tower) > i:
                    s += "".join(tower[i]) + " "
                else:
                    s += ". "
            s += "\n"
        return s

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash

######################
# Auxiliary function #
######################
def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    number_tower, size_tower = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = [[] for i in range(number_tower)]
    for row in lines[1:size_tower+1]:
        elems = row.split(" ")
        for index in range(number_tower):
            if elems[index] != '.':
                initial_grid[index].append(elems[index])

    for tower in initial_grid:
        tower.reverse()

    return number_tower, size_tower, initial_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./sort_tower.py <path_to_instance_file>")
    filepath = sys.argv[1]

    number, size, initial_grid = read_instance_file(filepath)

    init_state = State(number, size, initial_grid, "Init")
    problem = TowerSorting(init_state)
    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)
