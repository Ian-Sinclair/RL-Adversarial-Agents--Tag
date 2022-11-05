
import random as rnd
from agent import agent
import game
import numpy as np
import tkinter as tk 
from tkinter import *
import time
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
    
    def draw_agent(self, game , agents : list) :
        for A in agents :
            A.start_position(game)
        return [
            self.draw_object( game, A , A.position[0] , A.position[1] ) for A in agents
        ]

    
    def demo(self,
             game, 
             seekers : list,
             runners : list, 
             game_length = 100,
             epsilon = 0,
             strategy : str = 'random',
             animation_refresh_seconds = 0.02) -> None :
        function_links = ['agent_based', 'random']
        if strategy not in  function_links:
            raise ValueError("unsupported function: strategy must be in: " + str(function_links))
        eval('self.demo_' + strategy + '(game, seekers, runners, game_length, epsilon, animation_refresh_seconds)' )
    
    def demo_random(self,
            game, 
            seekers,
            runners, 
            game_length = 100,
            epsilon = 0,
            animation_refresh_seconds = 0.02) :
            print("Agents Will Preform Random Movements")
            self.root.wait_visibility()  # Saves animation frames for window origination
            lines = self.draw_grid( game )  #  draws grid lines
            rectangels = self.draw_defaultObjects( game )
            char_seekers = self.draw_agent( game , seekers )
            char_runners = self.draw_agent( game , runners )

            for i in range(game_length) :
                for A,Ob in zip(seekers + runners,char_seekers + char_runners) :
                    a,b = A.position
                    self.canvas.moveto(Ob, (b/game.size[1])*self.size[0], (a/game.size[0])*self.size[1])
                    self.root.update()
                    time.sleep(animation_refresh_seconds)
                    A.moveRandom(game)
                    #print('--------------------------------------')
            self.root.destroy()
            self.root.mainloop()




'''
    def demo(self, game,
            agents,
            game_lenth = 100,
            epsilon = 0,
            animation_refresh_seconds=0.02) :
        n1 = len(game.grid)
        n2 = len(game.grid[0])

        self.draw_grid(game, n1, n2)

        for A in agents :
                A.state = None
                A.start(game)
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
                if A.type == 'seeker' :
                    encoding_state = A.encode_Q_State(game, A.state, target_pos=agents[1].state)
                else :
                    encoding_state = A.encode_Q_State(game, A.state, target_pos=agents[0].state)

                action = A.q_table.getAction( encoding_state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_state, _ = A.q_table.getNewState(game, action, A.state )
                if A.type == 'seeker' :
                    reward, end =  A.get_reward(game , encoding_state, new_state , agents[1].state)
                else :
                    reward, end =  A.get_reward(game , encoding_state, new_state , agents[0].state, i)
                if A.isOpen(game , new_state) :
                    game.grid[new_state[0]][new_state[1]] = A.agent_symbol
                    A.state = new_state
                    game.grid[x][y] = ' '
                #print('--------------------------------------')
                #game.print_game()
                if end == True : 
                    break
            if end == True : 
                self.root.destroy()
                return True
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

'''

def test_GUI_Random() :
    print('Demoing Random Game')
    q = game.game((5,8), walls_prob=0.3)
    q.print_game()
    red = agent(q, symbol = {"R"}, color = 'red')
    blue = agent(q, symbol = {"B"}, color = 'green')
    play = GUI(q)
    play.demo(q, seekers = [red], runners = [blue], game_length=200 ,animation_refresh_seconds=0.08)
        


if __name__ == "__main__":
   print('Testing GUI.py file')
   print('------------------------')
   test_GUI_Random()


