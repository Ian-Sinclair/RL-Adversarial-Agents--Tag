'''
    Agent classes contains information availiable to each agent
    including Q table management. And information encoding.
'''
from base64 import encode
from cmath import inf
from Qtable import q_table
import random as rnd
from typing import List
import numpy as np
import tkinter as tk 
from tkinter import *
import pickle

class agent :
    def __init__(self,
                position : tuple = None,
                symbol : set = {'A'},
                color : str = 'black',
                learning_style : str = 'basic',
                gif : str = None ) :
            self.possible_moves = { 'North' : (-1,0),
                                    'East' : (0,1),
                                    'South' : (1,0), 
                                    'West' : (0,-1), 
                                    'Stay_still' : (0,0),
                                    'Random' : None }
            self.position = None
            if type(symbol) != type({0}) : symbol = {symbol}
            self.symbol = symbol   #  set
            self.color = color
            self.learning_style = learning_style
            self.gif = gif
    
    def get_possible_moves(self) :
        return self.possible_moves

    def start_position(self, game) :
        i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
        while (list(game.emptySpace.symbol)[0] not in game.grid[i][j]
                and game.grid[i][j] != None ) : 
                i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
        #if self.position != None :
        #    game.remove_grid( self.position , self.symbol )
        self.position = (i,j)
        game.update_grid( self.position , self.symbol ) 


    def getNewPosition(self, game , action : str, position : tuple) :
        if action not in list(self.possible_moves.keys()) : 
            action = list(self.possible_moves.keys())[rnd.randint(0,len(self.possible_moves)-1)]
        out_action = action
        while self.possible_moves[action] == None :
            action = list(self.possible_moves.keys())[rnd.randint(0,len(self.possible_moves)-1)]
        x,y = tuple([ sum(tup) for tup in zip(position, self.possible_moves[action] ) ])
        while not (0<=x < len(game.grid)) or not (0<=y < len(game.grid[0])) :
            action = self.possible_moves[rnd.randint(0,len(self.possible_moves))]
            x,y = tuple([ sum(tup) for tup in zip(position, self.possible_moves[action] ) ])
        return (x,y), out_action
        #return self.position, out_action

    
    def moveRandom(self, game) :  # Need to finish functionality for this method...
        dx,dy = self.possible_moves[np.random.choice(list(self.possible_moves.keys()))]
        i,j = self.position
        new_pos = (i+dx, j+dy)
        if game.isOpen( new_pos ) :
            self.position = new_pos
            #print(game.grid[i][j])
            game.remove_grid( (i,j), self.symbol )
            #print(game.grid[i][j])
            #print('--------')
            game.update_grid( new_pos , self.symbol )
    
    def moveTO(self, game, new_pos) :
        i,j = self.position
        if game.isOpen( new_pos ) :
            self.position = new_pos
            game.remove_grid( (i,j), self.symbol )
            game.update_grid( new_pos , self.symbol )




    
    def encode_Q_State(self, game, position, target_pos = (None,None)) : # move to encoding class
        return eval("encode_" + self.learning_style + '(game, position, target_pos=target_pos)')


class seeker( agent ) :
    def __init__( self, 
                position : tuple = None,
                symbol : set = {'S'},
                color : str = 'red',
                gif : str = None,
                special_moves : dict = {},
                learning_style : str = 'basic',
                Q_table : q_table = None ) :
        super().__init__(self,
                        symbol = symbol,
                        color =color,
                        learning_style = learning_style,
                        gif = gif)
        self.type = 'seeker'
        self.possible_moves = super().get_possible_moves()
        for action in special_moves.keys() : self.possible_moves[action] = special_moves[action]
        self.Q_table = q_table(moves = list(self.possible_moves.keys()))

    def get_reward(self, game, q_state : tuple , new_pos : tuple, target : set) :
        if game.contains( self.position , target ) : 
            return 1000, True
        if game.contains( new_pos , target ) : 
            return 10000, True
        if game.isOpen( new_pos ) == False : 
            return -60, False
        if any(list(target)[0] in q for q in q_state) : 
            return 20, False
        return 1, False
    
    def print_Qtable(self) :
        print(self.Q_table.print_Qtable())


class runner( agent ) :
    def __init__( self, 
                position : tuple = (None,None),
                symbol : set = {'R'},
                color : str = 'blue',
                gif : str = None,
                special_moves : dict = {},
                learning_style : str = 'basic',
                Q_table : q_table = q_table() ) :
        super().__init__(self,
                        symbol = symbol,
                        color =color,
                        learning_style = learning_style,
                        gif = gif)
        self.type = 'runner'
        self.possible_moves = super().get_possible_moves()
        for action in special_moves.keys() : self.possible_moves[action] = special_moves[action]
        self.Q_table = q_table(moves = list(self.possible_moves.keys()))

    def get_reward(self, game, q_state : tuple , new_pos : tuple, target : set) :
        if game.contains( self.position , target ) : 
            return -1000, True
        if game.contains( new_pos , target ) : 
            return -1000, True
        if not game.isOpen( new_pos ) : 
            return -10, False
        if any(list(target)[0] in q for q in q_state) : 
            return -60, False
        return 3, False
    
    def print_Qtable(self) :
        print(self.Q_table.print_Qtable())


class fixed_goal( agent ) :
    def __init__( self, 
                position : tuple = (None,None),
                symbol : set = {'F'},
                color : str = 'Yellow',
                gif : str = None,
                special_moves : dict = {},
                learning_style : str = 'basic',
                Q_table : q_table = q_table() ) :
        super().__init__(self,
                        symbol = symbol,
                        color =color,
                        learning_style = learning_style,
                        gif = gif)
        self.type = 'runner'
        self.possible_moves = super().get_possible_moves()
        for action in special_moves.keys() : self.possible_moves[action] = special_moves[action]
        self.Q_table = q_table(moves = list(self.possible_moves.keys()))

    def get_reward(self, game, q_state : tuple , new_pos : tuple, target : set) :
        return 0, False

    def start_position(self, game) :
        if self.position != None : return self.position
        i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
        while (list(game.emptySpace.symbol)[0] not in game.grid[i][j]
                and game.grid[i][j] != None ) : 
                i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
        if self.position != None :
            game.remove_grid( self.position , self.symbol )
        self.position = (i,j)
        game.update_grid( self.position , self.symbol ) 

    def getNewPosition(self, game , action : str, position : tuple) :
        return self.position
    
    def moveRandom(self, game) :  # Need to finish functionality for this method...
        return True
    
    def moveTO(self, game, new_pos) :
        return True
    
    def print_Qtable(self) :
        print(self.Q_table.print_Qtable())
    



def encode_basic(game, pos : tuple, size = 3, target_pos : tuple = (None,None)) :
    #  make mask with basic game objects, center mask at position
    #  overlay mask with image.
    mask = [[tuple(list(game.default_symbols)[0]) for j in range(size)] for i in range(size)]
    x,y = -1,-1
    for i in range(pos[0] - int(size/2) , pos[0]+int(size/2+1)) :
        x += 1
        y = -1
        for j in range(pos[1] - int(size/2) , pos[1]+int(size/2)+1) :
            y+=1
            if ( (0<= i < len(game.grid) )
                and (0<= j < len(game.grid[0]) ) ) :
                for symb in game.grid[i][j] :
                    if {symb} not in game.default_symbols :
                        mask[x][y] = tuple(game.grid[i][j].copy())
    return tuple(
        [item for sublist in mask for item in sublist]
    )


def encode_basic_tree( game, pos : tuple, target_pos, size = 3,  ) :
    state = encode_basic(game, pos, size)
    x,y = pos
    a,b = target_pos
    modx = '-1'
    mody = '-1'
    if a >= x :
        modx = '1'
    if b >= y :
        mody = '1'
    #return (modx ,  mody)
    return state + (modx ,  mody)








