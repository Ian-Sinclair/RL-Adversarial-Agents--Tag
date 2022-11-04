
from base64 import encode
from cmath import inf
from q-table import q_table
import random as rnd
from typing import List
import numpy as np
import tkinter as tk 
from tkinter import *

class agent :
    def __init__(self,
                position : tuple = (None,None),
                symbol : set = {'A'}
                color : str = 'black',
                gif : str = None ) :
            self.possible_moves = { 'North' : (0,1),
                                    'East' : (1,0),
                                    'South' : (0,-1), 
                                    'West' : (-1,0), 
                                    'Stay_still' : (0,0) }
            self.position = position
            self.symbol = symbol   #  set
            self.color = color
            self.gif = gif

    def start_position(self, game) :
        i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
        while (game.grid[i][j] != game.emptySpace.symbol
                and (i,j) not in self.active_start_states
                and game.grid[i][j] != None ) : 
                i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
        self.position = (i,j)
        game.update_grid( self.position , self.agent_symbol ) 


    def getNewPosition(self, game , action : str, position : tuple) :
        if action not in self.possible_moves.keys() : action = self.possible_moves[rnd.randint(0,len(self.possible_moves))]
        x,y = tuple([ sum(tup) for tup in zip(position, self.possible_moves[action] ) ])
        while not (0<=x < len(game.grid)) or not (0<=y < len(game.grid[0])) :
            action = self.possible_moves[rnd.randint(0,len(self.possible_moves))]
            x,y = tuple([ sum(tup) for tup in zip(position, self.possible_moves[action] ) ])
        return (x,y), action
    
    def moveRandom(self, game) :  # Need to finish functionality for this method...
        dx,dy = self.possible_moves[rnd.randint(0,len(self.possible_moves))]
        i,j = self.position
        new_pos = (i+dx, j+dy)
        if game.isOpen( new_pos ) :
            self.position = new_pos
            game.remove_grid( (i,j), self.symbol )
            game.update_grid( new_pos , self.symbol )
    
    def encode_Q_State(self, game, position, target_pos = (None,None)) : # move to encoding class
        return eval("encode_" + self.learning_style + '(game, position, target_pos=target_pos)')


class seeker( agent ) :
    def __init__( self, 
                position : tuple = (None,None),
                symbol : set = {'S'}
                color : str = 'red',
                gif : str = None,
                special_moves : dict = {},
                Q_table : q_table = q_table() ) :
        agent().__init__(self,
                        position = postion,
                        symbol = symbol
                        color =color,
                        gif = gif)
        for action in special_moves.keys() : self.possible_moves[action] = special_moves[action]
        self.Q_table = Q_table

    def get_reward(self, game, q_state : tuple , new_pos : tuple, target : set) :
        if game.contains( self.position , target ) : 
            return 1000, True
        if game.contains( new_pos , target ) : 
            return 1000, True
        if not game.isOpen( new_pos ) : return -50, False
        if any(v in q_state for v in target) : return 100, False
        return 0, False


class runner( agent ) :
    def __init__( self, 
                position : tuple = (None,None),
                symbol : set = {'R'}
                color : str = 'blue',
                gif : str = None,
                special_moves : dict = {},
                Q_table : q_table = q_table() ) :
        agent().__init__(self,
                        position = postion,
                        symbol = symbol
                        color =color,
                        gif = gif)
        for action in special_moves.keys() : self.possible_moves[action] = special_moves[action]
        self.Q_table = Q_table

    def get_reward(self, game, q_state : tuple , new_pos : tuple, target : set) :
        if game.contains( self.position , target ) : 
            return -1000, True
        if game.contains( new_pos , target ) : 
            return -1000, True
        if not game.isOpen( new_pos ) : return -50, False
        if any(v in q_state for v in target) : return -60, False
        return 0, False



def encode_basic(game, pos : tuple, size = 3, target_pos = (None,None)) :
    #  make mask with basic game objects, center mask at position
    #  overlay mask with image.
    mask = [[game.default_objects[0] for j in range(size)] for i in range(size)]
    x,y = -1,-1
    for i in range(pos[0] - int(size/2) , pos[0]+int(size/2+1)) :
        x+= 1
        y = -1
        for j in range(pos[1] - int(size/2) , pos[1]+int(size/2)+1) :
            y+=1
            if ( (0<= i < len(game.grid) )
                and (0<= j < len(game.grid[0]) ) ) :
                if game.grid[i][j] not in game.default_objects :
                    mask[x][y] = game.grid[i][j]
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
    return state + (modx ,  mody)








