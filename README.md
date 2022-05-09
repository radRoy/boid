
# Simulation of 'Boids' - studying emergence of complex group behaviour from simple algorithms

created on Montag, 2.5.2022
Authors: Daniel, Jacqueline

This is the git (GitHub) repository for the ESC202 (spring 2022) simulations project phase.

PDFs, organisation, coordination: refer to Ms Teams, instant messengers, and this README maybe.

For reference, here is the [course website](https://www.ics.uzh.ch/~stadel/doku.php?id=spin:esc202_fs2022).

For reference, here is the [course's page in the UZH course catalogue](), where this description of the project assessment is located:
> Selbstständiges Durchführen eines Programmierprojektes während des Semesters und Präsentation in einem 15-20 minütigen Vortrag in der letzten Semesterwoche.
> Das Thema kann selbst gewählt werden. Die **Präsentation soll** wie folgt gegliedert sein:
> 1. Aufgabenstellung und Motivation,
> 2. Lösungsideen,
> 3. Mathematisierung,
> 4. Algorithmus,
> 5. Programmstruktur,
> 6. Programmdemonstration.

## official task until Montag, 9.5.2022

Nail down the project topic and description. It's no problem to completely change the topic in the meantime (just communicate it and get help if needed). This means, we need some description of:
> 1. Aufgabenstellung und Motivation:  
> - How can complex behaviours like swarming/flocking in swallows or herding in sheep arise?  
> - Can we reproduce and verify previous work on these questions, suggesting that complex behaviour can emerge from a simple set of rules?  
> 'Boids' seemed like an easily accessible model to investigate these questions.

### our goals

If boids is the way to go:

- `Boid` class: TBD: testing flocking behaviour with animation

- animation: TBD (make things work) interactive sliders for input parameters (like field of view (FOW) angle, cohesion strength, etc.), mouse interface would be nice to have already maybe to play around and explore possibilities.
  - show a boid as a pointy triangle
  - boids have velocity vectors
    - () acceleration vectors could be interesting, showing where the boid wants to go


- pygame, good start: [some yt video](https://www.youtube.com/watch?v=cFq3dKa6q0o), pygame looks quite simple to get up and running, compared to matplotlib (use `pip install pygame` in the boid conda env on windows to install without error (version 2.1.2 or so)).


- **[matplotlib.animation.ArtistAnimation](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.ArtistAnimation.html) Animation using a fixed set of Artist objects. - *not suitable*** for our purpose (unfortunately what I am more familiar with).
- **[matplotlib.animation.FuncAnimation](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html#matplotlib.animation.FuncAnimation) makes an animation by repeatedly calling a function func. - suitable for endless live interactive animation.**
- [nice yt tutorial](https://www.youtube.com/watch?v=Ercd-Ip5PfQ)


- [matplotlib interactive functions](https://matplotlib.org/stable/gallery/event_handling/ginput_manual_clabel_sgskip.html)
- [matplotlib animation doc. page](https://matplotlib.org/stable/gallery/index.html#animation)
- [interactive figures](https://matplotlib.org/stable/users/explain/interactive.html) sounds promising
  - "For the figures to be responsive to mouse, keyboard, and paint events, the GUI event loop needs to be integrated with an interactive prompt. We recommend using IPython (scroll down in website)."
  - "PyCharm, Spyder, and VSCode: Many IDEs have built-in integration with Matplotlib, please consult their documentation for configuration details."



### things to discuss

- POSTPONE "We like things that make us go fast.", i.e., to `jit` or not to `jit`?
  - or even to `jitclass`?
  - both cases: beware so-called `reflected lists` and the like (see the [Deprecation Notices](https://numba.pydata.org/numba-doc/latest/reference/deprecation.html?highlight=list%20deprecation) of the Numba documentation page
- More/Less organisation? How to proceed?
  - fine, faster
- conda python environment:
  - [conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html): You can also share your environment with someone by giving them a copy of your `environment.yaml` file.
  - [conda: managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
  - need library `heapq`? how to install? not in pycharm's default repository list.

### progress report

- [matplotlib.widget example (sliders)](https://matplotlib.org/stable/gallery/widgets/slider_demo.html#sphx-glr-gallery-widgets-slider-demo-py) - works without pycharm (conda environment via anaconda prompt works 1st try)

## official task until Montag, 16.5.2022
.

## official task until Montag, 23.5.2022
.

## official task until Montag, 30.5.2022
... presentation?

## Code files provided for initial animation setup

Daniel: So far, stuff in `archive` folders are ones I might have taken code from.

## By The Way

ESC202 = Simulations in the Natural Sciences 2 (sins2)

## Thoughts?
