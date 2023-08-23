import streamlit as st
import astar_utils
import matplotlib.pyplot as plt
import streamlit.components.v1 as components


st.title("8 Puzzle solver using A* Search with Different Heuristics")

heuristic = st.selectbox("Heuristic to be used:", ["h(n) = 0 (Uniform Cost Search)", "Number of Displaced Tiles", "Manhattan Distance", "Euclidean Distance"])

temp_grid = st.text_input("Initial Grid(Give input as a string of 9 characters, 0 is blank tile):", "123450678")

c = st.container()

def solver(heuristic, temp_grid):

    temp_grid = [int(i) for i in temp_grid]
    initial_grid = ((temp_grid[0], temp_grid[1], temp_grid[2]),
                    (temp_grid[3], temp_grid[4], temp_grid[5]),
                    (temp_grid[6], temp_grid[7], temp_grid[8]))
    
    if astar_utils.soln_exists(initial_grid):
        st.write("Valid Input.")
    else:
        st.write("Solution is not possible for this input grid.")
        exit()
    
    if heuristic == "h(n) = 0 (Uniform Cost Search)":
        output = astar_utils.solve_puzzle(initial_grid, 1)
        
        st.write("Heuristic: ", heuristic)
        st.write("Number of states explored: ", output['states_explored'])
        ani = astar_utils.get_plots(output)
        
        components.html(ani.to_jshtml(), height = 400, width = 500)
    
    elif heuristic == "Number of Displaced Tiles":
        output = astar_utils.solve_puzzle(initial_grid, 2)
        
        st.write("Heuristic = ", heuristic)
        st.write("Number of states explored: ", output['states_explored'])
        ani = astar_utils.get_plots(output)
        components.html(ani.to_jshtml(), height = 400, width = 500)
        
    elif heuristic == "Manhattan Distance":
        output = astar_utils.solve_puzzle(initial_grid, 3)
        
        st.write("Heuristic = ", heuristic)
        st.write("Number of states explored: ", output['states_explored'])
        ani = astar_utils.get_plots(output)
        components.html(ani.to_jshtml(), height = 400, width = 500)
        
    elif heuristic == "Euclidean Distance":
        output = astar_utils.solve_puzzle(initial_grid, 4)
        
        st.write("Heuristic = ", heuristic)
        st.write("Number of states explored: ", output['states_explored'])
        ani = astar_utils.get_plots(output)
        components.html(ani.to_jshtml(), height = 400, width = 500)
        
    else:
        st.write("Invalid Output.")

c.button("Solve", on_click = solver(heuristic, temp_grid))