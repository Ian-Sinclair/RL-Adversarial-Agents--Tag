
import random as rnd
from agent import agent
import numpy as np
import tkinter as tk 
from tkinter import *
import time


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
    
    def demo(self, game,
            agents,
            game_lenth = 100,
            epsilon = 0.5,
            animation_refresh_seconds=0.02) :

        characters = []
        self.root.wait_visibility()
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

        for i in range(game_lenth) :
            for A,Ob in zip(agents,characters) :
                a,b = A.state
                self.canvas.moveto(Ob, (b/n2)*self.size[0], (a/n1)*self.size[1])
                self.root.update()
                time.sleep(animation_refresh_seconds)


                x,y = A.state
                encoding_state = A.encode_Q_State(game)
                action = A.q_table.getAction( encoding_state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_state, _ = A.q_table.getNewState( action, A.state )
                if A.isOpen(game , new_state) :
                    game.grid[new_state[0]][new_state[1]] = A.agent_symbol
                    A.state = new_state
                    game.grid[x][y] = ' '
                #print('--------------------------------------')
                #game.print_game()
        self.root.destroy()
        self.root.mainloop()

    def play_game(self, game , 
            agents : list,
            animation_refresh_seconds = 0.01
            ) :                         #     Lol this method play in reverse btw.
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
                    game.print_game()
            self.root.destroy()
            self.root.mainloop()