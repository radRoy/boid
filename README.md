# Simulation of 'Boids' - studying emergence of complex group behaviour from simple algorithms

created on Montag, 2.5.2022
Authors: Daniel, Jacqueline

This is the git (GitHub) repository for the ESC202 (spring 2022) simulations project phase.

PDFs, organisation, coordination: refer to Ms Teams (if possible).
	- Daniel: I like to write all this stuff in the `README.md` file. GitHub and other git GUIs nicely mark the additions and deletions for easy tracking of changes. Also, the Teams/... chat is not overflown, then, too.

## official task until Montag, 9.5.2022

Nail down the project topic and description. It's no problem to completely change the topic in the meantime (just communicate it and get help if needed).

If boids is the way to go:

- animation: interactive sliders for input parameters (like field of view (FOW) angle, cohesion strength, etc.), mouse interface would be nice to have already maybe to play around and explore possibilities.
- `Boid` class: <@Jacqueline, bitte deine Zielsetzung grob umschreiben>
- joint: working interface of data structures, calculations and animations.

### things to discuss

- "We like things that make us go fast.", i.e., to `jit` or not to `jit`?
    - or even to `jitclass`?
    - both cases: beware so-called `reflected lists` and the like (see the [Deprecation Notices](https://numba.pydata.org/numba-doc/latest/reference/deprecation.html?highlight=list%20deprecation) of the Numba documentation page
- More/Less organisation? How to proceed?
- What python version to use (ideally the same one)? 
  - Use of a **virtual environment** (see the [course website](https://www.ics.uzh.ch/~stadel/doku.php?id=spin:esc202_fs2022) for recommended/common approaches) might be most appropriate for our use case.
    - I currently use `conda` environments (friendly towards science stuff and other things 'up my alley')

## official task until Montag, 16.5.2022
.

## official task until Montag, 23.5.2022
.

## official task until Montag, 30.5.2022
... presentation?

## Code files provided for initial animation setup

Daniel: The folders `archive`, etc.: **currently not in use**. So far, these are `.zip`s of previous states of code backups when having reached a milestone of sorts. These scripts are the ones I might have taken code from (ideally the sources in general are stated in the comments or at the top of the files, etc.).
- the files sph_...ani...py are animation testing related. should be easy to extract animation code out of it and plug in another class structure.
	- library `heapq` - how to install? not in pycharm's default repository list.

## By The Way

ESC202 = Simulations in the Natural Sciences 2 (sins2)

## Thoughts?
