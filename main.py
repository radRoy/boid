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


def setup_sliders(display):
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
    sep_label = TextBox(display, s_left, s_top + t_dist, 0, t_height, fontSize=fontsize, borderThickness=1).setText("Separation")

    align_slider = Slider(display, s_left, s_top + s_dist, s_width, s_height, min=0.0, max=10.0, step=.1)
    align_out = TextBox(display, t_left, t_top + s_dist, 0, t_height, fontSize=fontsize, borderThickness=1)
    align_label = TextBox(display, s_left, s_top + s_dist + t_dist, 0, t_height, fontSize=fontsize, borderThickness=1).setText("Alignment")

    coh_slider = Slider(display, s_left, s_top + s_dist * 2, s_width, s_height, min=0.0, max=10.0, step=.1)
    coh_out = TextBox(display, t_left, t_top + s_dist * 2, 0, t_height, fontSize=fontsize, borderThickness=1)
    coh_label = TextBox(display, s_left, t_top + s_dist * 2, 0, t_height, fontSize=fontsize, borderThickness=1).setText("Cohesion")

    sep_rad_slider = Slider(display, s_left, s_top + s_dist * 4, s_width, s_height, min=0.0, max=80.0, step=.1)
    sep_rad_out = TextBox(display, t_left, t_top + s_dist * 4, 0, t_height, fontSize=fontsize, borderThickness=1)
    sep_rad_label = TextBox(display, s_left, t_top + s_dist * 4, 0, t_height, fontSize=fontsize, borderThickness=1).setText("Separation rad")

    avoid_slider = Slider(display, s_left, s_top + s_dist * 5, s_width, s_height, min=0.0, max=400.0, step=1)
    avoid_out = TextBox(display, t_left, t_top + s_dist * 5, 0, t_height, fontSize=fontsize, borderThickness=1)
    avoid_label = TextBox(display, s_left, t_top + s_dist * 5, 0, t_height, fontSize=fontsize, borderThickness=1).setText("Avoidance")

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

    slider_settings = {"sep_slider": sep_slider, "coh_slider": coh_slider, "align_slider": align_slider,
                       "sep_rad_slider": sep_rad_slider, "avoid_slider": avoid_slider, "sep_out": sep_out,
                       "coh_out": coh_out, "align_out": align_out, "sep_rad_out": sep_rad_out, "avoid_out": avoid_out}

    return slider_settings


def slider_update(slider_settings):
    # feeding slider values into simulation parameters
    actors.separation_strength = slider_settings["sep_slider"].getValue()  # 7.0 (yep, dem is birds, alright)
    actors.cohesion_strength = slider_settings["coh_slider"].getValue()  # 3.0
    actors.alignment_strength = slider_settings["align_slider"].getValue()  # 3.5
    actors.separation_radius = slider_settings["sep_rad_slider"].getValue()
    actors.avoidance_strength = slider_settings["avoid_slider"].getValue()

    # each following drawing command draws on top of previous ones (so, leave widgets.update on top)
    slider_settings["sep_out"].setText(actors.separation_strength)
    slider_settings["coh_out"].setText(actors.cohesion_strength)
    slider_settings["align_out"].setText(actors.alignment_strength)
    slider_settings["sep_rad_out"].setText(actors.separation_radius)
    slider_settings["avoid_out"].setText(actors.avoidance_strength)


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
            pg.draw.circle(display, (0, 0, 255), obstacle.pos, obstacle.rad)


def main(sim, fps, window_size):
    """Main function"""

    pg.init()
    display = pg.display.set_mode(window_size)
    clock = pg.time.Clock()

    slider_settings = setup_sliders(display)

    mouse_circle = None

    # Main game loop
    while True:
        # Get all events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                if mouse_circle is not None:
                    sim.delete_obstacles(mouse_circle)
                mouse_pos = pg.mouse.get_pos()
                mouse_circle = Circle(mouse_pos, 20)
                sim.add_obstacles(mouse_circle)

        display.fill(WHITE)
        dt = clock.tick(fps)

        slider_update(slider_settings)

        sim.step(dt)
        draw_actors(sim, display)
        draw_obstacles(sim, display)

        pg_widgets.update(events)

        pg.display.update()


if __name__ == "__main__":
    res = (1080, 720)
    sim_test = Simulation(res)
    sim_test.setup(nboids=50)

    main(sim=sim_test, fps=30, window_size=res)
