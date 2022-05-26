import sys
import pygame as pg
import pygame_widgets as pg_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import actors
from simulation import Simulation
from actors import Actor, Boid, Predator
from obstacles import Obstacle, Circle, Wall
from vectors2d import Vector

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def draw_actors(sim, display):
    """Iterates over all the actors in the simulation and draws them on screen."""
    for actor in sim.actors:
        # get the average direction of the last few frames of the actor
        direction = Vector(0, 0)
        for d in actor.dir_history:
            direction += d
        direction /= len(actor.dir_history)

        if type(actor) is Predator:
            left = actor.pos - direction * 15 + direction.orthonormal() * 5
            right = actor.pos - direction * 15 - direction.orthonormal() * 5
        else:
            left = actor.pos - direction * 10 + direction.orthonormal() * 2
            right = actor.pos - direction * 10 - direction.orthonormal() * 2

        pg.draw.polygon(display, actor.color, points=[actor.pos, left, right])


def draw_obstacles(sim, display):
    """Iterates over all the obstacles in the simulation and draws them on screen."""
    for obstacle in sim.obstacles:
        if type(obstacle) is Wall:
            pg.draw.line(display, BLUE, obstacle.start, obstacle.stop, 10)
        elif type(obstacle) is Circle:
            pg.draw.circle(display, BLUE, obstacle.pos, obstacle.rad)


def main(sim, fps, window_size):
    """Main function"""

    pg.init()
    display = pg.display.set_mode(window_size)
    clock = pg.time.Clock()

    mouse_circle = None

    # Main game loop
    while True:
        # Get all events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                if mouse_circle is not None:
                    sim.delete_obstacles(mouse_circle)
                mouse_pos = pg.mouse.get_pos()
                mouse_circle = Circle(mouse_pos, 20)
                sim.add_obstacles(mouse_circle)

        display.fill(WHITE)
        dt = clock.tick(fps)

        sim.step(dt)
        draw_actors(sim, display)
        draw_obstacles(sim, display)

        pg.display.update()


if __name__ == "__main__":
    sim_test = Simulation((720, 720))
    sim_test.setup(nboids=50)

    main(sim=sim_test, fps=30, window_size=(720, 720))
