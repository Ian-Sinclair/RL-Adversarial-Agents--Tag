"""
    Game attribute classes to control game objects and environment.
"""
import agent as char
#from object import *
import object
import GUI
import numpy as np
import random as rnd

class game( ) :
    def __init__(self, 
                size : tuple ,
                walls_prob = 0 , 
                fillFunc = 'randomGrid',
                empty_space = object.empty(),
                default_objects = [ object.wall() ],
                background_color = 'cyan' ) :

        self.size = size
        self.walls_prob = walls_prob
        self.emptySpace = empty_space
        self.default_objects = default_objects
        self.background_color = background_color
        self.default_symbols = [a.symbol for a in default_objects]
        self.all_objects = [self.emptySpace]+self.default_objects
        self.all_symbols = [a.symbol for a in self.all_objects] # set(set(str))

        self.grid = eval('self.' + fillFunc + '()' )

    def randomGrid( self ) :
        if len(self.default_objects) == 0 : return [[self.emptySpace.symbol]*self.size[0]]*self.size[1]
        prob = [1-self.walls_prob ] + [self.walls_prob/len(self.default_objects) ]*len(self.default_objects)
        grid = [[
                np.random.choice(self.all_symbols, p = prob).copy()
                for j in range(self.size[0])] 
            for i in range(self.size[1])
        ]
        grid[0] = [self.default_objects[0].symbol for a in grid[0]]
        grid[-1] = [self.default_objects[0].symbol for a in grid[-1]]
        for row in grid :
            row[0] = self.default_objects[0].symbol
            row[-1] = self.default_objects[0].symbol
        return grid


    def update_grid( self, position, value ) :
        if type(value) != type(set()) : value = set([value])
        i,j = position
        #print(i,j)
        self.grid[i][j].update(value)
    
    def remove_grid( self , position, value ) :
        if type(value) != type(set()) : value = set([value])
        i,j = position
        self.grid[i][j] = self.grid[i][j] - value
    
    def contains( self , position , value ) :
        x,y = position
        if type(value) == type('') : value = {value}
        if any(v in self.grid[x][y] for v in value) : 
            return True
        return False
    
    def isOpen(self , position : tuple ) :
        a,b = position
        if (not (0<= a < len(self.grid) )
            or not (0<= b < len(self.grid[0])) ) : 
            return False
        if any(x in self.default_symbols[0] for x in list(self.grid[a][b])) :
            if len(self.default_symbols[0]) > 1 : print(self.default_symbols[0])
            #print(self.default_symbols[0])
            return False
        return True


    def print_game(self) :
        [print(''.join([list(x)[0] for x in row])) for row in self.grid]

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

def test_game_boards() :
    print('Printing Random Game Boards')
    for i in range(100) :
        print('Random Board:  ' + str(i))
        q = game((rnd.randint(4,20),rnd.randint(4,20)), walls_prob=rnd.randint(0,20)/20)
        q.print_game()


if __name__ == "__main__":
   print('Testing game.py file')
   print('------------------------')
   test_game_boards()



