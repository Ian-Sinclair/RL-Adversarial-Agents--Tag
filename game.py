"""
    Game attribute classes to control game objects and environment.
"""
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

class agent( game ) :
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



class GUI(tk.Tk) :
    def __init__( self ) :
        self.init_canvas()

    def init_canvas(self, play_game = False) :
        self.root = tk.Tk()
        self.root.title("COMP 3705 HW 0 Ian Sinclair")
        size = "600x600"
        self.root.geometry(size)
        self.size = [int(a) for a in size.split('x')]
        self.cx,self.cy = 100,100
        self.canvas = Canvas(self.root, width = self.cx, height = self.cy, bg = "cyan")
        self.canvas.pack(expand = YES, fill = BOTH)

    def draw_grid(self, game, n1, n2 ) :
        for i in range(len(game.grid)) :
            self.canvas.create_line(0,(i/n1)*self.size[1],self.size[0],(i/n1)*self.size[1])
        for i in range(len(game.grid[0])) :
            self.canvas.create_line((i/n2)*self.size[0],0,(i/n2)*self.size[0],self.size[1])

    def play_game(self, game , 
            agents : List,
            animation_refresh_seconds = 0.01
            ) :
            characters = []
            self.root.wait_visibility() # run event loop until window appears
            n1 = len(game.grid)
            n2 = len(game.grid[0])
            radx = self.size[0]/n2
            rady = self.size[1]/n1
            self.draw_grid(game, n1, n2)
            [
                [self.canvas.create_rectangle((j/n2)*self.size[0],
                    (i/n1)*self.size[1],
                    (j/n2)*self.size[0] + radx,
                    (i/n1)*self.size[1] + rady,
                    fill="black", outline="black", width=4)  
                for j in range(len(game.grid[i])) if game.grid[i][j] in game.default_objects
                ]
                for i in range(len(game.grid))
            ]
            for A in agents :
                a,b = A.state
                characters += [self.canvas.create_oval((b/n2)*self.size[0],
                    (a/n1)*self.size[1],
                    (b/n2)*self.size[0] + radx,
                    (a/n1)*self.size[1] + rady,
            fill=A.agent_color, outline=A.agent_color, width=0) ]

            for i in range(200) :
                for A,Ob in zip(agents,characters) :
                    a,b = A.state
                    self.canvas.moveto(Ob, (b/n2)*self.size[0], (a/n1)*self.size[1])
                    self.root.update()
                    time.sleep(animation_refresh_seconds)
                    A.moveRandom(game)
                    #print('--------------------------------------')
                    #game.print_game()
            self.root.mainloop()






q = game((35,35), walls_prob=0.3, playable=True)

red = agent(q, agent_symbol = "R", agent_color = 'red')
blue = agent(q, agent_symbol = "B", agent_color = 'green')


play = GUI()
play.play_game(q, [red,blue], animation_refresh_seconds=0.05)


'''
for i in range(50) :
    red.moveRandom(q)
    Blue.moveRandom(q)

    print('--------------------------------------')
    q.print_game()

'''

