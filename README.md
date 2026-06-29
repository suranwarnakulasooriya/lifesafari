# LifeSafari: Discover and Catalogue New Life
A program that simulates any life-like grid-based cellular automaton.

Conway's Game of Life is the most famous life-like grid-based cellular automaton. The rules of the game can be condensed into two: the conditions under which dead cells comes to life and under which living cells stay alive. This information can be condensed into a [rulestring](https://conwaylife.com/wiki/Rulestring), which in this case is B3/S23, meaning dead cells come to life with 3 live neighbors and living cells stay alive with 2 or 3 live neighbors. This program generates random rulestrings and applies them to a randomly generated collection of cells, showcasing any possible life-like automaton.

## Usage
Make sure that `savedlifes.json` is in the same directory as the program file so it can access the premade list of interesting rulestrings (taken from [LifeWiki](https://conwaylife.com/wiki/List_of_Life-like_rules)). 
The program's arguments are
| flag | name        | type | description                                                                    | default   |
|------|-------------|------|--------------------------------------------------------------------------------|-----------|
| -r   | --rulestring | str  | rulestring in B{#...}/S{#...} format                                           | B3/S23    |
| -d   | --dimension  | int  | number of cells that make up the side length of the square grid                | 200       |
| -f   | --fullscreen | bool | spawn cells across the entire grid, keep off for rule sets that exhibit growth | False     |
| -a   | --age        | bool | change the color of live cells based on how long they've been alive            | False     |
| -s   | --seed       | int  | seed for random number generation                                     | random    |
| -b   | --bgcolor | str  | color of dead cells (matplotlib color)                                         | black     |
| -c   | --colormap   | str  | color map of live cells (matplotlib color)                                     | rainbow_r |
| -l   | --list       | bool | print all named rulestring from the save file and exit                                     
| -n   | --newname    | str  | save a rulestring with an associated name (two arguments) to the save file and exit

`--rulestring` can also take the following special inputs
| option   | description                                                                                                   |
|----------|---------------------------------------------------------------------------------------------------------------|
| random   | generate a completely random rulestring using the seed                                                       |
| lifelike | same as random but ensures that the numbers in B and S are consecutive, for more realistic life-like behavior |
| pick     | pick a rulestring from the save file                                        |
| [name]   | the name of any saved rulestring (not case sensitive) e.g. `-r ant colony` will be read as B3/S234           |

The controls for the simulation are
| key   | action                                                      |
|-------|-------------------------------------------------------------|
| SPACE | toggle pause                                                |
| a     | toggle showing cell age (same as -a)                        |
| c     | toggle spawning cells in the middle of the grid only        |
| r     | restart simulation with same seed                           |
| n     | restart simulation with new seed (overwrites previous seed) |
| ESC   | close simulation                                            |
