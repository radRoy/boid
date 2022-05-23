import sys
import pygame as pg
from simulation import Simulation
from obstacles import Obstacle, Circle, Wall

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def main(sim: Simulation, fps: int) -> None:
    """the function in charge of handling all function calls regarding the live animation interface and display"""
    pg.init()

    size = (720, 720)
    display = pg.display.set_mode(size)

    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        dt = clock.tick(fps)

        sim.step(dt)
        display.fill(WHITE)

        for actor in sim.actors:
            direction = actor.v.normalize()
            left = actor.pos - direction*10 + direction.orthonormal()*2
            right = actor.pos - direction*10 - direction.orthonormal()*2
            pg.draw.polygon(display, actor.color, points=[actor.pos, left, right])

        for obstacle in sim.obstacles:
            if type(obstacle) is Wall:
                pg.draw.line(display, BLUE, obstacle.start, obstacle.stop, 10)
            elif type(obstacle) is Circle:
                pg.draw.circle(display, RED, obstacle.pos, obstacle.rad)

        pg.display.update()  # better than display.flip() (faster & does more)


if __name__ == "__main__":
    sim_test = Simulation((720, 720))
    sim_test.setup(nboids=50)

    main(sim=sim_test, fps=30)
