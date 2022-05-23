import sys
import pygame as pg
from simulation import Simulation
from obstacles import Obstacle, Circle, Wall
from vectors2d import Vector

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def main(sim, fps, window_size):
    """Main function"""

    pg.init()
    display = pg.display.set_mode(window_size)

    # Slider(pg.display, dist_left, dist_top, length, width, ...)
    separation_slider = Slider(display, 10, 10, 100, 10, min=0, max=10.0, step=.01)
    alignment_slider = Slider(display, 10, 50, 100, 10, min=0, max=10.0, step=.01)
    cohesion_slider = Slider(display, 10, 90, 100, 10, min=0, max=10.0, step=.01)

    # TextBox(pg.display, dist_left, dist_top, length, width, ...)
    cohesion_output = TextBox(display, 45, 30, 25, 25, fontSize=16, borderThickness=1)
    cohesion_output = TextBox(display, 45, 70, 25, 25, fontSize=16, borderThickness=1)
    cohesion_output = TextBox(display, 45, 110, 25, 25, fontSize=16, borderThickness=1)
    cohesion_output.disable()  # Act as label instead of textbox

    # TBD: write description for each slider (for the textbox below)

    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        dt = clock.tick(fps)
        sim.step(dt)
        display.fill(WHITE)

        for actor in sim.actors:
            direction = Vector(0, 0)
            for d in actor.dir_history:
                direction += d
            direction /= len(actor.dir_history)

            left = actor.pos - direction * 10 + direction.orthonormal() * 2
            right = actor.pos - direction * 10 - direction.orthonormal() * 2
            pg.draw.polygon(display, actor.color, points=[actor.pos, left, right])

        for obstacle in sim.obstacles:
            if type(obstacle) is Wall:
                pg.draw.line(display, BLUE, obstacle.start, obstacle.stop, 10)
            elif type(obstacle) is Circle:
                pg.draw.circle(display, BLUE, obstacle.pos, obstacle.rad)

        pg.display.update()


if __name__ == "__main__":
    sim_test = Simulation((720, 720))
    sim_test.setup(nboids=50)

    main(sim=sim_test, fps=30, window_size=(720, 720))
