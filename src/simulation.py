from loguru import logger
import numpy as np

NEAREST_NEIGHBOUR_COUPLING_CONSTANT = 1
BOLTZMANN_CONSTANT = 1.38e-23

class Simulation:
    
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.spins = [[int(np.random.choice([-1, +1])) for _ in range(self.width)] for _ in range(self.height)]
    
    def update(self, delta, temperature):
        # Calculate energy for every spin.
        energy_matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y, row in enumerate(self.spins):
            for x, spin in enumerate(row):
                neighbour_spin_left   = self.get_spin(x - 1, y)
                neighbour_spin_right  = self.get_spin(x + 1, y)
                neighbour_spin_bottom = self.get_spin(x, y - 1)
                neighbour_spin_top    = self.get_spin(x, y + 1)
                neighbour_spins = [neighbour_spin_left, neighbour_spin_right, neighbour_spin_bottom, neighbour_spin_top]
                neighbour_spins = [spin for spin in neighbour_spins if not (spin is None)]
                energy_matrix[y][x] = calculate_spin_energy(spin, neighbour_spins)
        
        # Random choose next spin value for each spin from the energy.
        new_spins = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y, row in enumerate(energy_matrix):
            for x, energy in enumerate(row):
                new_spins[y][x] = pick_random_spin(energy, temperature)
        
        # Overwrite old spins.
        self.spins = new_spins
    
    def get_spin(self, x, y):
        """
        Returns spin value if the coordinates are valid, else returns None.
        """
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return self.spins[y][x]
    
    def render(self, display):
        pass

def calculate_spin_energy(spin, neighbour_spins):
    """
    Calculate U_i for this particular spin. This function will be more specific in the future, when more 'exotic' interactions are examined (e.g. next-nearest neighbours, general interaction between all spins, or external fields). Specifically, this function will have a name involving 'nearest_neighbours' or something.
    """
    # Warn user in various cases.
    if NEAREST_NEIGHBOUR_COUPLING_CONSTANT < 0:
        logger.warning("Coupling constant (J) is negative, this might make the simulation have undesired behaviour.")
    if NEAREST_NEIGHBOUR_COUPLING_CONSTANT == 0:
        logger.warning("Coupling constant (J) is zero, this disables spin interaction.")
    
    # Calculate energy.
    J = NEAREST_NEIGHBOUR_COUPLING_CONSTANT
    energy = -J/2 * spin * sum(neighbour_spins)
    return energy

def pick_random_spin(energy, temperature):
    # Calculate proportionality factor for spin up and spin down.
    spin_up_factor   = np.exp(energy * temperature * BOLTZMANN_CONSTANT)
    spin_down_factor = np.exp(energy * temperature * BOLTZMANN_CONSTANT)
    
    # Calculate normalized probabilities.
    spin_up_prob   = spin_up_factor / (spin_up_factor + spin_down_factor)
    spin_down_prob = spin_down_factor / (spin_up_factor + spin_down_factor)
    
    # Draw random integer.
    rand_int = np.random.randint(low=0, high=1e6)
    
    # Return new spin.
    if rand_int < spin_up_prob * 1e6:
        return +1
    else:
        return -1
