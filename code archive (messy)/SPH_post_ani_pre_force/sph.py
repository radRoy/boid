#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name:      Walther, Daniel M.
Email:     daniel.walther@uzh.ch
Date:      1500, 21.3.2022
Kurs:      ESC202
Semester:  FS22
Week:      5, 6, 7
    5: sph square box with periodic BC for all boundaries
    6: sph wind tunnel with periodic BC for y-axis (tunnel width), ghost regions before & after tunnel for x-axis (tunnel length)
    7: 2D Ising (done) + generous extension of week 6 deadline.
        7.1 2D-Ising Model (done)
        7.2 sph 2D square box
            .1: animation for scatterplot + colormap combo.
            .2: leapfrog calculation of particle movements and interaction forces
            .3: create initial perturbation (like a Sedov-Taylor blast wave (like density super high, just some extreme starting value))
        7.3 sph 2D wind tunnel
            .x: look at my lecture notes - then decide on the sub tasks
TA:        Sebastian Schulz, sebastian.schulz@uzh.ch

Note (from treebuild week): NEVER USE if ... is None, for the time being (like half a year) - it breaks some stuff in very weird way... (probably py3.11 thing...)
"""

# Priority Queue (sentinel = most useful snippet, all else easier with doc.)
# retro update: sentinel was not needed so far.
"""
# https://docs.python.org/3/library/heapq.html
# Use a tuple (key, data) for one element (i.e., for a cell or particle to be pushed to the queue).
# (see https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes) - wrapper classes mentionend as impl. option
sentinel = (0, None)
"""


#%% libraries, imports

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from heapq import *

#%% classes

# Cell aka box, names may be inconsistently used
class Cell(object):
    # initialise a Cell object, with leaf cells containing at most 8 particles, can contain no particles.
    def __init__(self, rmin, rmax, lower, upper):
        self.rmin_ = np.copy(rmin)  # float np.array: pos. vector in global Cell
        self.rmax_ = np.copy(rmax)
        self.centre_ = (self.rmin_ + self.rmax_) / 2
        self.iLower = lower  # int index for p. array (same for all dim.s)
        self.iUpper = upper
        self.lchild = None  # left branch, None if this is leaf
        self.rchild = None  # right branch
        self.count = self.iUpper - self.iLower + 1  # came in handy. can (should) be int from 0 to N (N <= 8 if it is leaf Cell)
        self.isleaf = self.count < 9


class Particle(object):
    # assume k is not bigger than total N of particles

    N_particles = 0

    def __init__(self, r_):
        Particle.N_particles += 1
        # self.ID = 0  # later (in main_sph) defined as its index in the particle array (should be unique (DEBUG TEMP))
        # self.knn() stuff
        self.cq = []  # heapq
        self.pq = []  # heapq

        # physical variables
        self.r_ = r_  # np.array: position vector, with a coordinate (float) for each dimension
        self.v_ = np.zeros_like(r_)  # np.zeros_like(x) returns float or int, just like x's contents
        self.e = 0.  # energy
        self.c = 0.  # speed of sound (prob. based on gas equ. from lec.)
        self.rho = 0.  # mass density [mass/area] construct (float!)
        # self.knn() related
        self.h = 0.  # kernel size (previously self.d2max), defined within self.knn()

        # need to calculate:
        self.a_ = np.zeros_like(r_)  # "start with a=0 for all particles"
        self.dedt = 0.

        # 2 extra temp. variables (for leapfrog-like algorithm)
        self.v_pred_ = np.zeros_like(r_)  # temp. var. for integration step (I think)
        self.e_pred = 0.  # temp. var. for integration step (I think)

        #self.h = defined above

    def fill_cq(self, a, c):
        if c.isleaf:
            dist = boxdist(c.centre_, c.rmax_ - c.centre_, self.r_)
            self.cq.append((dist, c))  # quicker way, heapq doc: quicker to once do heapq afterwards than build the heap with heappush.
        else:
            self.fill_cq(a, c.lchild)
            self.fill_cq(a, c.rchild)

    # uses lib. heapq, only min heaps in lib.; most distant = highest priority => Kehrwert der Dist. in partq nehmen
    def fill_pq(self, a, radius):
        # need only cellq, not entire a - don't pop until have k particles after cq loop

        # p_count = 0
        for c_tuple in self.cq:
            c_dist, c = c_tuple[0], c_tuple[1]
            if c_dist > radius:
                continue
            for p in a[c.iLower : c.iUpper+1]:
                if p in self.pq or p == self:
                    continue
                p_dist = self.d2(p)
                if p_dist < radius:
                    self.pq.append((1/p_dist, p))  # d2_pbc done with pbc

    # knn of this p. instance, lib. heapq is practical. default min heap, max heap not findable as setting.
    def knn(self, a, k, root, radius):
        if k > Particle.N_particles:
            print(f"Caution, given k is invalid, can not have more neighbours than there are simulated particles. return")
            return
        self.fill_cq(a, root)
        heapify(self.cq)
        self.fill_pq(a, radius)
        # assumes k <= N_particles
        while len(self.pq) < k: # should take about 2 or 3 iterations maybe, often just one.
            self.fill_pq(a, radius=radius*1.5)
        heapify(self.pq)
        if len(self.pq) > k:
            del self.pq[k:]
        self.h = 1 / self.pq[0][0]  # = kernel size
        self.cq, self.pq = np.array(self.cq), np.array(self.pq)

    # (with pbc) euclidean squared distance between this and another Particle
    def d2(self, p):
        L = 1.
        d2 = 0.
        for d in range(2):
            dist = self.r_[d] - p.r_[d]
            if dist < 0:
                dist_pbc = dist + L
            else:
                dist_pbc = dist - L

            dist = abs(dist)
            dist_pbc = abs(dist_pbc)
            if dist < dist_pbc:  # direct distance is smaller, in dimension d
                d2 += dist ** 2
            else:  # pbc distance (accross boundary) is smaller, in dimension d
                d2 += dist_pbc ** 2
        return d2

    # (with pbc) brute force knn algorithm, in-place, no return
    def knn_brute(self, a, k):
        self.pq_p = []  # list of the knn particles
        self.pq_d2 = []  # list of the squared distances to the knn particles
        self.cq_c = []  # same but for cells
        self.cq_d2 = []
        for i in range(k):
            d2min = float('inf')  # pseudo distance to compare to
            for q in a:
                if self != q and q not in self.pq_p:
                    d2 = self.d2(q)
                    if d2 < d2min:
                        d2min = d2
                        qmin = q
            # "Here pq_p and pq_d2 lists for Particle p are filled. Compare with the lists from the recursive knn algorithm."
            # assume there exist qmin and d2min
            self.pq_p.append(qmin)
            self.pq_d2.append(d2min)
        self.h = d2min

    # returns (monaghan kernel) mass density of its Particle instance
    def density_monaghan(self):
        sigma = 40 / (7 * np.pi)  # normalising constant in 2D space
        m = 1.  # mass of another Particle (later iterate over this, when mass is instance variable)
        h = self.h
        for r in 1/self.pq[:,0]:
            if 0. <= r/h < .5:
                monaghan = 6 * (r/h)**3 - 6 * (r/h)**2 + 1
            elif .5 <= r/h <= 1:
                monaghan = 2 * (1 - (r/h))**3
            else:  # if r_/h > 1, this should never be the case, though. just from the mathematical background of the Kernel invented by Monaghan and his colleague.
                monaghan = 0.
            w_mon = sigma / (h**2) * monaghan
            self.rho += m * w_mon

    # returns (symmetrised Benz kernel) mass density of its Particle instance
    def density_Benz_symm(self):
        # sigma = 40 / (7 * np.pi)  # normalising constant in 2D space
        # m = 1.  # mass of another Particle (later iterate over this, when mass is instance variable)
        # h = self.h
        # for r in 1/self.pq[:,0]:
        #     if 0. <= r/h < .5:
        #         monaghan = 6 * (r/h)**3 - 6 * (r/h)**2 + 1
        #     elif .5 <= r/h <= 1:
        #         monaghan = 2 * (1 - (r/h))**3
        #     else:  # if r_/h > 1, this should never be the case, though. just from the mathematical background of the Kernel invented by Monaghan and his colleague.
        #         monaghan = 0.
        #     w_mon = sigma / (h**2) * monaghan
        #     self.rho += m * w_mon
        self.density_monaghan()  # TBD (leave until ohter physics work)

#%% functions

# random generation of an array with Particle objects (their position is randomly generated).
def gen_part_array(N, n_dim):
    return np.array([Particle(r_=np.random.random(n_dim)) for i in range(N)])

def partition(a, il, ir, v=None, d=0):
    """
    Partitions an array of Particle objects into 2 partitions, lower and upper, by changing their place in the array, but not changing the position attributes of the particles. Returns the index of the 1st upper Particle in the partitioned array.

    :param a: numpy.ndarray containing Particle objects (expecting unsorted, unpartitioned array).
    :param il: int index of the first Particle to include in partitioning.
    :param ir: int index of the last Particle to include in partitioning.
    :param v: float value of the split location in the given dimension d.
    :param d: int the dimension that is to be partitioned.
    :return: int The index of the Particle below or at the split value (in dimension d).
    """

    if len(a) == 0:
        print("no particles found (empty Particle array given).")
    if d >= len(a[0].r_):
        print("Invalid input: Invalid dimension chosen (not as many dimensions available).")

    # iLower or iUpper out of bounds
    if il >= len(a):
        print(f"iLower out of bounds (too high).")
    if il < 0:
        print(f"iLower out of bounds (too low).")
    if ir < 0:
        print(f"iUpper out of bounds (too low).")
    if ir >= len(a):
        print(f"iUpper out of bounds (too high).")

    # core algorithm to partition a Cell into two child cells
    while il <= ir:
        if a[il].r_[d] < v:
            il += 1
        else:  # swap a[iLower] with a[iUpper]
            a[il], a[ir] = a[ir], a[il]
            ir -= 1

    if il == len(a):
        print(f"All particles in left child Cell - iLower out of bounds by 1 (too high). return iLower={il}")
    if il == 0:
        print(f"All particles in right child Cell - Warning: All particles are above the split, upper index iUpper is now out of lower bounds by 1 index. return iLower={il}")
    if il == len(a) and il == 0:  # never know. might remove this later.
        print(f"Caution: This part should be unreachable! Save and restart your IDE!")

    return il  # 1st (would-be) upper Particle

def treebuild(a, c, d, n_dim=2):
    """
    In-place algorithm, changing variables from global scope.
    Recursively organises a cell object into a binary tree of cells, where the leafs each contain at most 8 particles

    :param a: array of particles (even though in-place algorithm, still need specific. of array to change in-place)
    :type a: np.ndarray of Particle objects
    :param c: current root cell (recursive)
    :type c: Cell
    :param d: the current dimension to partition in (alternate between all dimensions)
    :type d: int
    :return: nothing, plot a graphical representation of the tree structure
    :rtype: None
    """

    if c.count > 8:
        v = 0.5 * (c.rmin_[d] + c.rmax_[d])
        split = partition(a, c.iLower, c.iUpper, v, d)

        rmax_ = np.copy(c.rmax_)
        rmax_[d] = v
        left = Cell(np.copy(c.rmin_), rmax_, c.iLower, split - 1)
        c.lchild = left

        rmin_ = np.copy(c.rmin_)
        rmin_[d] = v
        right = Cell(rmin_, np.copy(c.rmax_), split, c.iUpper)
        c.rchild = right

        # should work for n dimensions
        treebuild(a, c.lchild, (d+1) % n_dim, n_dim)
        treebuild(a, c.rchild, (d+1) % n_dim, n_dim)

# boxdist function (returning distance from a point to the Cell boundaries), but with periodic BC
def boxdist(c, b, p):
    """c,b,p: 2D pos. vectors: cell centre_, cell halfdiagonal (rmax_), a point. returns minimal distance from point p to boundary of cell with attr. c & b.
    c = coordinates of cell centre, b = diff. rmax - centre = length of halfdiagonal, p = coordinates of some point"""

    L = 1.  # the length & width of the global Cell (in one dimension, assumes equal boundary lengths in all dimensions) - should work for non-quadratic fields, too.
    d2 = 0.
    for d in range(2):  # 2 for 2 space dimensions
        t = c[d] - p[d]
        if t < 0:
            t_per = t + L
        else:
            t_per = t - L

        t = abs(t) - b[d]
        t_per = abs(t_per) - b[d]
        t = min(t, t_per)
        if t > 0:
            d2 += t * t
    # intention of use: compare d2 with a radius (distance), see whether box intersects with radius.
    return d2

# write (Rattenschwanz ass. week 5)
def knn_density(particles):
    """for all p.: calculates mass density within a particles kernel size (knn-radius)"""
    for p in particles:
        p:Particle
        p.density_Benz_symm()  # TBD (just does monaghan for now)

def drift1(dt, particles):
    """for all p.: 1st half-drift => position at halfstep, velocity_temp, energy_temp
    (temp var.s needed for calcforce(), calcforce() needed for acceleration_halfstep)"""
    for p in particles:
        p:Particle
        p.r_ += p.v_ * dt
            # r.5_ += v0_ * dt/2
            # r.5_ = r0_ + v0_ * dt/2 (source: dmw(c).hs2019.sins1.week5(solarsys))
        p.v_pred_ = p.v_ + p.a_ * dt  # 1st order Euler approx.
        p.e_pred = p.e + p.dedt * dt  # 1st order Euler approx.

def kick(dt, particles):
    """for all p.: full kick from half-step position => velocity at full step (for 2nd half drift)"""
    for p in particles:
        p:Particle
        p.v_ += p.a_ * dt
            # v1_ += a.5_ * dt
            # v1_ = v0_ + a.5_ * dt (source: dmw(c).hs2019.sins1.week5(solarsys))
                # a.5_ = a_(at r.5_)
        p.e_ += p.dedt * dt

def drift2(dt, particles):
    """for all p.: 2nd half-drift => position at fullstep"""
    for p in particles:
        p:Particle
        p.r_ += p.v_ * dt
            # r1_ += v1_ * dt/2
            # r1_ = r.5_ + v1_ * dt/2 (source: dmw(c).hs2019.sins1.week5(solarsys))

def knn_density(particles):
    """for all p.: calculate density => p.roh (gather-scatter-scheme)"""
    for p in particles:
        p:Particle
        p.density_monaghan()  # switch with Benz density (TBD)
        # p.density_monaghan()  # switch with Benz density (TBD)

def calcsound(particles):
    # write (ass. week 5)
    for p in particles:
        p:Particle
        p.c = p.c  # TBD

def knn_sphforce(particles):
    """for all p.: at half-step, calculate acceleration and energy-time-derivative.
    Here the gather-scatter method for conservation of momentum (given different particle kernel sizes) is implemented."""
    for p in particles:
        p:Particle
        p.a_ = p.a_  # TBD
        p.dedt = p.dedt  # TBD

def calcforce(particles, cell, k, radius):
    # import
    treebuild(particles, cell, d=0)
    for p in particles:
        p:Particle
        p.knn(particles, k, cell, radius)
    knn_density(particles)  # treewalk, gather: all p: calculate p.roh

    # write
    calcsound()  # all particles
    knn_sphforce()  # treewalk, gather & scatter: all p: calculate p.acc_vec, p.de_dt

#%% plot functions - keep save=False in general  # maybe write main_plot() and adapt other plot f.s to take fig/ax inst.s

def plot_partition():
    print("See partition.py for the partition plotting code.")

# draws 2D cell tree
def plot_cell(a, root, ax):  # np.array, Cell, plt.figure, plt.axes

    if root != None:  # deprecated (only this line, not contained body)?
        if root.isleaf:
            # .count is the count of particles in root, from 0 to 8

            rmin, rmax = root.rmin_, root.rmax_
            # draw box of this Cell. adjust width & opacity
            ax.plot(
                [rmin[0], rmax[0], rmax[0], rmin[0], rmin[0]],
                [rmin[1], rmin[1], rmax[1], rmax[1], rmin[1]], linewidth = .5, alpha = .5)

            # only draws particles when there are any to draw
            if root.count:
                # (()TBD if bored: just for fun, check whether contained code would work for empty cells, too)
                p: Particle
                draw_a = np.array([[p.r_[0], p.r_[1]] for p in a[root.iLower:root.iUpper + 1]])
                    # assumes 2D space
                    # TBD check which indices are included or excluded

                # not essential, but keep for nostalgia and pondering
                """
                ax.plot()  # visualise contiguous memory by connecting memory-adjacent particles (= adj. in a, I assume) with lines
                #TBD later: connect last and first particles accross sibling leaf cells, just for fun (and insight into proper working of tree algorithm) - and might get more efficient way of kNN search out of it.
                """

                # points: draw the particles contained in this Cell
                ax.scatter(draw_a[:,0], draw_a[:,1], s=2)

        # makes that all left and right children get visited (exactly once)
        else:
            plot_cell(a, root.lchild, ax)
            plot_cell(a, root.rchild, ax)

# messy, traced back to ballwalk & densities, ill dur., revision approp.
def plot_ball(centre, radius, ax):
    # pBC vis. would be nice (if bored)

    x = np.linspace(0, 2*np.pi, 60)
    y = np.copy(x)
    x = centre[0] + radius*np.cos(x)
    y = centre[1] + radius*np.sin(y)
    ax.plot_density(x, y, linewidth=1, color='black')

# messy, traced back to ballwalk & densities, ill dur., revision approp.
def plot_tree(a, root, density=False, cells=False, ball=False, centre=np.array([.5, .5]), radius=.2, save=False):
    ax = plt.subplot(111)  # make figsize equivalent of plt.subplot() bigger than 10,10 (not essential)
    if ball:
        plot_ball(centre, radius, ax)
    """if density:
        draw_density(a, root, ax)"""
    if cells:
        # (recursive) tree traversal takes place (if root not None)
        plot_cell(a, root, ax)

    #plt.legend()
    if save:
        plt.savefig("image archive/tree_n_leafs_test.png")
    plt.show()

# plot density heatmaps with 8 surrounding copies (no mesh etc.)
def plot_density_pbc_check(ax, x, y, c, cmap="viridis", s=10, alpha=.8):
    ax.scatter(x, y, c=c, cmap=cmap, s=s, alpha=alpha)
    ax.scatter(x + 1, y, c=c, cmap=cmap, s=s, alpha=alpha)
    ax.scatter(x + 2, y, c=c, cmap=cmap, s=s, alpha=alpha)
    ax.scatter(x, y + 1, c=c, cmap=cmap, s=s, alpha=alpha)
    ax.scatter(x + 1, y + 1, c=c, cmap=cmap, s=s, alpha=alpha)
    ax.scatter(x + 2, y + 1, c=c, cmap=cmap, s=s, alpha=alpha)
    ax.scatter(x, y + 2, c=c, cmap=cmap, s=s, alpha=alpha)
    ax.scatter(x + 1, y + 2, c=c, cmap=cmap, s=s, alpha=alpha)
    return ax.scatter(x + 2, y + 2, c=c, cmap=cmap, s=s, alpha=alpha)

# plot desnity heatmaps - useful link: https://stackoverflow.com/questions/17682216/scatter-plot-and-color-mapping-in-python
def plot_density(a, save, bc, s=10, alpha=.8, show=False):
    # coordinates of particles
    rs = np.array([p.r_ for p in a])
    x, y = rs[:,0], rs[:,1]
    # densities at Particle locations
    rhos = np.array([ p.rho for p in a ])

    # set colormap of choice
    cmap='viridis'  # I say, smashing colours, indeed, are they not?

    # creating mappable colormap for fig (matplotlib keyword 'mappable')
    fig2, ax2 = plt.subplots(1,1)
    map1 = ax2.imshow(np.stack([rhos, rhos]), cmap)
    plt.close(fig2)  # output of ax.imshow() remains if stored in a variable.

    # plotting heatmap of Particle densities (mass/area)
    fig, ax = plt.subplots(1,1, constrained_layout=True)
    ax.set_aspect('equal')
    if bc:
        plot_density_pbc_check(ax, x, y, rhos, cmap, s=s, alpha=alpha)
    else:
        ax.scatter(x, y, c=rhos, cmap=cmap, alpha=alpha, s=s)
    fig.colorbar(map1, ax=ax)
    # triple AAA studio quality hotfix 99.99$  # lol, artefact, leave it for shits n grins
    """
    ax.set_title('brighter is denser')
    """

    if save:
        if bc: plt.savefig("image archive/rho_t0_monaghan_pbc.png")
        else: plt.savefig("image archive/rho_t0_monaghan.png")
    if show:
        plt.show()

# purpose TBD
def plot_sph():
    pass

#%% ()animation functions - delegating other functions for each frame (opt.1)

#%% main functions

def main_tree(N, n_dim):
    # for try_again in range(1):  # Debug: for testing plotting bugs
    a0 = gen_part_array(N, n_dim)  # random location
    a = np.copy(a0)

    ## Build the tree (for now in 2D space)
    rLow = np.array([0., 0.])  # position vector to n_dim-dimensional lower bound corner
    rHigh = np.array([1., 1.])  # position vector to n_dim-dimensional upper bound corner

    low = 0  # index of very first Particle in whole array
    upp = N - 1  # index of very last Particle in whole array

    root = Cell(rLow, rHigh, low, upp)
    dim = 0  # start dimension for splitting cells (first split), arbitrary but must be valid int (e.g. in 2D space)
    treebuild(a, root, dim, n_dim)
    # TBD check with plot function (should work, thought through fully)

    # centre_=np.array([.5, .5])
    # radius=.25
    # count = ball_walk(a, root, centre_, radius)
    # print(count)
    plot_tree(a, root, cells=True, save=False)  # ¡WHAT A FRICKING MESS! TBD

    print("- end of tree.py -")

def main_sph(particles, root, N, n_dim, rmin, rmax, wind_tunnel=False, k=32, N_steps=1, dur_step=1):
    if not wind_tunnel:
        # initiate a_ = dv_/dt = 0 for all particles.
        # have positions, velocities, knn
        # want densities (symmetrised Benz formulation density kernel)
        # want accelerations
        # etc. (deprecated)

        # final solutions for animation
        positions_t = []
        densities_t = []
        radius = abs(rmin[0] - rmax[0])**2 / N * k * 1.5

        ########## pseudo animation data creation for ani test ##########
        """
        positions_t.append(np.array(positions))
        densities_t.append(np.array(densities))
        for t in range(N_steps):  # whole thing works. pbc satisfied.
            # print(f"\nt={t}")
            positions = []
            densities = []

            for i in range(N):
                r_ = np.copy(particles[i].r_)
                r_ += .01  # works, temp pseudo change
                for j,coord in enumerate(r_):
                    if coord>1: r_[j] -= 1.
                positions.append(r_)
                densities.append(np.copy(particles[i].rho))
                particles[i].r_ = r_

            # print([pos for pos in positions])
            positions_t.append(np.array(positions))
            densities_t.append(np.array(densities))
        """

        ########## actual sph simulation below ##########
        # I think it should all work with 1 tree updated as I go (if all is implemented properly, else can do quickfix by copying the tree and have a (half-step) lagging cell tree)

        # drift1(dt=0)  # bootstrap step for v_vec_pred, e_pred
            # should not be necessary (see how Particle.__init__() was implemented)
        calcforce(particles, root, k, radius)
    
        for t in range(N_steps):
            drift1(dt=dur_step/2)  # stepsize is actually stepDuration
            calcforce(particles, root)
            kick(dt=dur_step)
            drift2(dt=dur_step/2)
        print("- sph.py: calculations done -")
        plot_sph()  # TBD
        print("- sph.py: plotting/animation(tbd) done -")

        positions_t = np.array(positions_t)
        densities_t = np.array(densities_t)
        return np.array(positions_t), np.array(densities_t)
    else:
        print("SPH wind tunnel not implemented yet.")
        return None

#%% name main
if __name__ == "__main__":
    np.random.seed(1)

    N = 100  # no. of total particles
    n_dim = 2  # no. of total spatial dimensions
    k = 32  # k nearest neighbours that interact
        # monaghan kernel: with larger k, becomes unstable...
    fps = 30
    N_steps = 5 * fps  # x * fps, where x = sec of video animated
    dur_step = .1  # step size (simulated time)

    # init stuff
    particles_t0 = gen_part_array(N, n_dim)
    a = np.copy(particles_t0)
    rmin, rmax = np.zeros(n_dim), np.ones(n_dim)
    root = Cell(rmin, rmax, 0, N-1)
    treebuild(a, root, 0, n_dim)

    # knn
    # ani test: pseudo change
    positions_t, densities_t = main_sph(a, root, N, n_dim, rmin, rmax, k, N_steps, dur_step)

    # variables with a trailing underscore_ are vectors, e.g., r_ is a positional vector, v_ is velocity vector, a_ is acceleration vector.

    # animate
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.set_aspect('equal')
    images = []
    for t,positions in enumerate(positions_t):
        # print(f"\nt={t}")
        images.append([ ax.scatter(positions[:,0], positions[:,1], c=densities_t[t], alpha=.8, s=10) ])

    ani = ArtistAnimation(fig, images)
    ani.save("ani_test_sph_densities.mp4", fps=fps)