"""
    Game attribute classes to control game objects and environment.
"""
import agent as char
import GUI
import random as rnd
from typing import List
import numpy as np
import tkinter as tk 
from tkinter import *
import time




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


    def update_grid( self, state, value ) :
        i,j = state
        self.grid[i][j] = value
        if self.playable :
            #  Update screen.
            pass
    
    def print_game(self) :
        [print(''.join(a)) for a in self.grid]



q = game((35,35), walls_prob=0.1, playable=True)

red = char.agent(q, agent_symbol = "R", agent_color = 'red')
blue = char.agent(q, agent_symbol = "B", agent_color = 'green')


play = GUI.GUI()
play.play_game(q, [red,blue], animation_refresh_seconds=0.05)


'''
for i in range(50) :
    red.moveRandom(q)
    Blue.moveRandom(q)

    print('--------------------------------------')
    q.print_game()

'''

