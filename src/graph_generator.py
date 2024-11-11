from loguru import logger
import matplotlib.pyplot as plt
import numpy as np

from src.constants import *
from src.simulation import Simulation

PRIMARY_COLOR = "royalblue"
SECONDARY_COLOR = "indianred"

def nearest_neighbour_coupling_mean_magnetization():
    # Generate data from simulation.
    logger.info("Generating simulation results...")
    mean_magnetization = {}
    for temperature in np.linspace(start=0.1, stop=5.0, num=1000):
        logger.info(f"Progress: {(temperature - 0.1) / (5.0 - 0.1) * 100.0:.2f}%")
        sim = Simulation(width=20, height=20, mode="nearest_neighbour")
        for _ in range(100):
            sim.update(temperature)
        mean_mag = sum(sim.average_spin_over_time[-50:]) / len(sim.average_spin_over_time[-50:]) # sim.get_average_spin()
        mean_magnetization[temperature] = mean_mag
    logger.info("Done generating simulation results!")
    
    # Generate data using theoretical prediction.
    logger.info("Generating theoretical predictions...")
    theory_data = {temperature: find_tanh_x_eq_ax_solution(temperature) for temperature in np.linspace(start=0.1, stop=5.0, num=5000)}
    logger.info("Done generating theoretical predictions!")
    
    logger.info("Generating plot...")
    # Create figure.
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(12, 8))
    
    # Plot simulation results.
    sim_results, = ax.plot(list(mean_magnetization.keys()), list(mean_magnetization.values()), color=PRIMARY_COLOR)
    sim_results.set_label("Simulation Results")
    
    # Plot theoretical prediction.
    theory_prediction, = ax.plot(list(theory_data.keys()), list(theory_data.values()), color=SECONDARY_COLOR)
    theory_prediction.set_label("Theoretical Predictions")
    
    # Render vertical line indicating the critical temperature.
    z = 4 # 2D
    critical_temperature = (NEAREST_NEIGHBOUR_COUPLING_CONSTANT * z) / BOLTZMANN_CONSTANT
    ax.vlines(x=critical_temperature, ymin=-0.1, ymax=1.1, color="black")
    
    # Set xticks.
    ax.set_xticks(ticks=[-1, 0, 1, 2, 3, 4, 5, critical_temperature], labels=["-1", "0", "1", "2", "3", "4", "5", r"$T_c$"])
    
    # Enable legend and grid.
    ax.legend()
    ax.grid()
    
    # Set graph limits.
    ax.set_xlim([0, 5])
    ax.set_ylim([-0.1, 1.1])
    
    # Set axis labels.
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Mean Spin")
    ax.set_title("Mean Spin vs Temperature for Mean-Field Approximation with Nearest Neighbour Interactions Only")
    
    # Save figure.
    fig.tight_layout()
    fig.savefig("temp.png")

def find_tanh_x_eq_ax_solution(temperature):
    """
    Finds solution to the equation tanh(x) = ax.
    """
    # Initialize parameters for analysis.
    z = 4 # 2D
    beta = 1 / (BOLTZMANN_CONSTANT * temperature)
    a = 1 / (beta * NEAREST_NEIGHBOUR_COUPLING_CONSTANT * z)
    
    # Check if the slope of the line a*x is greater than one. In this case there is only one solution.
    if a > 1:
        return 0
    
    # Evaluate derivative of tanh(x) - ax.
    def eval_derivative(x):
        return 1 - np.tanh(x) ** 2 - a
    
    # Evaluate tanh(x) - ax.
    def eval_function(x):
        return np.tanh(x) - a * x
    
    # Use Newton's method to find the solution.
    x0 = 3 # Three seemed to be a good starting value regardless of a.
    while abs(eval_function(x0)) > 0.0001:
        x0 -= eval_function(x0) / eval_derivative(x0)
    
    # Return x0 * a = beta J z m * (1 / beta J z) = m.
    return x0 * a
