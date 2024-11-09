from src.simulation import Simulation
from src.visualizer import window

def main():
    sim = Simulation(width=10, height=10)
    window(resolution=(1920, 1080), simulation=sim)

if __name__ == "__main__":
    main()
