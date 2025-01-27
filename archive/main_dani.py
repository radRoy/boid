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

    fontsize = 28

    # Slider settings
    s_left = 15  # distance to left window border (x-dir.) in px
    s_top = 15  # distance to top window border (x-dir.) in px
    s_width = 150  # width (x-dir.) in px
    s_height = 10  # height (y-dir.) in px
    s_dist = 50  # distance between sliders (y-dir.) in px

    # TextBox settings
    t_dist = 20  # dist. to corr. slider (above in animation)
    t_left = s_left + s_width + 5  # dist. to left border
    t_top = s_top + t_dist
    t_width, t_height = 30, 20

    # Sliders and TextBoxes by Simulation parameter
    sep_slider = Slider(display, s_left, s_top, s_width, s_height, min=0.0, max=10.0, step=.1)
    sep_out = TextBox(display, t_left, t_top, 0, t_height, fontSize=fontsize, borderThickness=1)
    sep_label = TextBox(display, s_left, s_top + t_dist, 0, t_height, fontSize=fontsize, borderThickness=1).setText("separation")
    coh_slider = Slider(display, s_left, s_top + s_dist, s_width, s_height, min=0.0, max=10.0, step=.1)
    coh_out = TextBox(display, t_left, t_top + s_dist, 0, t_height, fontSize=fontsize, borderThickness=1)
    coh_label = TextBox(display, s_left, s_top + s_dist + t_dist, 0, t_height, fontSize=fontsize, borderThickness=1).setText("coherence")
    align_slider = Slider(display, s_left, s_top + s_dist * 2, s_width, s_height, min=0.0, max=10.0, step=.1)
    align_out = TextBox(display, t_left, t_top + s_dist * 2, 0, t_height, fontSize=fontsize, borderThickness=1)
    align_label = TextBox(display, s_left, t_top + s_dist * 2, 0, t_height, fontSize=fontsize, borderThickness=1).setText("alignment")

    # view_angle
    # view_distance
    # max_speed
    maxvel_slider = Slider(display, s_left, s_top + s_dist * 4, s_width, s_height, min=0.0, max=10.0, step=.1)
    maxvel_out = TextBox(display, t_left, t_top + s_dist * 4, 0, t_height, fontSize=fontsize, borderThickness=1)
    maxvel_label = TextBox(display, s_left, t_top + s_dist * 4, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 4")
    slider_5 = Slider(display, s_left, s_top + s_dist * 5, s_width, s_height, min=0.0, max=10.0, step=.1)
    slider_5_out = TextBox(display, t_left, t_top + s_dist * 5, 0, t_height, fontSize=fontsize, borderThickness=1)
    slider_5_label = TextBox(display, s_left, t_top + s_dist * 5, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 5")
    # slider_6 = Slider(display, s_left, s_top + s_dist * 6, s_width, s_height, min=0.0, max=10.0, step=.1)
    # slider_6_out = TextBox(display, t_left, t_top + s_dist * 6, 0, t_height, fontSize=fontsize, borderThickness=1)
    # slider_6_label = TextBox(display, s_left, t_top + s_dist * 6, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 6")
    # slider_7 = Slider(display, s_left, s_top + s_dist * 7, s_width, s_height, min=0.0, max=10.0, step=.1)
    # slider_7_out = TextBox(display, t_left, t_top + s_dist * 7, 0, t_height, fontSize=fontsize, borderThickness=1)
    # slider_7_label = TextBox(display, s_left, t_top + s_dist * 7, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 7")
    # slider_8 = Slider(display, s_left, s_top + s_dist * 8, s_width, s_height, min=0.0, max=10.0, step=.1)
    # slider_8_out = TextBox(display, t_left, t_top + s_dist * 8, 0, t_height, fontSize=fontsize, borderThickness=1)
    # slider_8_label = TextBox(display, s_left, t_top + s_dist * 8, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 8")
    # slider_9 = Slider(display, s_left, s_top + s_dist * 9, s_width, s_height, min=0.0, max=10.0, step=.1)
    # slider_9_out = TextBox(display, t_left, t_top + s_dist * 9, 0, t_height, fontSize=fontsize, borderThickness=1)
    # slider_9_label = TextBox(display, s_left, t_top + s_dist * 9, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 9")

    #%% slider settings end

    #%% mouse settings start TBD (Falco Punch!)
    #%% mouse settings end

    clock = pg.time.Clock()

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()

        # feeding slider values into simulation parameters
        actors.separation_strength = sep_slider.getValue()  # 7.0 (yep, dem is birds, alright)
        actors.cohesion_strength = coh_slider.getValue()  # 3.0
        actors.alignment_strength = align_slider.getValue()  # 3.5

        # each following drawing command draws on top of previous ones (so, leave widgets.update on top)
        sep_out.setText(actors.separation_strength)
        coh_out.setText(actors.cohesion_strength)
        align_out.setText(actors.alignment_strength)

        display.fill(WHITE)
        pg_widgets.update(events)

        dt = clock.tick(fps)
        sim.step(dt)

        for obstacle in sim.obstacles:
            if type(obstacle) is Wall:
                pg.draw.line(display, BLUE, obstacle.start, obstacle.stop, 10)
            elif type(obstacle) is Circle:
                pg.draw.circle(display, BLUE, obstacle.pos, obstacle.rad)

        for actor in sim.actors:
            break  # predator TBD
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
