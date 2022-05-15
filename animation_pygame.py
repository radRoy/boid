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
# import pygame.camera  # CAUTION: code will very likely break with next pygame release! (see doc pg.camera.Camera)
import simulation as s
import numpy as np
# import matplotlib.pyplot as plt  # TBD: for creation of background grid


def get_actors_positions(sim: s.Simulation):
    """get Simulation.actors' positions and return as numpy array"""
    xys = np.full((len(sim.actors), 2), .0)
    for i, actor in enumerate(sim.actors):
        xys[i] = np.array([actor.pos[0], actor.pos[1]])
    return xys


def get_zoom(xys: np.ndarray, size: tuple, screen_coverage: float = .5):
    """calculate the zoom needed to display flock as a whole with some boarder region"""
    # could use corners - half the variable count - double speed
    xmin, xmax = np.min(xys[:, 0]), np.max(xys[:, 0])
    ymin, ymax = np.min(xys[:, 1]), np.max(xys[:, 1])
    xspan = xmax - xmin
    yspan = ymax - ymin
    if xspan > yspan:  # TBD: make proportional to chosen display resolution
        span = xspan
    else:
        span = yspan
    return min(size) / span * screen_coverage


def get_transposition(xys: np.ndarray, size: tuple):
    """returns transposition/-location (linear transformation) vector,
    for a flock of Actors to be centered in the (static) pygame.display"""
    display_centre = np.array([size[0] // 2, size[1] // 2])  # centre of the pygame.display
    # flock_median_pos = np.array(np.median(xys[:, 0]), np.median(xys[:, 1]))
    flock_mean_pos = np.array(np.mean(xys[:, 0]), np.mean(xys[:, 1]))
    # return display_centre - flock_mean_pos
    return 0 - flock_mean_pos


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
    # pg.display.get_desktop_sizes()  # useful to run program on other devices (e.g. multi-devs or .exe running)
    # can use hardware acceleration if toggling pygame's fullscreen mode on ('flags' in .set_mode())
    screen = pg.display.set_mode(size)
    # https://www.pygame.org/docs/ref/display.html - .set_mode() seems able to do automatic scaling & tracking

    # black = 0, 0, 0
    white = 255, 255, 255
    background = white
    # TBD: add a grid for position tracking in moving screen
    # IDEA: could use mpl.pyplot for creating .png of resolution adapted to pygame.get_desktop_size(), procedural

    # CALCULATE initial zoom & transposition
    # xys = get_actors_positions(sim)
    # zoom = get_zoom(xys, size, .5)
    # transpose = get_transposition(xys, size)

    # INIT RECTS POSITIONS (& init frame, not required for ani. to work)
    arrow = pg.image.load("arrowhead_upwards_tiny.png")
    screen.fill(background)
    temp_zoom = 50
    # print((zoom * xys + transpose)[0])  # TBD: have to apply these operations to the Rect objects after .move()
    for i, boid in enumerate(actors):
        rect = arrow.get_rect()  # TBD: configure .get_rect() to return centre instead of (leftupper) corner coordinates
        rect = rect.move([boid.pos[0] * temp_zoom, boid.pos[1] * temp_zoom])
        rects.append(rect)
        screen.blit(arrow, rect)  # look into .blits() for one-liner of multi-Surface animation
    pg.display.update()  # more efficient & capable version of .display.flip() (flip() must do vsync, update() can)

    while True:
        for event in pg.event.get():
            # print(f"event = {event}")  # registers keyboard & mouse inputs & cursor location with or without usage
            if event.type == pg.QUIT:
                # pg.camera.Camera.stop()  # .start() not found
                sys.exit()

        # UPDATE Simulation()
        sim.step(dt)  # = sim.run(steps=1, dt=dt)

        # CALCULATE zoom & transposition
        # xys = get_actors_positions(sim)
        # zoom = get_zoom(xys, size, .5)
        # transpose = get_transposition(xys, size)

        # UPDATE DISPLAY
        # screen.fill(background)  # comment out to see movement trajectories
        for i, rect in enumerate(rects):
            boid = actors[i]
            # rect = rect.move(boid.pos)  # boids overlap, currently
            rect = rect.move([boid.pos[0] * temp_zoom, boid.pos[1] * temp_zoom])  # boids don't overlap
            screen.blit(arrow, rect)
        pg.display.update()


if __name__ == "__main__":
    sim_test = s.Simulation()
    sim_test.setup(nboids=50)

    # pg.init()
    # print(pg.camera.get_backends())  # MSMF seems like earliest implemented Camera in pygame
    main(sim=sim_test, fps=60)
