
import random as rnd
from typing import List
import numpy as np
import tkinter as tk 
from tkinter import *
import time

class agent( ) :
    def __init__(self ,
                game ,
                state = None,
                in_active_start_states = [],
                agent_symbol = "A",
                agent_color = 'white' ) :
        self.agent_symbol = agent_symbol
        self.state = state
        self.agent_color = agent_color
        if self.state == None :  #  Pick an available random space to start agent.
            i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
            while (game.grid[i][j] != game.emptySpace_Char
                    and (i,j) not in in_active_start_states
                    and game.grid[i][j] != None ) : 
                    i,j = rnd.randint(0,game.size[1]-1), rnd.randint(0,game.size[0]-1)
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