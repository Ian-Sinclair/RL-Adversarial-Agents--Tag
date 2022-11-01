from game import game as game_
from agent import agent
import numpy as np
import GUI


possible_moves = ['North', 'East', 'South', 'West', 'Stay_still']


def basic_Q_learning(
    game,
    #seekers : list[agent],
    #hiders : list[agent],
    agents : list[agent],
    num_epocs = 10000,
    game_lenth = 100,
    game_size = (20,20),
    walls_prob=0.25,
    epsilon = 0.5,
    animation_refresh_seconds=0.02
) :
    for epoc in range(num_epocs) :
        q = game_(game_size, walls_prob=walls_prob)
        #for A in seekers : A.start(q)
        #for A in hiders : A.start(q)
        for A in agents : A.start(q)
        seekers_total_reward = 0
        hiders_total_reward = 0

        epsilon = 0.5*(1-((epoc+1)/num_epocs))

        for ii in range(game_lenth) :
            for A in agents :
                x,y = A.state
                encoding_state = A.encode_Q_State(q)
                action = A.q_table.getAction( encoding_state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_state, action = A.q_table.getNewState( action, A.state )
                if A.type == 'seeker' :
                    reward, end =  A.get_reward(q , new_state , agents[1].state)
                else :
                    reward, end =  A.get_reward(q , new_state , agents[0].state, ii)

                if A.type == 'seeker' : seekers_total_reward += reward
                else : hiders_total_reward += reward

                state = A.encode_Q_State(q)
                A.state = new_state
                new_state_ = A.encode_Q_State(q)
                A.state = (x,y)
                if A.isOpen(q , new_state) :
                    q.grid[new_state[0]][new_state[1]] = A.agent_symbol
                    A.state = new_state
                    game.grid[x][y] = ' '
                A.q_table.update_q_Table(state,reward,action,new_state_)
            if end == True : break
                
        if epoc%100 == 0: 
            print('Epoc: ' + str(epoc)
            + '\t' + 'Seekers: ' + str(seekers_total_reward) 
            + '\t' + 'Runners: ' + str(hiders_total_reward) )

        if epoc%100 == 0: 
            play = GUI.GUI()
            play.demo(q, agents)

q = game_((10,10), walls_prob=0.1)
red = agent(q, agent_symbol = "R", agent_color = 'red')
blue = agent(q, agent_symbol = "B", agent_color = 'green', type = 'runner')


basic_Q_learning(q , [red ,blue], game_size=(10,10), game_lenth=250)

