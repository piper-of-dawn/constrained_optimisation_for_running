import streamlit as st
import numpy as np

from runtime_optimiser import get_bounds, find_multiple_solutions, gini, pretty_print_results
st.title("Run Planning using Constrained Optimization")


# Parameters
distance = st.number_input("Enter distance:", value=5)
time = st.number_input("Enter time:", value=25)
speeds = st.text_area(
    "Enter speeds in KMPH (comma separated):", 
    value="10.0, 11.5, 12, 13.5, 14.0, 14.5, 15, 15.5", 
    height=100
)
speeds = [float(speed) for speed in speeds.split(",")]
speeds_constraints = st.text_area(
    "Enter speed constraints (speed: [min_mins, max_mins], comma separated. All constraints should be enclosed within { }. Make sure it's a valid Python dict):",
    value="{10.0: [0, 26], 13.5: [1, 25], 14.0: [2, 7], 14.5: [1, 5], 15: [2, 3]}",
    height=150,  # Taller text area for better mobile editing
    placeholder="{10.0: [0, 26], 13.5: [1, 25], 14.0: [2, 7], 14.5: [1, 5], 15: [2, 3]}"
)

speeds_constraints = eval(speeds_constraints)
speeds_constraints = {speed: [min_mins/60, max_mins/60] for speed, (min_mins, max_mins) in speeds_constraints.items()}
bounds = get_bounds(speed_time=speeds_constraints, speeds=speeds, time=time)
# Find and print multiple solutions

pace_variations = st.selectbox("Select Pace Variations you want (How often do you want to change pace?)", ["Minimum", "Maximum"])
ar = find_multiple_solutions(time, distance, speeds, bounds=bounds, num_starts=10)

if not ar:
    st.write("NO SOLUTIONS FOUND")
    st.write("You possibly have entered impossible constraints")

if ar:    
    if pace_variations == "Minimum":
        best = ar[np.argmax([gini(np.array(array)[:,0]) for array in ar])]
    else:
        best = ar[np.argmin([gini(np.array(array)[:,0]) for array in ar])]
    for item in best:
        final_plan = "\n".join([pretty_print_results(item) for item in best])
    st.text_area("Your Running Plan:", final_plan, height=200, label_visibility="collapsed")





