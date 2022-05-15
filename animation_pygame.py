"""animation_pygame.py
code adapted from https://www.pygame.org/docs/tut/PygameIntro.html and https://www.pygame.org/docs/ in general.
images taken from:
    - https://www.iconfinder.com/icons/1051165/arrow_head_arrowhead_direction_move_orientation_pointer_right_icon (rightward arrowhead)
    - https://www.iconfinder.com/icons/1051162/arrow_head_arrowhead_direction_move_orientation_pointer_send_up_icon (upward arrowhead)
abbreviations used:
    - RT: real time"""

import sys
import pygame
import simulation as s


def main(sim: s.Simulation, fps: int) -> None:
    """the function in charge of handling all function calls regarding the live animation interface and display"""
    dt = fps / 1000
    # boid = sim.actors[0]
    boids = sim.actors
    rects = []
    arrows = []

    pygame.init()
    size = (res_x, res_y) = 1280, 720
    screen = pygame.display.set_mode(size)
    black = 0, 0, 0
    white = 255, 255, 255
    background = white

    # INIT RECTS POSITIONS (& init frame, not required for ani. to work)
    arrow = pygame.image.load("arrowhead_upwards_tiny.png")
    screen.fill(background)  # add a grid for position tracking in moving screen
    # for i, boid in enumerate(boids):
    for i, boid in enumerate(sim.actors):
        rect = arrow.get_rect()
        rect = rect.move(boid.pos)
        rects.append(rect)
        # rects.append(arrow.get_rect())
        # rects[i] = rects[i].move(boid.pos)
        # screen.blit(arrow, rects[i])
        screen.blit(arrow, rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            # print(f"event = {event}")
            if event.type == pygame.QUIT:
                sys.exit()

        # UPDATE Simulation()
        sim.step(dt)  # = sim.run(steps=1, dt=dt)

        # UPDATE DISPLAY
        screen.fill(background)  # add a grid for position tracking in moving screen
        for i, rect in enumerate(rects):
            # rect = rect.move(boids[i].pos)
            # rect = rect.move([sim.actors[i].pos[0]*20, sim.actors[i].pos[1]*20])
            rect = rect.move([boids[i].pos[0]*50, boids[i].pos[1]*50])
            # screen.blit(arrows[i], rect)
            screen.blit(arrow, rect)
        pygame.display.flip()


if __name__ == "__main__":
    sim_test = s.Simulation()
    sim_test.setup(nboids=50)

    main(sim=sim_test, fps=60)
