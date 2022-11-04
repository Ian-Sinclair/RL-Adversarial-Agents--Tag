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
    temp = epsilon

    for epoc in range(num_epocs) :
        #for A in seekers : A.start(q)
        #for A in hiders : A.start(q)
        q = game_(game_size, walls_prob=walls_prob)

        for A in agents : 
            A.state=None
            A.start(q)
        seekers_total_reward = 0
        hiders_total_reward = 0

        epsilon = temp*(1-((epoc+1)/num_epocs))
        for ii in range(game_lenth) :
            for A in agents :
                x,y = A.state
                if A.type == 'seeker' :
                    encoding_state = A.encode_Q_State(q, A.state, target_pos=agents[1].state)
                else :
                    encoding_state = A.encode_Q_State(q, A.state, target_pos=agents[0].state)
                action = A.q_table.getAction( encoding_state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_state, action = A.q_table.getNewState(q, action, A.state )
                if A.type == 'seeker' :
                    reward, end =  A.get_reward(q , encoding_state , new_state , agents[1].agent_symbol)
                else :
                    reward, end =  A.get_reward(q , encoding_state , new_state , agents[0].agent_symbol, ii)

                if A.type == 'seeker' : seekers_total_reward += reward
                else : hiders_total_reward += reward
                if A.isOpen(q , new_state) :
                    q.grid[new_state[0]][new_state[1]] = A.agent_symbol
                    A.state = new_state
                    q.grid[x][y] = " "
                else : new_state = A.state
                if A.type == 'seeker' :
                    new_state_ = A.encode_Q_State(q, new_state, target_pos=agents[1].state)
                else :
                    new_state_ = A.encode_Q_State(q, new_state, target_pos=agents[0].state)
                A.q_table.update_q_Table(encoding_state,reward,action,new_state_)
                if end == True :
                    for B in agents :
                        if B is not A :
                            x,y = B.state
                            if B.type == 'seeker' :
                                encoding_state = B.encode_Q_State(q, B.state, target_pos=agents[1].state)
                            else :
                                encoding_state = B.encode_Q_State(q, B.state, target_pos=agents[0].state)
                            action = B.q_table.getAction( encoding_state )
                            action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                            new_state = B.state
                            if B.type == 'seeker' :
                                reward =  1000
                            else :
                                reward = -1000

                            if B.type == 'seeker' : seekers_total_reward += reward
                            else : hiders_total_reward += reward
                            if B.isOpen(q , new_state) :
                                q.grid[new_state[0]][new_state[1]] = B.agent_symbol
                                B.state = new_state
                                q.grid[x][y] = " "
                            else : new_state = B.state
                            if B.type == 'seeker' :
                                new_state_ = B.encode_Q_State(q, new_state, target_pos=agents[1].state)
                            else :
                                new_state_ = B.encode_Q_State(q, new_state, target_pos=agents[0].state)

                            B.q_table.update_q_Table(encoding_state,reward,action,new_state_)
                    break
            if end == True : break
                
        if epoc%100 == 0: 
            print('Epoc: ' + str(epoc)
            + '\t' + 'Seekers: ' + str(seekers_total_reward) 
            + '\t' + 'Runners: ' + str(hiders_total_reward) 
            + '\t' + 'Epsilon: ' + str(epsilon)
            + '\t' + 'Game Length: ' + str(ii))

        if epoc%500 == 0: 
            play = GUI.GUI()
            play.demo(q, agents, game_lenth=game_lenth,animation_refresh_seconds=animation_refresh_seconds, epsilon=epsilon)

    #print(agents[1].q_table.q_table)
    return agents

q = game_((10,10), walls_prob=0)
red = agent(q, agent_symbol = "R", agent_color = 'red', learning_style='basic_tree')
blue = agent(q, agent_symbol = "B", agent_color = 'green', type = 'runner', learning_style='basic_tree')


agents = [red,blue]
agents = basic_Q_learning(q , agents, game_size=(10,10), game_lenth=200,num_epocs=10000, walls_prob=0.15,animation_refresh_seconds=0.06)

print('Demoing')
'''
for i in range(50) :
    q = game_((6,6), walls_prob=0.15)
    play = GUI.GUI()
    play.demo(q, agents, game_lenth=400, animation_refresh_seconds=0.04)
'''
#print('Strarting New Training Strategy')
#agents = basic_Q_learning(q , agents, game_size=(13,13), game_lenth=400,num_epocs=30000, epsilon=0.3, walls_prob=0.1)



