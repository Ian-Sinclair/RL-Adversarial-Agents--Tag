import game
from agent import agent
import numpy as np


possible_moves = ['North', 'East', 'South', 'West', 'Stay_still', 'Move_Random']


def basic_Q_learning(
    game,
    seekers : list[agent],
    hiders : list[agent],
    num_epocs = 10000,
    game_lenth = 100,
    game_size = (20,20),
    walls_prob=0.1,
    epsilon = 0.5,
    animation_refresh_seconds=0.02
) :
    for epoc in range(num_epocs) :
        q = game((20,20), walls_prob=0.1)
        for A in seekers : A.start(q)
        for A in hiders : A.start(q)
        seekers_total_reward = 0
        hiders_total_reward = 0

        epsilon = epsilon*(1-((epoc+1)/num_epocs))

        for ii in range(game_lenth) :
            for A in hiders + seekers :
                x,y = A.state
                encoding_state = A.encode_Q_State()
                action = A.q_table.getAction( encoding_state )
                np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_state = A.q_table.getNewState( action, A.state )
                reward, end =  A.get_reward(q , new_state , hiders[0].state)

                if A.type == 'seeker' : seekers_total_reward += reward
                else : hiders_total_reward += reward

                state = A.encode_Q_State()
                A.state = new_state
                new_state_ = A.encode_Q_State()
                A.state = (x,y)
                if A.isOpen(q , new_state) :
                    q.grid[new_state[0]][new_state[1]] = A.agent_symbol
                    A.state = new_state
                    game.grid[x][y] = ' '
                A.q_table.update_q_Table(state,reward,action,new_state_)
            if end == True : break
                
        if epoc%10 == 0: 
            print('Epoc: ' + epoc
            + '\t' + 'Seekers: ' + str(seekers_total_reward) 
            + '\t' + 'Runners: ' + str(hiders_total_reward) )

q = game((20,20), walls_prob=0.1)
red = agent(q, agent_symbol = "R", agent_color = 'red')
blue = agent(q, agent_symbol = "B", agent_color = 'green', type = 'runner')


basic_Q_learning(q , [red], [blue])

