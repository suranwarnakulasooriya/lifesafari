# LifeSafari
A program that simulates any life-like grid-based cellular automaton.

## Discover and Catalogue New Life
Conway's Game of Life is the most famous life-like grid-based cellular automaton. The rules of the game can be condensed into two: the conditions under which dead cells comes to life and under which living cells stay alive. This information can be condensed into a rulestring, which in this case is B3/S23, meaning dead cells come to life with 3 live neighbors and living cells stay alive with 2 or 3 live neighbors. This program generates random rulestrings and applies them to a randomly generated collection of cells, showcasing any possible life-like automaton.

## Usage
The program's arguments are
| flag | name        | type | description                                                                    | default   |
|------|-------------|------|--------------------------------------------------------------------------------|-----------|
| -r   | -rulestring | str  | rulestring in B{#...}/S{#...} format                                           | B3/S23    |
| -d   | -dimension  | int  | number of cells that make up the side length of the square grid                | 200       |
| -f   | -fullscreen | bool | spawn cells across the entire grid, keep off for rule sets that exhibit growth | False     |
| -a   | -age        | bool | change the color of live cells based on how long they've been alive            | False     |
| -s   | -seed       | int  | random seed to replicate exact simulations                                     | random    |
| -b   | -background | str  | color of dead cells (matplotlib color)                                         | black     |
| -c   | -colormap   | str  | color map of live cells (matplotlib color)                                     | rainbow_r |

`-rulestring` can also take the following special inputs
| option   | description                                                                                                   |
|----------|---------------------------------------------------------------------------------------------------------------|
| random   | generates a completely random rulestring using the seed                                                       |
| lifelike | same as random but ensures that the numbers in B and S are consecutive, for more realistic life-like behavior |
| pick     | picks a rulestring from a hard-coded dictionary of named rulestrings                                          |
| *name    | the name of any hard-coded rulestring is also valid, e.g. `-r 'Ant Colony'` will be read as B3/S234           |
