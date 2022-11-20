"""
    Game attribute classes to control objects and environment. 
    All position information for agents/objects is stored in game class object.
    Works like a grid -> list[ list[ set{ string } ] ]
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
        self.default_symbols = [a.symbol for a in default_objects]  # list of default object sets.
        self.all_objects = [self.emptySpace]+self.default_objects  #  list of all object symbols.
        self.all_symbols = [a.symbol for a in self.all_objects] # set(set(str))

        self.grid = eval('self.' + fillFunc + '()' )

    def randomGrid( self ) :  # Randomly adds default obects to grid by some probability distrabution
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
    
    def emptyGrid( self ) :
        if len(self.default_objects) == 0 : return [[self.emptySpace.symbol]*self.size[0]]*self.size[1]
        grid = [[
                np.random.choice([self.emptySpace.symbol]).copy()
                for j in range(self.size[0])] 
            for i in range(self.size[1])
        ]
        grid[0] = [self.default_objects[0].symbol for a in grid[0]]
        grid[-1] = [self.default_objects[0].symbol for a in grid[-1]]
        for row in grid :
            row[0] = self.default_objects[0].symbol
            row[-1] = self.default_objects[0].symbol
        return grid
    
    def uniformGrid( self ) :
        if len(self.default_objects) == 0 : return [[self.emptySpace.symbol]*self.size[0]]*self.size[1]
        prob = [1-self.walls_prob ] + [self.walls_prob/len(self.default_objects) ]*len(self.default_objects)
        grid = [
                    [
                    np.random.choice(self.default_symbols).copy()
                    if ((j+i)%4 == 1 and i%2 == 1)
                    else
                        self.emptySpace.symbol.copy()
                    for j in range(self.size[0])
                    ] 
                    for i in range(self.size[1])
                ]
        grid[0] = [self.default_objects[0].symbol for a in grid[0]]
        grid[-1] = [self.default_objects[0].symbol for a in grid[-1]]
        for row in grid :
            row[0] = self.default_objects[0].symbol
            row[-1] = self.default_objects[0].symbol
        return grid

    def roomsGrid( self ) :
        if len(self.default_objects) == 0 : return [[self.emptySpace.symbol]*self.size[0]]*self.size[1]
        min_mod_rooms = 5
        h_rooms = rnd.randint(min([min_mod_rooms,int(self.size[0]/2)]) , min([min_mod_rooms,self.size[0]]))
        v_rooms = rnd.randint(min([min_mod_rooms, int(self.size[1]/2)]) , min([min_mod_rooms,self.size[1]]))
        prob = [1-self.walls_prob ] + [self.walls_prob/len(self.default_objects) ]*len(self.default_objects)
        grid = [
                    [
                    np.random.choice([np.random.choice(self.default_symbols).copy(), self.emptySpace.symbol.copy()], p = [0.75,0.25])
                    if j%h_rooms == 0 or i%v_rooms == 0
                    else
                        self.emptySpace.symbol.copy()
                    for j in range(self.size[0])
                    ] 
                    for i in range(self.size[1])
                ]
        grid[0] = [self.default_objects[0].symbol for a in grid[0]]
        grid[-1] = [self.default_objects[0].symbol for a in grid[-1]]
        for row in grid :
            row[0] = self.default_objects[0].symbol
            row[-1] = self.default_objects[0].symbol
        return grid


    def update_grid( self, position, value ) :  #  Adds a string type value to the current set of strings at grid location (position)
        if type(value) != type(set()) : value = set([value])
        i,j = position
        #print(i,j)
        self.grid[i][j].update(value)
    
    def remove_grid( self , position, value ) : #  Removes an element from grid at location 'position'
        if type(value) != type(set()) : value = set([value])
        i,j = position
        self.grid[i][j] = self.grid[i][j] - value
    
    def contains( self , position , value ) : #  Primitive to check if value is contained at grid location position
        x,y = position
        if type(value) == type('') : value = {value}
        if any(v in self.grid[x][y] for v in value) : 
            return True
        return False
    
    def isOpen(self , position : tuple ) : #  Primitive checks of position is valid and/or occupied by default object.
        a,b = position
        if (not (0<= a < len(self.grid) )
            or not (0<= b < len(self.grid[0])) ) : 
            return False
        if any(x in self.default_symbols[0] for x in list(self.grid[a][b])) :
            if len(self.default_symbols[0]) > 1 : print(self.default_symbols[0])
            #print(self.default_symbols[0])
            return False
        return True


    def print_game(self) :  # prints game board.
        [print(''.join([list(x)[0] for x in row])) for row in self.grid]


def test_game_boards() :
    print('Printing Random Game Boards')
    board_types = ['randomGrid', 'uniformGrid', 'roomsGrid', 'emptyGrid']
    for i in range(30) :
        type = np.random.choice(board_types)
        print('Random Board: ' + str(type) + ' Iteration: ' + str(i))
        q = game((rnd.randint(8,20),rnd.randint(8,20)), walls_prob=rnd.randint(0,19)/20, fillFunc=type)
        q.print_game()


if __name__ == "__main__":
   print('Testing game.py file')
   print('------------------------')
   test_game_boards()



