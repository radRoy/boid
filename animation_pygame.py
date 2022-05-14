"""animation_pygame.py
code adapted from https://www.pygame.org/docs/tut/PygameIntro.html and https://www.pygame.org/docs/ in general
images taken from:
    - https://www.iconfinder.com/icons/1051165/arrow_head_arrowhead_direction_move_orientation_pointer_right_icon (rightward arrowhead)
    - https://www.iconfinder.com/icons/1051162/arrow_head_arrowhead_direction_move_orientation_pointer_send_up_icon (upward arrowhead)"""

import sys
import pygame
import simulation as s


def main(sim: s.Simulation, fps: int) -> None:
    """the function in charge of handling all function calls regarding the live animation interface and display"""

    pygame.init()
    size = (width, height) = 1028, 720  # pygame window dimensions
    screen = pygame.display.set_mode(size)

    black = 0, 0, 0
    boid = pygame.image.load("arrowhead_upwards.png")
    boid_rect = boid.get_rect()

    boid_speed = sim.actors[0].v
    boid_position = sim.actors[0].pos

    while True:

        for event in pygame.event.get():
            # print(f"event = {event}")
            if event.type == pygame.QUIT:
                sys.exit()

        # UPDATE THE FRAME
        boid_rect = boid_rect.move


if __name__ == "__main__":
    sim_test = s.Simulation()
    sim_test.setup(nboids=1)

    print(f"sim_test.actors: {sim_test.actors}")
    print("\n")
    for x in sim_test.actors:
        print(x)

    #main(sim=sim_test, fps=30)
