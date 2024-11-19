from loguru import logger
import numpy as np

from src.constants import *
import src.graph_generator as generator
from src.simulation import Simulation
from src.visualizer import window

def verify_constants():
    # Warn user for untypical coupling constant for nearest neighbour interaction.
    if NEAREST_NEIGHBOUR_COUPLING_CONSTANT < 0:
        logger.warning("Coupling constant (J) is negative, this might make the simulation exhibit undesired behaviour.")
    if NEAREST_NEIGHBOUR_COUPLING_CONSTANT == 0:
        logger.warning("Coupling constant (J) is zero, this disables nearest neighbour spin interaction.")
    
    # Warn user for invalid value for the Boltzmann constant.
    if BOLTZMANN_CONSTANT <= 0:
        logger.critical("Boltzmann constant must have a positive value!")

def generate_graphs():
    # Set seed.
    np.random.seed(SEED)
    
    # Generate graphs.
    generator.nearest_neighbour_coupling_mean_magnetization()

def run_visualizer():
    sim = Simulation(width=50, height=50, mode="nearest_neighbour")
    window(resolution=(1920, 1080), simulation=sim)

def main():
    # Verify constants.
    verify_constants()
    
    # Generate graphs.
    generate_graphs()
    
    # Run visualizer (or generate graph, or etc).
    run_visualizer()

if __name__ == "__main__":
    main()
