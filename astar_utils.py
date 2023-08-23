from queue import PriorityQueue
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from matplotlib.colors import ListedColormap

target = ((1, 2, 3),
          (4, 5, 6),
          (7, 8, 0))

def find_blank(grid):
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                return i, j

def get_children(grid):
    children = []
    bx, by = find_blank(grid)
    if bx < 2:
        temp = [list(i) for i in grid]
        temp[bx][by], temp[bx + 1][by] = temp[bx + 1][by], temp[bx][by]
        t = tuple(tuple(i) for i in temp)
        children.append(t)

    if bx > 0:
        temp = [list(i) for i in grid]
        temp[bx][by], temp[bx - 1][by] = temp[bx - 1][by], temp[bx][by]
        t = tuple(tuple(i) for i in temp)
        children.append(t)

    if by < 2:
        temp = [list(i) for i in grid]
        temp[bx][by], temp[bx][by + 1] = temp[bx][by + 1], temp[bx][by]
        t = tuple(tuple(i) for i in temp)
        children.append(t)

    if by > 0:
        temp = [list(i) for i in grid]
        temp[bx][by], temp[bx][by - 1] = temp[bx][by - 1], temp[bx][by]
        t = tuple(tuple(i) for i in temp)
        children.append(t)

    return children

def heuristic_cost(grid, h_i):
    if h_i == 1:  # Uniform Cost Search
        return 0

    if h_i == 2:  # Number of Displaced Tiles
        cost = 0
        for i in range(3):
            for j in range(3):
                if grid[i][j] == 0:
                    continue
                elif grid[i][j] == target[i][j]:
                    continue
                else:
                    cost += 1
        return cost

    if h_i == 3:  # Manhattan Distance
        cost = 0
        for i in range(3):
            for j in range(3):
                if grid[i][j] == 0:
                    continue
                x = int((grid[i][j] - 1) / 3)
                y = (grid[i][j] - 1) % 3
                cost += (abs(x - i) + abs(y - j))
        return cost

    if h_i == 4:  # Euclidean Distance
        cost = 0
        for i in range(3):
            for j in range(3):
                if grid[i][j] == 0:
                    continue
                x = int((grid[i][j] - 1) / 3)
                y = (grid[i][j] - 1) % 3
                cost += np.sqrt((x - i) ** 2 + (y - j) ** 2)
        return cost

def solve_puzzle(grid, h_i):
    # if h_i == 1:
    #     print("Using h1: h(n) = 0")

    # elif h_i == 2:
    #     print("Using h2: h(n) = Number of Tiles Displaced")

    # elif h_i == 3:
    #     print("Using h3: h(n) = Manhattan Cost")

    # elif h_i == 4:
    #     print("Using h4: h(n) = Euclidean Cost")

    bx, by = find_blank(grid)
    open_list = PriorityQueue()
    open_list.put([heuristic_cost(grid, h_i), grid])
    dist = {grid: 0}
    parent = {grid: grid}
    closed_list = set()
    while open_list:
        prior, curr_state = open_list.get()
        if curr_state == target:
            print("Target State reached.")
            print("Total states in optimal path ", dist[target] + 1)
            print("Total number of states explored is ", len(closed_list))

            path = []
            temp = target
            while temp != grid:
                path.insert(0, temp)
                temp = parent[temp]
            path.insert(0, temp)
            for i in path:
                if i == target:
                    continue

            output = {"states_explored": len(closed_list),
                      "optimal_path": path}
            return output

        bx, by = find_blank(curr_state)
        children = get_children(curr_state)
        for i in children:
            i = tuple(tuple(j) for j in i)
            if i not in closed_list and (i not in dist or dist[i] > dist[curr_state] + 1):
                dist[i] = dist[curr_state] + 1
                parent[i] = curr_state
                open_list.put([heuristic_cost(i, h_i) + dist[i], i])

            closed_list.add(curr_state)

    # print("Target State not found.")
    # print("Number of States visited is ", len(closed_list))
    # return
    
def get_inversions(arr):
    inv_count = 0
    empty_value = -1
    for i in range(0, 8):
        for j in range(i + 1, 8):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count

def soln_exists(grid) :
    # Check input validity
    input_list = [j for sub in grid for j in sub]
    
    for i in range(9):
        if i not in input_list:    
            return False
    
    input_list.remove(0)
    
    # Count inversions in given 8 puzzle
    inv_count = get_inversions(input_list)

    # Can't be solved if inversions is odd
    return (inv_count % 2 == 0)


def get_plots(output):
    paths = output['optimal_path']
        
    # plt.rcParams["animation.html"] = "jshtml"
    plt.rcParams["figure.figsize"] = (3, 2)
    plt.rcParams['figure.dpi'] = 150  
    plt.ioff()

    def plot(i):
        fig.clear()
        ax = fig.add_subplot(111)
        my_cmap = ListedColormap(['bisque']).copy()
        my_cmap.set_under('greenyellow')
        sns.heatmap(paths[i], annot = True, annot_kws={"size":10}, cbar = False, linewidths= 3,
                    linecolor='black', cmap= my_cmap, yticklabels=False, xticklabels=False, vmin = 1, ax = ax)
        
        title = str(i+1) + ' out of ' + str(len(paths)) + ' items in optimal path'
        plt.title(title)
        plt.tight_layout()
        
    n_frames = len(paths)
    fig, ax = plt.subplots()

    anim = animation.FuncAnimation(fig, plot, frames = n_frames, interval = 1000)
    
    return anim


        # sns.heatmap(paths[i], mask = paths[i] > 0, cmap='Blues', annot=False, yticklabels=False, xticklabels=False, ax=ax)