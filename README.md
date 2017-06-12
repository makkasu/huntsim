# huntsim
A simple simulation of animals hunting written in pygame.

Top-down 2D tile based map with animals represented by coloured squares. 
Deer eat grass. Tigers hunt deer. Tigers hide in forests. 
The distribution of grass, forest and neutral tiles is randomly generated (Voronoi map generation).

Animals are controlled by AI. 
AI is implemented as a static Tensorflow neural network.
Let's see what happens!

Implemented:
- Map generator
- Simple game loop with a controlable tiger
- Added killable deer

To-do:
- Add vision system
- Add health/energy system
- Implement AI
