from simulation import Simulation
import pygame

if __name__ == "__main__":
    sim = Simulation()  # one Simulation instance
    sim.setup(10)
    sim.run(10, 1)
