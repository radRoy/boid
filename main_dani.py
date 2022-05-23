import sys
import pygame as pg
import pygame_widgets as pg_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import actors
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

    #%% slider settings start

    slider_left, slider_top = 15, 15  # distance in pixel between sliders and left, top pg.display border
    slider_width, slider_height = 100, 10  # width (x-dir.), height (y-dir.) in pixel
    separation_slider = Slider(display, slider_left, slider_top, slider_width, slider_height, min=0.0, max=10.0, step=.01)
    textbox_width, textbox_height = 20, 20
    textbox_dist = 20
    separation_output = TextBox(display, slider_left, slider_top + textbox_dist, textbox_width, textbox_height, fontSize=16, borderThickness=1)
    separation_output.disable()  # act as label instead of textbox

    slider_dist = 50
    cohesion_slider = Slider(display, slider_left, slider_top + slider_dist, slider_width, slider_height, min=0.0, max=10.0, step=.01)
    cohesion_output = TextBox(display, slider_left, slider_top + slider_dist + textbox_dist, textbox_width, textbox_height, fontSize=16, borderThickness=1)
    cohesion_output.disable()

    alignment_slider = Slider(display, slider_left, slider_top + slider_dist*2, slider_width, slider_height, min=0.0, max=10.0, step=.01)
    alignment_output = TextBox(display, slider_left, slider_top + slider_dist*2 + textbox_dist, textbox_width, textbox_height, fontSize=16, borderThickness=1)
    alignment_output.disable()

    #%% slider settings end

    clock = pg.time.Clock()

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()

        dt = clock.tick(fps)
        sim.step(dt)
        display.fill(WHITE)

        # feeding slider values into simulation parameters
        actors.separation_strength = separation_slider.getValue()  # 7.0 (yep, dem is birds, alright)
        actors.cohesion_strength = cohesion_slider.getValue()  # 3.0
        actors.alignment_strength = alignment_slider.getValue()  # 3.5

        # each following drawing command draws on top of previous ones (so, leave widgets.update on top)
        separation_output.setText(actors.separation_strength)
        cohesion_output.setText(actors.cohesion_strength)
        alignment_output.setText(actors.alignment_strength)
        pg_widgets.update(events)

        for obstacle in sim.obstacles:
            if type(obstacle) is Wall:
                pg.draw.line(display, BLUE, obstacle.start, obstacle.stop, 10)
            elif type(obstacle) is Circle:
                pg.draw.circle(display, BLUE, obstacle.pos, obstacle.rad)

        for actor in sim.actors:
            direction = Vector(0, 0)
            for d in actor.dir_history:
                direction += d
            direction /= len(actor.dir_history)

            left = actor.pos - direction * 10 + direction.orthonormal() * 2
            right = actor.pos - direction * 10 - direction.orthonormal() * 2
            pg.draw.polygon(display, actor.color, points=[actor.pos, left, right])
            # pg.draw.line(display, GREEN, actor.pos, actor.pos + actor.ahead)  # debug

        pg.display.update()


if __name__ == "__main__":
    res = (x, y) =\
    1280,\
    720
    sim_test = Simulation(res)
    sim_test.setup(nboids=50)

    main(sim=sim_test, fps=30, window_size=res)
