from src.simulation import Simulation

def main():
    sim = Simulation(width=10, height=10)
    print(sim.spins)
    sim.update(delta=0.01, temperature=1)
    print(sim.spins)

if __name__ == "__main__":
    main()
