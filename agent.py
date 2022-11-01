
from cmath import inf
import random as rnd
from typing import List
import numpy as np
import tkinter as tk 
from tkinter import *

possible_moves = ['North', 'East', 'South', 'West', 'Stay_still']

class q_table() :
    def __init__(self, 
                func = 'basic',
                moves = possible_moves) :
        self.possible_moves = moves
        self.q_table = eval('self.'+func + '()')
    
    def basic( self ) : # 3X3 In front of target.
        return {}
    def update_q_Table(self, state, reward, action, new_state, discount = 1, alpha = 0.7) :
        if state not in self.q_table.keys() or new_state not in self.q_table.keys() :
            if state not in self.q_table.keys() :
                self.q_table[state] = {}
                for a in self.possible_moves :
                    self.q_table[state][a] = 0
            if new_state not in self.q_table.keys() :
                self.q_table[new_state] = {}
                for a in self.possible_moves :
                    self.q_table[new_state][a] = 0
            return True
        else : 
            if action in self.possible_moves :
                sample = reward + discount*max(self.q_table[new_state].values())
                self.q_table[state][action] = (
                    (1-alpha)*self.q_table[state][action]
                    + alpha*sample
                    )
                return True
        return False
    
    def getAction(self, state) :
        if state in self.q_table.keys() : 
            return max(self.q_table[state], key=self.q_table[state].get)
        return np.random.choice(self.possible_moves)
    
    def getNewState(self, action : str, state : tuple) :
        action_map = {
            'North' : (0,1),
            'South' : (0,-1),
            'East' : (-1,0),
            'West' : (1,0),
            'Stay_still' : (0,0),
            'Move_Random' : None
        }
        if action_map[action] == None : action = self.possible_moves[np.random.choice(list(range(5)))]
        x,y = tuple([ sum(tup) for tup in zip(state, action_map[action] ) ])
        while not (0<=x < 10) or not (0<=y < 10) :
            action = self.possible_moves[np.random.choice(list(range(5)))]
            x,y = tuple([ sum(tup) for tup in zip(state, action_map[action] ) ])
        return (x,y), action




class agent( ) :
    def __init__(self ,
                game ,
                state = None,
                in_active_start_states = [],
                agent_symbol = "A",
                agent_color = 'white',
                learning_style = 'basic',
                type = 'seeker') :
        self.agent_symbol = agent_symbol
        self.type = type
        self.active_start_states = []
        self.state = state
        self.agent_color = agent_color
        self.learning_style = learning_style
        self.q_table = q_table()

        self.start(game)

    def start(self, game) :
        if self.state == None :  #  Pick an available random space to start agent.
            i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
            while (game.grid[i][j] != game.emptySpace_Char
                    and (i,j) not in self.active_start_states
                    and game.grid[i][j] != None ) : 
                    i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
            self.state = (i,j)
        i,j = self.state
        game.grid[i][j] = self.agent_symbol


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
    
    def encode_Q_State(self, game) :
        return eval("encode_" + self.learning_style + '(game, self.state)')

    def isOpen(self , game, new_state : tuple ) :
        a,b = new_state
        if (not (0<= a < len(game.grid) )
            or not (0<= b < len(game.grid[0])) ) : 
            return False
        if game.grid[a][b] in game.default_objects : return False
        return True
    
    def get_reward(self, game, new_state, target, time_alive = None ) :
        if self.type == 'seeker' : return self.get_reward_seeker(game, new_state, target)
        return self.get_reward_hider(game, new_state, target, time_alive)


    def get_reward_seeker(self, game, new_state, target) :
        x,y = new_state
        if game.grid[x][y] == target : return 1000, True
        if not self.isOpen(game, (x,y)) : return - 10, False
        return 0, False
    def get_reward_hider(self, game, new_state, target, time_alive) :
        x,y = new_state
        if game.grid[x][y] == target : return -1000, True
        if not self.isOpen(game, (x,y)) : return - 10, False
        return time_alive*0.5, False



def encode_basic(game, pos : tuple, size = 5) :
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




