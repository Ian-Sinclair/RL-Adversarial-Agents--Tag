'''
    -Ian Sinclair-
    Object class for every type of playable (AI driven) game character/agent.
    Includes functionality for updating the agents position, along with
    exploring its environment.
    An agent will have
        -Symbol -> display marker on the game grid
        -color -> for demoing the games
        -learning_style -> this is how the agent will encode its environment (generates each state in its state space.)
                            There are several learning styles to pick from and each one must match the function name
                            it is using to encode. ['basic' , 'basic_tree', 'k_quad_tree']
        -possible_moves -> every action an agent is capable of preforming for all states.
        -Q-table -> a look up table for the estimated best action given a state.
    There are two main agents that inherits from the agent class
        -Seeker -> agent that benefits from tracking other agents.
        -Runner -> agent that benefits from avoiding other agents.
        -fixed_goal -> runner agent that is incapable of moving (can be used to train seekers.)
'''
from base64 import encode
from cmath import inf
from Qtable import q_table
#from util import k_quad_tree
import random as rnd
from typing import List
import numpy as np
import tkinter as tk 
from tkinter import *
import pickle

from util import k_quad_tree

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
                                    'Random' : None }
            self.position = None
            if type(symbol) != type({0}) : symbol = {symbol}
            self.symbol = symbol   #  set
            self.color = color
            self.learning_style = learning_style
            self.gif = gif
    
    def get_possible_moves(self) :
        return self.possible_moves

    #  Given a game, places agent randomly on a valid game square.
    def start_position(self, game) :
        i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
        while (list(game.emptySpace.symbol)[0] not in game.grid[i][j]
                and game.grid[i][j] != None ) : 
                i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
        #if self.position != None :
        #    game.remove_grid( self.position , self.symbol )
        self.position = (i,j)
        game.update_grid( self.position , self.symbol ) 

    # Given an action and game position, moves the agent to the new location corresponding to the action.
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

    #  Randomly moves the agent (extremely basic form of AI)
    def moveRandom(self, game) :  # Need to finish functionality for this method...
        dx,dy = self.possible_moves[np.random.choice(list(self.possible_moves.keys()))]
        i,j = self.position
        new_pos = (i+dx, j+dy)
        if game.isOpen( new_pos ) :
            self.position = new_pos
            game.remove_grid( (i,j), self.symbol )
            game.update_grid( new_pos , self.symbol )
    
    # Forces the agent to move to a particular position regardless of action.
    def moveTO(self, game, new_pos) :
        i,j = self.position
        if game.isOpen( new_pos ) :
            self.position = new_pos
            game.remove_grid( (i,j), self.symbol )
            game.update_grid( new_pos , self.symbol )


    #  Encodes the environment of the agent based on its learning policy.
    def encode_Q_State(self, game, position, k_tree, target_pos = (None,None)) : # move to encoding class
        return eval("encode_" + self.learning_style + '(game, position, target_pos=target_pos , k_tree = k_tree)')


#  agent type inherits form agent class
#  benefits from seeking runner agents.
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
                        color = color,
                        learning_style = learning_style,
                        gif = gif)
        self.type = 'seeker'
        self.possible_moves = super().get_possible_moves()
        for action in special_moves.keys() : self.possible_moves[action] = special_moves[action]
        self.Q_table = q_table(moves = list(self.possible_moves.keys()))

    #  Determines the quality of an action in a particular state (sparse).
    '''
        Reward INFO
            - Seeker tags a runner -> +1000
            - Seeker hits a wall -> -60
            - Seeker gets really close to runner -> +20
            - Seeker extends the game without winning -> +1
    '''
    def get_reward(self, game, q_state : tuple , new_pos : tuple, target : set) :
        if game.contains( self.position , target ) : 
            return 1000, True
        if game.contains( new_pos , target ) : 
            return 1000, True
        if game.isOpen( new_pos ) == False : 
            return -60, False
        if any(list(target)[0] in q for q in q_state) : 
            return 20, False
        return 1, False
    
    def print_Qtable(self) :
        print(self.Q_table.print_Qtable())


#  agent type inherits form agent class
#  benefits from running away from seeker agents (staying alive).
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
        self.possible_moves['Stay Still'] = (0,0)
        self.Q_table = q_table(moves = list(self.possible_moves.keys()))


    #  Determines the quality of an action in a particular state (sparse).
    '''
        Reward INFO
            - Runner gets tagged by a seeker -> -1000
            - Runner hits a wall -> -60
            - Runner gets really close to seeker -> -60
            - Runner extends the game without losing -> +3
    '''
    def get_reward(self, game, q_state : tuple , new_pos : tuple, target : set) :
        if game.contains( self.position , target ) : 
            return -1000, True
        if game.contains( new_pos , target ) : 
            return -1000, True
        if not game.isOpen( new_pos ) : 
            return -60, False
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
    


#  returns list information for a grid of size 'size' surrounding the agent. (list of symbols)
#  Default size = 3 ensures the agents can only see they're immediate surroundings. (small state space complexity)
def encode_basic(game, pos : tuple, size = 3, target_pos : tuple = (None,None), k_tree = None) :
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

#  encodes a basic grid along with vague radar for the agents targets.
# Telling the agent if they're target is North-East, South-West, ... etc. But does
# not tell the agent how far away its target is.
def encode_basic_tree( game, pos : tuple, target_pos, size = 3 ,k_tree = None ) :
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


#  A more complicated version of basic tree that reveals some information about
# the distance a agent is from its target.
def encode_k_quad_tree(game , pos : tuple, k_tree, target_pos, size = 3) :
    state = encode_basic(game, pos, size)
    tree_data = k_tree.extract_data()
    return state + tree_data







