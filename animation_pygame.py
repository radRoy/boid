"""animation_pygame.py
in pygame, every image is a pygame.surface.Surface object, including the displayed image surface
code adapted from https://www.pygame.org/docs/tut/PygameIntro.html and https://www.pygame.org/docs/ in general.
images taken from:
    - https://www.iconfinder.com/icons/1051165/arrow_head_arrowhead_direction_move_orientation_pointer_right_icon (rightward arrowhead)
    - https://www.iconfinder.com/icons/1051162/arrow_head_arrowhead_direction_move_orientation_pointer_send_up_icon (upward arrowhead)
abbreviations used:
    - RT: real time"""

import sys
import pygame as pg
import pygame.camera  # CAUTION: code will very likely break with next pygame release! (see doc pg.camera.Camera)
import simulation as s


def main(sim: s.Simulation, fps: int) -> None:
    """the function in charge of handling all function calls regarding the live animation interface and display"""
    dt = fps / 1000
    actors = sim.actors
    rects = []

    pg.init()  # multiple .init()s don't hurt pygame
    # pg.camera.init()
    # pg.camera.init('_camera (MSMF)')
    # neither cameras make ..Camera.start() work (not found)
    # pg.camera.Camera.start()  # not found

    size = (res_x, res_y) = 720, 720
    screen = pg.display.set_mode(size)
    # black = 0, 0, 0
    white = 255, 255, 255
    background = white
    # TBD: add a grid for position tracking in moving screen

    # INIT RECTS POSITIONS (& init frame, not required for ani. to work)
    arrow = pg.image.load("arrowhead_upwards_tiny.png")
    screen.fill(background)
    for i, boid in enumerate(actors):
        rect = arrow.get_rect()
        rect = rect.move(boid.pos)
        rects.append(rect)
        screen.blit(arrow, rect)  # look into .blits() for one-liner of multi-Surface animation
    pg.display.update()  # more efficient & capable version of .display.flip() (flip() must do vsync, update() can)

    while True:
        for event in pg.event.get():
            # print(f"event = {event}")  # registers keyboard & mouse inputs & cursor location with or without usage
            if event.type == pg.QUIT:
                sys.exit()

        # UPDATE Simulation()
        sim.step(dt)  # = sim.run(steps=1, dt=dt)

        # UPDATE DISPLAY
        screen.fill(background)  # comment out to see movement trajectories
        for i, rect in enumerate(rects):
            boid = actors[i]
            # rect = rect.move(boid.pos)  # boids overlap, currently
            rect = rect.move([boid.pos[0]*50, boid.pos[1]*50])  # boids don't overlap
            screen.blit(arrow, rect)
        pg.display.update()

    # pg.camera.Camera.stop()  # .start() not found


if __name__ == "__main__":
    sim_test = s.Simulation()
    sim_test.setup(nboids=30)

    # pg.init()
    # print(pg.camera.get_backends())  # MSMF seems like earliest implemented Camera in pygame
    main(sim=sim_test, fps=30)
