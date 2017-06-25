# huntsim
A simple simulation of animals hunting written in pygame.

Top-down 2D tile based map with animals represented by coloured squares. 
Deer eat grass. Tigers hunt deer. Tigers hide in forests. 
The distribution of grass, forest and neutral tiles is randomly generated (Voronoi map generation).

Animals are controlled by AI. 
AI is implemented as a static Keras neural network.
Let's see what happens!

Implemented:
- Map generator
- Creature class to populate map with tigers and deer
- Vision system - each creature can see a 5x5 area of the map around them
- Brains - each creature has 65 neuron neural network (no training)
- Game loop - check for collisions, move creatures, pass new vision information, update screen.
- Pseudo-DNA generation - each network has weights that are initially generated from a randomised binary sequences, which are stored as strings.

To-do:
- Genetic algorithm - fitness assessment determines which animals will breed, then by manipulation of a pair of DNA sequences offspring are generated.
