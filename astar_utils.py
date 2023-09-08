import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from matplotlib.colors import ListedColormap

target = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

def find_blank(grid):
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                return i, j

def get_plots(output, cmap_name='coolwarm'):
    paths = output['optimal_path']
    plt.rcParams["figure.figsize"] = (3, 2)
    plt.rcParams['figure.dpi'] = 150
    plt.ioff()

    def plot(i):
        fig.clear()
        ax = fig.add_subplot(111)
        my_cmap = ListedColormap(['bisque']).copy()
        my_cmap.set_under('greenyellow')
        sns.heatmap(
            paths[i], annot=True, annot_kws={"size": 10}, cbar=False,
            linewidths=3, linecolor='black', cmap=cmap_name,
            yticklabels=False, xticklabels=False, vmin=1, ax=ax
        )

        title = str(i+1) + ' out of ' + str(len(paths)) + ' items in the optimal path'
        plt.title(title)
        plt.tight_layout()

    n_frames = len(paths)
    fig, ax = plt.subplots()

    anim = animation.FuncAnimation(fig, plot, frames=n_frames, interval=1000)

    return anim

# Streamlit UI
st.title("8-Puzzle Solver with Streamlit")

st.sidebar.header("Select Puzzle Configuration")

# Create a 3x3 grid for user input
input_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

for i in range(3):
    for j in range(3):
        input_grid[i][j] = st.sidebar.number_input(f"Tile ({i+1}, {j+1})", 0, 8, 0, key=f"{i}{j}")

if st.sidebar.button("Solve Puzzle"):
    # Check if the input puzzle is solvable
    input_grid = tuple(tuple(row) for row in input_grid)
    if not soln_exists(input_grid):
        st.error("The given puzzle configuration is not solvable.")
    else:
        st.info("Solving the puzzle...")
        output = solve_puzzle(input_grid, h_i=3)
        cmap_name = st.selectbox("Select Grid Color", ["coolwarm", "viridis", "magma", "inferno"])
        anim = get_plots(output, cmap_name=cmap_name)
        st.pyplot(anim.to_jshtml())

st.sidebar.text("Note: Enter values from 0 to 8 (0 represents the blank space).")
