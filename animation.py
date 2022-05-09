import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(i, sim, dt_animate):
    boids = sim.actors

    plt.clf()  # clear axis, if axis should change

    for boid in boids:
        xp = boid.pos[0]
        yp = boid.pos[1]
        xv = boid.v[0]
        yv = boid.v[1]

        plt.scatter(xp, yp, c="black")
        plt.plot([xp, xp+xv], [yp, yp+yv], color="black")

    plt.tight_layout()
    sim.run(1, dt_animate)


def main(sim, fps):

    dt_main = 1/fps
<<<<<<< Updated upstream
    ani = FuncAnimation(plt.gcf(), animate, frames=200, fargs=(Sim, dt_main,), interval=dt_main)
=======
    wait_duration = 1000/fps
    ani = FuncAnimation(plt.gcf(), animate, fargs=(sim, dt_main,), interval=wait_duration)
    # frames = <number of total frames to animate>
>>>>>>> Stashed changes

    plt.tight_layout()
    ani.save("boids_vel.gif", writer="pillow")  # This step takes very long - wihtout it, runtime < 1sec
