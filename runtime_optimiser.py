from scipy.optimize import minimize
import numpy as np
from collections import defaultdict

def get_bounds (speed_time: dict, speeds: list, time: float) -> list[float]:
    speed_time = defaultdict(lambda: (0, time/60), speed_time)
    bounds = [(speed_time[speed][0], speed_time[speed][1]) for speed in speeds]
    return bounds


# Define the constraint functions
def get_constraint_functions(time, distance, speeds):
    num_speeds = len(speeds)  

    def distance_constraint(vars):
        c1 = sum(speed * var for speed, var in zip(speeds, vars)) - distance
        return c1

    def time_constraint(vars):
        c2 = sum(vars) - time / 60
        return c2

    
    return [distance_constraint, time_constraint]

# Objective function (dummy function as we are only interested in constraints)
def objective(dummy):
    return 1  # Dummy objective for constraint satisfaction

# Pretty print function
def pretty_print_results(data):
    hours, speed = data
    total_minutes = hours * 60
    minutes = int(total_minutes)
    seconds = int((total_minutes - minutes) * 60)
    return f"Run {speed} kmph for {minutes} minutes : {seconds} seconds."

# Decorator to print results nicely
def print_results(func):
    def wrapper(*args, **kwargs):
        running_speed = [8, 9, 10, 11.5, 12.5, 13.5, 14.0]
        solutions = func(*args, **kwargs)
        for sol in solutions:
            list_of_results = list(map(pretty_print_results, zip(sol.x, running_speed)))
            print("Solution:")
            for result in list_of_results:
                print(result)
            print("-" * 30)
            return list(zip(sol.x, running_speed))
    return wrapper

# Function to perform multi-start optimization

def find_multiple_solutions(time, distance, speeds, bounds, num_starts=5):
    constraints = get_constraint_functions(time, distance, speeds)
    
    solutions = []
    for _ in range(num_starts):
        initial_guess = np.random.uniform(0, time / 60, len(speeds))      

        cons = [{'type': 'eq', 'fun': constraints[0]},  # distance constraint
                {'type': 'eq', 'fun': constraints[1]}]  # time constraint       
       
        sol = minimize(objective, initial_guess, bounds=bounds, constraints=cons)                
        if sol.success:  # Check if a solution is found
            solutions.append(list(zip(sol.x, speeds)))
    return solutions
def gini(x):
    return np.sum(np.abs(np.subtract.outer(x, x)))/(2*len(x)**2*x.mean())
