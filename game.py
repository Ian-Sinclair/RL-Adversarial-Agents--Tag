"""
    Game attribute classes to control game objects and environment.
"""
import random as rnd
import numpy as np


class game( ) :
    def __init__(self, size : tuple ,
                random_start = True ,
                startRed = (0,0) ,
                startBlue = (0,0) ,
                walls_prob = 0 , 
                playable = False , 
                default_objects = ["W"]) :
        '''
        :param size: tuple (n , m) for game board
        :param walls_prob: probability that any square is not empty.
        :param default_objects: optional argument to add other environment objects to the game board, not including white space.
        '''
        #  Note:  Add functionality to increase the probability of walls initializing next to each other.
        self.playable = playable
        self.size = size
        self.emptySpace_Char = ' '
        self.default_objects = default_objects
        self.all_objects = [self.emptySpace_Char]+default_objects #  White space must be first element.
        prob = [1-walls_prob ] + [walls_prob/len(default_objects) ]*len(default_objects)
        self.grid = [[
                np.random.choice(self.all_objects, p = prob)
                for j in range(size[0])] 
            for i in range(size[1])
        ]
    def print_game(self) :
        [print(''.join(a)) for a in self.grid]

class agent( game ) :
    def __init__(self ,
                game ,
                state = None,
                in_active_start_states = [],
                agent_symbol = "A" ) :
        self.agent_symbol = agent_symbol
        self.state = state
        if self.state == None :  #  Pick an available random space to start agent.
            i,j = rnd.randint(0,game.size[0]-1), rnd.randint(0,game.size[1]-1)
            while (game.grid[i][j] != game.emptySpace_Char
                    and (i,j) not in in_active_start_states
                    and game.grid[i][j] != None ) : 
                    i,j = rnd.randint(0,game.size[0]-1), rnd.randint(0,game.size[1]-1)
            self.state = (i,j)
        i,j = self.state
        game.grid[i][j] = agent_symbol

    def moveRandom(self, game) :  # Need to finish functionality for this method...
        update = [
            (0,1), (0,-1), (1,0), (-1,0)
        ]
        dx,dy = update[np.random.choice(len(update))]
        i,j = self.state
        if self.isOpen(game, (i+dx, j+dy)) :
            game.grid[i+dx][j+dy] = self.agent_symbol
            self.state = (i+dx, j+dy)
            game.grid[i][j] = ' '


    def isOpen(self , game, new_state : tuple ) :
        a,b = new_state
        if (not (0<= a < len(game.grid) )
            or not (0<= b < len(game.grid[0])) ) : 
            return False
        if game.grid[a][b] in game.default_objects : return False
        return True

q = game((10,10), walls_prob=0.2)

red = agent(q, agent_symbol = "R")
Blue = agent(q, agent_symbol = "B")
for i in range(50) :
    red.moveRandom(q)
    Blue.moveRandom(q)

    print('--------------------------------------')
    q.print_game()



