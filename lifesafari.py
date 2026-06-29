import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np
import argparse
import json

def get_random_rules(lifelike=False):
    '''Create a random rulestring.'''
    b = np.array(list(range(0,9)))
    s = b.copy()
    if lifelike:
        b_a = np.random.randint(0,9,dtype=int)
        if b_a < 8:
            b_b = np.random.randint(b_a,9,dtype=int)
        else:
            b_b = 9
        s_a = np.random.randint(0,9,dtype=int)
        if s_a < 8:
            s_b = np.random.randint(s_a,9,dtype=int)
        else:
            s_b = 9
        b = b[b_a:b_b+1]
        s = s[s_a:s_b+1]
    else:
        bm = np.random.randint(0,2,size=9,dtype=int)
        sm = np.random.randint(0,2,size=9,dtype=int)
        b *= bm
        s *= sm
    bf = ''.join(map(str,b)).replace('0','')
    sf = ''.join(map(str,s)).replace('0','')
    
    return f'B{bf}/S{sf}'

def read_rules(rule_set,nts,default='B3/S23'):
    '''Parse ruleset from given rulestring, default to B3/S23 if invalid.'''
    if rule_set in list(nts.keys()):
        return read_rules(nts[rule_set],nts)
    rules = list(rule_set)
    if rules[0] == 'B' and '/S' in rule_set:
        rules.pop(0)
        rules.remove('/')
        rules.remove('S')
        try:
            _ = [int(i) for i in rules] # check if every character is an integer
            born = rule_set[1:rule_set.index('/')]
            if born != '':
                for b in born:
                    rules.remove(b)
                survive = rules[:]

                # create and return properly formatted rulestring
                born = tuple(set(sorted(tuple([int(b) for b in born]))))
                survive = tuple(set(sorted(tuple([int(s) for s in survive]))))
                return (born,survive)

        except ValueError:
            pass
    # default to Conway 
    print(f'! Rulestring "{rule_set}" could not be parsed')
    return read_rules(default,nts)

def get_neighbors(position,g=None):
    '''Get indices of neighbors of a given cell index, or their values if grid is also given.'''
    row, col = position
    n = (row - 1) % gamesize
    s = (row + 1) % gamesize
    e = (col + 1) % gamesize
    w = (col - 1) % gamesize
    if g is not None:
        return [g[n,col], g[n,e], g[row,e], g[s,e], g[s,col], g[s,w], g[row,w], g[n,w]]
    return [(n,col), (n,e), (row,e), (s,e), (s,col), (s,w), (row,w), (n,w)]

def get_all_check(L):
    '''Get list of all live cells and their neighbors.'''
    N = []
    for cell in L:
        N += get_neighbors(cell)
    return list(set(N+L))

def get_next_state(cell,g,rule_set):
    '''Find if the given cell will be 0 or 1 in the next tick.'''
    n_live_neighbors = sum(get_neighbors(cell,g))
    r,c = cell
    if not g[r,c] and n_live_neighbors in rule_set[0]: # cell is born
        return 1
    elif g[r,c] and n_live_neighbors in rule_set[1]: # cell survives
        return 1
    return 0

def update(g,L,h,rule_set):
    '''Update the grid, live cells, and history over one tick.'''
    new_g = np.zeros((gamesize,gamesize),dtype=int)
    new_L = []

    if 2*len(L) < gamesize*gamesize: # check over live cells
        cells_to_check = get_all_check(L)
        for cell in cells_to_check:
            new_state = get_next_state(cell,g,rule_set)
            if new_state:
                new_g[cell[0],cell[1]] = 1
                new_L.append(cell)
    else: # check over all cells if it is faster
        for r in range(gamesize):
            for c in range(gamesize):
                new_state = get_next_state((r,c),g,rule_set)
                if new_state:
                    new_g[r,c] = 1
                    new_L.append((r,c))

    new_h = h.copy()
    new_h = new_h*new_g + new_g
    return new_g, new_L, new_h

def init_grid(c,gs,s):
    '''Create grid, live cell list, and history on first tick.'''
    np.random.seed(s)
    if c: # randomize middle of field only
        colonysize = gs//5
        cmin = gs//2 - colonysize//2
        cmax = gs//2 + colonysize//2 
        g = np.zeros((gs,gs),dtype=int)
        g[cmin:cmax,cmin:cmax] = np.random.randint(0,2,size=(colonysize,colonysize),dtype=int)
    else: # randomize entire field
        g = np.random.randint(0,2,size=(gs,gs),dtype=int)

    # make live_cells
    L = []
    for r in range(gs):
        for c in range(gs):
            if g[r,c]:
                L.append((r,c))

    h = g.copy()
    return g, L, h

# parser
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=('''\
LifeSafari: Simulate any life-like grid-based cellular automaton in Python
--------------------------------
simulation controls:
  SPACE                 toggle pause
  a                     toggle showing cell age (see -a)
  c                     toggle whether cells spawn in the middle of the screen (see -f), use r or n to restart
  r                     restart simulation with same seed
  n                     restart simulation with new seed (overwrites previous seed)
  ESC/q                 close simulation

random generation with -r:
  -r random             generate completely random rulestring
  -r lifelike           same as random but guarantees consecutive numbers
  -r pick               pick a rulestring from the list of named rulestrings
  -r [name]             the name of any named rulestring e.g. `-r Ant Colony`, not case sensitive'''),
            epilog='See https://github.com/suranwarnakulasooriya/lifesafari for README')
parser.add_argument("-r", "--rulestring", nargs='*', type=str, default='B3/S23',
        help="Rulestring in B{#...}/S{#...} format, see https://conwaylife.com/wiki/Rulestring")
parser.add_argument("-d", "--dimension", type=int, default=200,
        help="Number of cells per row")
parser.add_argument("-f", "--fullscreen", action="store_true", default=False, 
        help="Spawn cells in the entire field (otherwise only in the middle of the screen)")
parser.add_argument("-a", "--age", action="store_true", default=False,
        help="Change cell color based on age spent alive")
parser.add_argument("-s", "--seed", type=int, default=-1,
        help="Random seed to replicate results")
parser.add_argument("-b", "--bgcolor", type=str, default='k',
        help="Color of dead cells (matplotlib)")
parser.add_argument("-c", "--colormap", type=str, default='rainbow_r',
        help="Colormap of live cells (matplotlib)")
parser.add_argument("-l", "--list", action="store_true", default=False,
        help="Print list of named rulestrings and exit")
parser.add_argument("-n", "--newname", nargs=2,
        help="Save a rulestring and give it a name, exit")

# load saved rulestrings
try:
    with open('savedlifes.json','r') as savefile:
        string_to_name = json.load(savefile)
except:
    print('No savefile located')
    string_to_name = {'B3/S23':"Conway's Game of Life"}

rulestrings = list(string_to_name.keys())
names = [i.lower() for i in list(string_to_name.values())]
name_to_string = dict(zip(names,rulestrings))

if __name__ == '__main__':
    # parse
    args = parser.parse_args()

    # print named rulestring and exit
    printnames = args.list
    if printnames:
        print(json.dumps(string_to_name,indent=4)); exit()
    
    # save a new rulestring
    try:
        newstring, newname = args.newname
        if newstring != '':
            parsed_string = read_rules(newstring, name_to_string)
            parsed_string = 'B'+''.join(map(str,parsed_string[0]))+'/S'+''.join(map(str,parsed_string[1]))
            if parsed_string != newstring:
                exit('No changes were made')
            if newstring in rulestrings:
                exit(f'{newstring} already saved as {string_to_name[newstring]}\nNo changes were made')
            string_to_name[newstring] = newname
            with open('savedlifes.json','w') as savefile:
                json.dump(string_to_name,savefile,indent=4)
            exit(f'Saved {newstring} as {newname}')
    except TypeError:
        pass

    # get simulating config
    gamesize = args.dimension
    colony = not args.fullscreen
    show_history = args.age
    bg_color = args.bgcolor
    colormap = args.colormap

    seed = args.seed
    if seed < 0:
        seed = np.random.randint(0,99999999)
    np.random.seed(seed)
    
    ruleset = ' '.join(args.rulestring) if args.rulestring != 'B3/S23' else args.rulestring

    if ruleset == 'random':
        ruleset = get_random_rules()
    elif ruleset == 'lifelike':
        ruleset = get_random_rules(lifelike=True)
    elif ruleset == 'pick':
        ruleset = np.random.choice(list(string_to_name.keys()))

    rules = read_rules(ruleset,name_to_string)
    ruleset = 'B'+''.join(map(str,sorted(rules[0])))+'/S'+''.join(map(str,sorted(rules[1])))
    try:
        ruleset = name_to_string[ruleset]
    except KeyError:
        pass
    
    cmap = plt.colormaps[colormap].copy()
    cmap.set_bad(color=bg_color)

    print('Use -h for help, controls, and README')
    print(f'Seed: {seed}')
    try:
        print(f'Rulestring: {ruleset} {string_to_name[ruleset]}')
    except KeyError:
        print(f'Rulestring: {ruleset}')
    
    # init grid
    grid, live_cells, history = init_grid(colony, gamesize, seed)
    
    # init first frame
    fig, ax = plt.subplots(figsize=(14,14))
    initial_matrix = grid
    im = ax.matshow(initial_matrix, cmap=cmap, animated=True)
    ax.set_xticks([])
    ax.set_yticks([])
    simulation_paused = False

    def keypress(event):
        '''Handle simulation controls via keypresses.'''
        global grid, live_cells, history, simulation_paused, show_history, seed, colony
        if event.key == ' ': # pause
            simulation_paused ^= 1
        elif event.key == 'escape': # close
            plt.close()
        elif event.key == 'a': # toggle age
            show_history ^= 1
        elif event.key == 'c': # toggle colony
            colony ^= 1
        elif event.key == 'r': # restart with same seed
            grid, live_cells, history = init_grid(colony, gamesize, seed)
        elif event.key == 'n': # restart with new seed
            seed = np.random.randint(0,99999999)
            print(f'New seed: {seed}')
            grid, live_cells, history = init_grid(colony, gamesize, seed)

    def animate(frame):
        '''Called every frame to update and display simulation.'''
        global grid, live_cells, history, simulation_paused, show_history

        if not simulation_paused:
            grid, live_cells, history = update(grid,live_cells,history,rules)
        # mask dead cells with background color
        if show_history:
            masked_data = np.ma.masked_where(history == 0, history)
            im.set_data(masked_data/128)
        else:
            masked_data = np.ma.masked_where(grid == 0, grid)
            im.set_data(masked_data)

        return (im,)
    
    fig.canvas.mpl_connect('key_press_event', keypress)
    ani = anim.FuncAnimation(fig, animate,
                        frames = 200, interval = 22, blit = True, cache_frame_data=False)
    plt.show()