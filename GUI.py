'''
    Contains demo information to display games and agent strategies.
'''


import os
import random as rnd
from agent import agent, seeker, runner
import game
import numpy as np
import tkinter as tk 
from tkinter import *
import time
from PIL import ImageGrab, Image
import ghostscript
#  from PIL import Image, ImageTk



class GUI(tk.Tk) :
    def __init__( self,
                game,
                root_size : str = '600x600',
                title = 'Demo'
                 ) :
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(root_size)
        self.size = [int(a) for a in root_size.split('x')]
        self.cx,self.cy = 100,100  # This may be wrong...
        self.canvas = Canvas(self.root, width = self.cx, height = self.cy, bg = game.background_color)
        self.canvas.pack(expand = YES, fill = BOTH)

    def init_canvas(self) : # might want to init canvas in own function, add functionality here.
        pass

    def draw_grid(self, game ) :
        lines = []
        max_x = game.size[1]
        max_y = game.size[0]
        for i in range(len(game.grid)) :
            lines.append(
                self.canvas.create_line(0,(i/max_x)*self.size[1],self.size[0],(i/max_x)*self.size[1]) 
                )
        for i in range(len(game.grid[0])) :
            lines.append(
                self.canvas.create_line((i/max_y)*self.size[0],0,(i/max_y)*self.size[0],self.size[1]) 
                )
        return lines
    
    def draw_object(self, game, object, x , y ) :
        radx = self.size[0]/game.size[0]
        rady = self.size[1]/game.size[1]
        if object.symbol in game.default_symbols :
            if object.gif == None :
                return self.canvas.create_rectangle((y/game.size[0])*self.size[0],
                    (x/game.size[1])*self.size[1],
                    (y/game.size[0])*self.size[0] + radx,
                    (x/game.size[1])*self.size[1] + rady,
                    fill=object.color, outline=object.color, width=4)
            else :
                print('No image information found:  Object' + object.name )
                # Draw gif at location
        else :
            if object.gif == None :
               return self.canvas.create_oval((y/len(game.grid[0]))*self.size[0],
                    (x/len(game.grid))*self.size[1],
                    (y/len(game.grid[0]))*self.size[0] + radx,
                    (x/len(game.grid))*self.size[1] + rady,
                    fill=object.color, outline=object.color, width=4)

            else :
                print('No image information found:  Object' + object.name )
                # Draw gif at location
        return False

    def draw_defaultObjects(self, game) :
        return [
            [self.draw_object(game, [obj for obj in game.default_objects if obj.symbol == {symb} ][0] , i , j)
            for j in range(len(game.grid[i])) 
            for symb in game.grid[i][j]
            if {symb} in game.default_symbols
            ]
            for i in range(len(game.grid))
        ]

    def draw_background(self, game) :
        self.canvas.create_rectangle(0,
                    0,
                    self.size[0],
                    self.size[1],
                    fill=game.background_color, outline=game.background_color, width=0)


    def draw_agent(self, game , agents : list) :
        for A in agents :
            A.start_position(game)
        return [
            self.draw_object( game, A , A.position[1] , A.position[0] ) for A in agents
        ]

    def saveImage(self, savelocation):
        widget = self.canvas
        x = self.root.winfo_rootx() + widget.winfo_x()
        y = self.root.winfo_rooty() + widget.winfo_y()
        x1 = x + widget.winfo_width()
        y1 = y + widget.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save(savelocation)


    def demo(self,
             game, 
             seekers : list,
             runners : list, 
             game_length = 100,
             epsilon = 0,
             strategy : str = 'random',
             animation_refresh_seconds = 0.02) -> None :
        function_links = ['agent_strategy', 'random']
        if strategy not in  function_links:
            raise ValueError("unsupported function: strategy must be in: " + str(function_links))
        eval('self.demo_' + strategy + '(game, seekers, runners, game_length, epsilon, animation_refresh_seconds)' )
    
    def demo_random(self,
            game, 
            seekers : list,
            runners : list, 
            game_length = 100,
            epsilon = 0,
            animation_refresh_seconds = 0.02) :
            print("Agents Will Preform Random Movements")
            self.root.wait_visibility()  # Saves animation frames for window origination
            #  lines = self.draw_grid( game )  #  draws grid lines
            rectangels = self.draw_defaultObjects( game )
            char_seekers = self.draw_agent( game , seekers )
            char_runners = self.draw_agent( game , runners )

            for i in range(game_length) :
                for A,Ob in zip(seekers + runners , char_seekers + char_runners) :
                    a,b = A.position
                    self.canvas.moveto(Ob, (b/game.size[1])*self.size[0], (a/game.size[0])*self.size[1])
                    self.root.update()
                    time.sleep(animation_refresh_seconds)
                    A.moveRandom(game)
            self.root.destroy()
            self.root.mainloop()

    def play_game( self, 
            game,
            seekers,
            runners,
            seekers_moves,
            runners_moves,
            animation_refresh_seconds = 0.02,
            collect_GIF = False,
            FilePath = None,
            FileName = None
            ) :
            images = []
            self.root.wait_visibility()  # Saves animation frames for window origination
            #  lines = self.draw_grid( game )  #  draws grid lines
            self.draw_background(game)
            rectangels = self.draw_defaultObjects( game )
            char_seekers = self.draw_agent( game , seekers )
            char_runners = self.draw_agent( game , runners )
            i = 0
            for S_pos,R_pos in zip( seekers_moves, runners_moves ) :
                i += 1
                a,b = S_pos
                self.canvas.moveto(char_seekers[0], (b/game.size[1])*self.size[0], (a/game.size[0])*self.size[1])
                self.root.update()
                time.sleep(animation_refresh_seconds)
                a,b = R_pos
                self.canvas.moveto(char_runners[0], (b/game.size[1])*self.size[0], (a/game.size[0])*self.size[1])
                self.root.update()
                time.sleep(animation_refresh_seconds)
                #if collect_GIF : self.save_as_png(self.canvas, 'image ' + str(i), 'testGame/')
                if collect_GIF :  images += [ self.to_Image(self.canvas, 'image ' + str(i), 'testGame/') ]
            self.root.destroy()
            self.root.mainloop()
            if collect_GIF : return images

    def save_as_GIF(self, images : list, filename, path) :
        if not os.path.exists(path):
            os.makedirs(path)
        images[0].save( path + filename + '.gif', save_all=True, append_images=images[1:], optimize=True,duration=100, loop=1)

    def to_Image(self, canvas, filename, path) :
        if not os.path.exists('epsDumping/') :
            os.makedirs('epsDumping/')
        canvas.postscript(file = 'epsDumping/'+filename+'.eps')
        img = Image.open('epsDumping/'+filename + '.eps')
        return img

    def save_as_png(self, canvas, filename, path) :
        if not os.path.exists('epsDumping/'):
            os.makedirs('epsDumping/')
        canvas.postscript(file = 'epsDumping/'+filename+'.eps')
        img = Image.open('epsDumping/'+filename + '.eps')
        newpath = path
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        img.save(path+filename +'.png', 'png')

    def demo_agent_strategy(self,
            game, 
            seekers : list,
            runners : list, 
            game_length = 100,
            epsilon = 0,
            animation_refresh_seconds = 0.02) :
            '''
            for A in seekers + runners :
                A.start_position(game)
            
            game_info = learn.run_game_instance(
                                    game,
                                    seekers,
                                    runners,
                                    game_length,
                                    epsilon,
                                update_strategy=False
                                )
            seekers_moves = game_info['Seeker Positions']
            runners_moves = game_info['Runner Positions']
            self.play_game(
                    game,
                    seekers,
                    runners,
                    seekers_moves,
                    runners_moves,
                    animation_refresh_seconds
                )
            '''

def test_GUI_Random() :
    print('Demoing Random Game')
    q = game.game((15,15), walls_prob=0.3)
    q.print_game()
    red = agent(q, symbol = {"R"}, color = 'red')
    blue = agent(q, symbol = {"B"}, color = 'green')
    play = GUI(q)
    play.demo(q, seekers = [red], runners = [blue], game_length=600 ,animation_refresh_seconds=0.04)
        


if __name__ == "__main__":
   print('Testing GUI.py file')
   print('------------------------')
   test_GUI_Random()


