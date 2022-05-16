import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(i, sim, dt_animate):
    boids = sim.actors
    obstacles = sim.obstacles

    plt.clf()  # clear axis, if axis should change

    for boid in boids:
        xp = boid.pos[0]
        yp = boid.pos[1]
        xv = boid.v[0]
        yv = boid.v[1]

        plt.scatter(xp, yp, c="black")
        plt.plot([xp, xp+xv], [yp, yp+yv], color="black")

    for obstacle in obstacles:
        obstacle.plot(plt)

    plt.tight_layout()
    sim.run(1, dt_animate)


def main(sim, fps):
    # create a figure with matplotlib
    # fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    #
    # # force equal aspect ratio
    # ax.set_aspect("equal")
    #
    # # grid overlay
    # ax.grid(False)

    dt_main = 1/fps

    ani = FuncAnimation(plt.gcf(), animate, frames=200, fargs=(sim, dt_main))
    # frames = <number of total frames to animate>

    plt.tight_layout()
    ani.save("boids_vel.gif", writer="pillow")  # This step takes very long - wihtout it, runtime < 1sec
