"""
code source: https://matplotlib.org/stable/gallery/animation/double_pendulum.html#sphx-glr-gallery-animation-double-pendulum-py
code source: slider_demo.py (also from matplotlib examples)"""

from inspect import trace
import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()

PI = np.pi

def increment_phi(angle):
    angle = (angle + PI/90) % (2*PI)
    return angle

def update_plot(frame, r, phis, xs, ys):
    phi = increment_phi(phis[-1])
    x = np.cos(phi) * r  # INSERT SLIDERS HERE (for r)
    y = np.sin(phi) * r  # INSERT SLIDERS HERE
    
    phis.append(phi)
    xs.append(x)
    ys.append(y)

    line.set_data(x, y)
    trace.set_data(xs, ys)
    
    return line, trace

fps = 30
phi = 0.  # angle (radians)
phi_list = [phi]
trace_x = []
trace_y = []
radius = 1.  # make into matplotlib.widget.Slider later

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect("equal")
ax.grid()
plt.tight_layout()

line, = ax.plot([], [], "o", lw=2)  # MUST SET A MARKER TYPE (fmt), e.g. "o" for points - else will not actually draw anything
trace, = ax.plot([], [], '.-', lw=1, ms=2)

ani = FuncAnimation(fig=plt.gcf(), func=update_plot, frames=itertools.count, fargs=(radius, phi_list, trace_x, trace_y), interval=1000/fps)
# passing None to frames is equivalent to passing itertools.count (just counts upwards)

plt.show()
# ani.save("slider_live_test.mp4")  # just saves animation with slider settings as is when window was closed, probably runs for default duration with default frame number

"""
Live animation could be implemented with button presses (pause, resume, stop). Although VS Code already includes some functions (pane, zoom, reset fov, stop (close window), etc.)
"""
