"""animation_pygame.py
code adapted from https://www.pygame.org/docs/tut/PygameIntro.html and https://www.pygame.org/docs/ in general"""

import sys
import pygame
import simulation as s


def main(sim: s.Simulation, fps: int) -> None:
    """the function in charge of handling all function calls regarding the live animation interface and display"""

    pygame.init()
    size = (width, height) = 1028, 720  # pygame window dimensions
    speed = sim.actors.speeds  # TBD
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    boid = pygame.image.load("arrowhead_upwards.png")
    boid_rect = boid.get_rect()

    while True:

        for event in pygame.event.get():
            # print(f"event = {event}")
            if event.type == pygame.QUIT:
                sys.exit()

        # UPDATE THE FRAME
        boid_rect


if __name__ == "__main__":
    sim_test = s.Simulation()
    sim_test.setup(nboids=1)

    main(sim=sim_test, fps=30)
