# huntsim
A simple simulation of animals hunting written in pygame.

Top-down 2D tile based map with animals represented by coloured squares. 
Deer eat grass. Tigers hunt deer. Tigers hide in forests. 
The distribution of grass, forest and neutral tiles is randomly generated (Voronoi map generation).

Animals are controlled by AI. 
AI is implemented as a static state machine with a genetic algorithm for optimisation.
Let's see what happens!

Implemented:
- Map generator
- Creature class to populate map with tigers and deer
- Game loop - check for collisions, move creatures, pass new vision information, update screen.
- Vision system - each creature can see a 5x5 area of the map around them.
- Pseudo-DNA generation - creature 'DNA' dictates the response to every possible vision state.
- Genetic algorithm - fitness assessment determines which animals will breed, then by manipulation of a pair of DNA sequences offspring are generated.

To-do:
- Optimising fitness function 
- Meta-training - exploring the parameter space for things like mutation rate and weightings in the fitness function to find optimal values