# Simulation of 'Boids' - studying emergence of complex group behaviour from simple algorithms

created on Montag, 2.5.2022
Authors: Daniel, Jacqueline

This is the git (GitHub) repository for the ESC202 (spring 2022) simulations project phase.

PDFs, organisation, coordination: refer to Ms Teams, instant messengers, and this README maybe.

Useful links:
- [course website](https://www.ics.uzh.ch/~stadel/doku.php?id=spin:esc202_fs2022)
- [course's page in the UZH course catalogue](https://studentservices.uzh.ch/uzh/anonym/vvz/?sap-language=EN&sap-ui-language=EN#/details/2021/004/SM/50031436)
> Selbstständiges Durchführen eines Programmierprojektes während des Semesters und Präsentation in einem 15-20 minütigen Vortrag in der letzten Semesterwoche.
> Das Thema kann selbst gewählt werden. **Die Präsentation soll wie folgt gegliedert sein**: Aufgabenstellung und Motivation, Lösungsideen, Mathematisierung, Algorithmus, Programmstruktur, Programmdemonstration.

## Done
algorithms:
- flocking behaviour works well
- efficient computation
- obstacle avoidance (incl. coundary conditions)

live animation
- live pygame animation
- rotating boids
- proxy of current velocity implemented? (stretching boid icons?)
- pygame plotting solved?

## To Be Done
animation:
- live parameter sliders
- mouse interface
- ()boids have acceleration vectors, visualising boids' intention

## Discuss / Possibilities
- numba.jit optimisation (see the [Deprecation Notices](https://numba.pydata.org/numba-doc/latest/reference/deprecation.html?highlight=list%20deprecation) of the Numba documentation page
  - necessary with nboids > 50 (fps aim 30 stable)

## Talk (Presentation)
15-20 minutes talk seems appropriate.

### 1. Aufgabenstellung und Motivation
How can complex behaviours like swarming/flocking in swallows or herding in sheep arise?
Can we reproduce and verify previous work on these questions, suggesting that complex behaviour can emerge from a simple set of rules?  
'Boids' seemed like an easily accessible model to investigate these questions.

#### potential Bonus section at the end
Could we make a couch 2 or even multiplayer game out of it? (refer to swarm control paper)
- real world applications?
- spin-offs?
- code adaptability? (plug our code into your simulation and get better grades!)

### 2. Lösungsideen
Class structures for animaloid actors, interactive live animations with sliders for model parameters and additional features

### 3. Mathematisierung
refer to literature (the original one probably suffices, pretty chill prof.s)

### 4. Algorithmus
refer to formula ruleset?

### 5. Programmstruktur
refer to some visual graph-like debugging tool (like in VR)?

### 6. Programmdemonstration
demonstrate interactive animation
offer audience interaction (anyone wanna have a go? can you beat the devs score? fork us on github, donate, etc.)
