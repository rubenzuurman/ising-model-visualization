from loguru import logger
import numpy as np
import pygame

from src.constants import *

class Simulation:
    
    def __init__(self, width=10, height=10, mode="nearest_neighbour"):
        self.width = width
        self.height = height
        self.spins = [[int(np.random.choice([-1, +1])) for _ in range(self.width)] for _ in range(self.height)]
        self.average_spin_over_time = []
        
        # Set mode.
        available_modes = ["nearest_neighbour"]
        if not (mode in available_modes):
            logger.critical(f"Mode '{mode}' is not a valid mode! (Options: {available_modes})")
        self.mode = mode
    
    def update(self, temperature):
        # Calculate energy for every spin.
        energy_matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y, row in enumerate(self.spins):
            for x, spin in enumerate(row):
                if self.mode == "nearest_neighbour":
                    # Get nearest neighbour spins.
                    neighbour_spin_left   = self.get_spin(x - 1, y)
                    neighbour_spin_right  = self.get_spin(x + 1, y)
                    neighbour_spin_bottom = self.get_spin(x, y - 1)
                    neighbour_spin_top    = self.get_spin(x, y + 1)
                    neighbour_spins = [neighbour_spin_left, neighbour_spin_right, neighbour_spin_bottom, neighbour_spin_top]
                    
                    # Keep only spins that are not None (e.g. spins that are in the field and thus actually exist).
                    neighbour_spins = [spin for spin in neighbour_spins if not (spin is None)]
                    
                    # Calculate energy from nearest neighbours and store into energy matrix.
                    energy_matrix[y][x] = calculate_nearest_neighbour_spin_energy(spin, neighbour_spins)
        
        # Random choose next spin value for each spin from the energy.
        new_spins = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y, row in enumerate(energy_matrix):
            for x, energy in enumerate(row):
                new_spins[y][x] = pick_random_spin(energy, temperature)
        
        # Overwrite old spins.
        self.spins = new_spins
        
        # Append average spin to cummulative list.
        self.average_spin_over_time.append(self.get_average_spin())
    
    def get_spin(self, x, y):
        """
        Returns spin value if the coordinates are valid, else returns None.
        """
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return self.spins[y][x]
    
    def get_average_spin(self):
        return sum([sum(row) for row in self.spins]) / (self.width * self.height)
    
    def render(self, display, font, resolution):
        for y, row in enumerate(self.spins):
            for x, spin in enumerate(row):
                self.render_spin(display, resolution, x, y, spin)
    
    def render_spin(self, display, resolution, x, y, spin):
        # Calculate screen position.
        SPIN_SEPARATION = 50
        spin_x = resolution[0] / 2 + (x - self.width / 2) * SPIN_SEPARATION
        spin_y = resolution[1] / 2 + (y - self.height / 2) * SPIN_SEPARATION
        
        # Render arrow at spin position.
        pygame.draw.line(display, (255, 255, 255), (spin_x, spin_y - 10), (spin_x, spin_y + 10))
        if spin == -1:
            pygame.draw.line(display, (255, 255, 255), (spin_x, spin_y + 10), (spin_x - 4, spin_y + 6))
            pygame.draw.line(display, (255, 255, 255), (spin_x, spin_y + 10), (spin_x + 4, spin_y + 6))
        elif spin == +1:
            pygame.draw.line(display, (255, 255, 255), (spin_x, spin_y - 10), (spin_x - 4, spin_y - 6))
            pygame.draw.line(display, (255, 255, 255), (spin_x, spin_y - 10), (spin_x + 4, spin_y - 6))
        else:
            pygame.draw.circle(display, (0, 0, 255), (spin_x, spin_y), 10)

def calculate_nearest_neighbour_spin_energy(spin, neighbour_spins):
    """
    Calculate U_i for this particular spin. This function will be more specific in the future, when more 'exotic' interactions are examined (e.g. next-nearest neighbours, general interaction between all spins, or external fields). Specifically, this function will have a name involving 'nearest_neighbours' or something.
    """
    # Calculate energy.
    J = NEAREST_NEIGHBOUR_COUPLING_CONSTANT
    energy = -J/2 * spin * sum(neighbour_spins)
    return energy

def pick_random_spin(energy, temperature):
    # Calculate proportionality factor for spin up and spin down.
    spin_up_factor   = np.exp(-energy / (temperature * BOLTZMANN_CONSTANT))
    spin_down_factor = np.exp(energy / (temperature * BOLTZMANN_CONSTANT))
    
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
