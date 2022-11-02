"""
    Game attribute classes to control game objects and environment.
"""
import agent as char
import GUI
import numpy as np



class game( ) :
    def __init__(self, size : tuple ,
                walls_prob = 0 , 
                playable = False ,
                fillFunc = 'randomGrid', 
                default_objects = ["W"]) :
        '''
        :param size: tuple (n , m) for game board
        :param walls_prob: probability that any square is not empty.
        :param default_objects: optional argument to add other environment objects to the game board, not including white space.
        '''
        #  Note:  Add functionality to increase the probability of walls initializing next to each other.
        self.playable = playable
        self.size = size
        self.walls_prob = walls_prob
        self.emptySpace_Char = ' '
        self.default_objects = default_objects
        self.all_objects = [self.emptySpace_Char]+default_objects #  White space must be first element.
        self.grid = eval('self.' + fillFunc + '()' )

    def randomGrid( self ) :
        prob = [1-self.walls_prob ] + [self.walls_prob/len(self.default_objects) ]*len(self.default_objects)
        grid = [[
                np.random.choice(self.all_objects, p = prob)
                for j in range(self.size[0])] 
            for i in range(self.size[1])
        ]
        grid[0] = [self.default_objects[0] for a in grid[0]]
        grid[-1] = [self.default_objects[0] for a in grid[-1]]
        for row in grid :
            row[0] = self.default_objects[0]
            row[-1] = self.default_objects[0]
        return grid


    def update_grid( self, state, value ) :
        i,j = state
        self.grid[i][j] = value
        if self.playable :
            #  Update screen.
            pass

    def print_game(self) :
        [print(''.join(a)) for a in self.grid]

'''
for i in range(100) :
    q = game((20,20), walls_prob=0.1, playable=True)

    red = char.agent(q, agent_symbol = "R", agent_color = 'red')
    blue = char.agent(q, agent_symbol = "B", agent_color = 'green')


    play = GUI.GUI()
    play.play_game(q, [red,blue], animation_refresh_seconds=0.02)
'''

'''
for i in range(50) :
    red.moveRandom(q)
    Blue.moveRandom(q)

    print('--------------------------------------')
    q.print_game()
'''

