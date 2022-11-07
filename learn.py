'''
    Learning set-up file for different agent, environment cponfigurations.
    -- Curently includes
        - single_goal_training() :
            Trains a single agent to find a fixed goal for static (non-changing) environments
            (This is the most basic form of q-learning for path finding.)
        - Tag_training() :
            adversarial agents learn to play tag currently initializes with random grid.
            Demo's current strategy every 1000 epocs or so.
'''



from Qtable import q_table
from game import game as game_
from agent import agent, runner, seeker, fixed_goal
import numpy as np
import GUI


possible_moves = ['North', 'East', 'South', 'West', 'Stay_still']


def basic_Q_learning(
    game,
    seekers : list[agent],
    runners : list[agent],
    #agents : list[agent],
    num_epocs = 10000,
    game_length = 100,
    game_size = (25,25),
    walls_prob=0.25,
    epsilon = 0.5,
    animation_refresh_seconds=0.02,
    random_games = True
) :
    temp = epsilon
    q = game
    for epoc in range(num_epocs) : 
        if random_games == True : q = game_(game_size, walls_prob=walls_prob)
        runner_positions = []
        seeker_positions = []
        for A in seekers : 
            A.start_position(q)
            seeker_positions += [A.position]

        for A in runners : 
            A.start_position(q)
            runner_positions += [A.position]
        seekers_total_reward = 0
        runners_total_reward = 0

        epsilon = temp*(1-((epoc+1)/num_epocs))

        for ii in range(game_length) :
            seeker_states = []
            seeker_actions = []
            seeker_rewards = []
            seeker_next_positions = []
            seeker_next_state = []

            runner_states = []
            runner_actions = []
            runner_rewards = []
            runner_next_positions = []
            runner_next_state = []

            stop = False


            for A in seekers : seeker_states.append( A.encode_Q_State(q, A.position, target_pos=runners[0].position) ) #  Need to refactor for list of target agents.
            for A in runners : runner_states.append( A.encode_Q_State(q, A.position, target_pos=seekers[0].position) )

            for A,state in zip(seekers, seeker_states) : 
                action = A.Q_table.getAction( state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_position, action = A.getNewPosition(q, action, A.position )
                seeker_next_positions.append( new_position )
                A.moveTO(q, new_position)
                seeker_positions += [A.position]
                seeker_actions.append( action )
                
            
            for A,state in zip(runners, runner_states) : 
                action = A.Q_table.getAction( state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_position, action = A.getNewPosition(q, action, A.position )
                runner_next_positions.append( new_position )
                A.moveTO(q, new_position)
                runner_positions += [A.position]
                runner_next_state.append(A.encode_Q_State(q, A.position, target_pos=seekers[0].position))
                runner_actions.append( action )
                reward, end =  A.get_reward(q , runner_next_state[-1] , new_position , seekers[0].symbol)
                runner_rewards.append( reward )
                if end == True :
                    stop = True
            
            for A, new_position in zip( seekers, seeker_next_positions ) :
                seeker_next_state.append(A.encode_Q_State(q, A.position, target_pos=runners[0].position))
                reward, end =  A.get_reward(q , seeker_next_state[-1] , new_position , runners[0].symbol)
                seeker_rewards.append( reward )
                if end == True :
                    stop = True

            for R in seeker_rewards :
                seekers_total_reward += R
            for R in runner_rewards :
                runners_total_reward += R

            for A, state, reward, action, new_state in zip(seekers, seeker_states, seeker_rewards, seeker_actions, seeker_next_state) :
                A.Q_table.update_q_Table( state,reward,action,new_state )

            for A, state, reward, action, new_state in zip(runners, runner_states, runner_rewards, runner_actions, runner_next_state) :
                A.Q_table.update_q_Table( state,reward,action,new_state )
            
            if stop == True :
                break
                

        if epoc%100 == 0: 
            print('Epoc: ' + str(epoc)
                + '\t' + 'Seekers: ' + str(seekers_total_reward) 
                + '\t' + 'Runners: ' + str(runners_total_reward) 
                + '\t' + 'Epsilon: ' + str(epsilon)
                + '\t' + 'Game Length: ' + str(ii))

        if epoc%400 == 0: 
            #q = game_(game_size, walls_prob=walls_prob)
            #seekers[0].Q_table.print_Qtable()
            print(seeker_states[-1])
            print(seekers[0].Q_table.q_table[seeker_states[-1]])
            play = GUI.GUI(q)
            #  play.demo(q, seekers=seekers, runners=runners, game_length=game_length,animation_refresh_seconds=animation_refresh_seconds, epsilon=epsilon, strategy='agent_strategy')
            play.play_game(q, seekers=seekers, runners=runners, seekers_moves=seeker_positions,runners_move=runner_positions, animation_refresh_seconds=animation_refresh_seconds )

    #print(agents[1].q_table.q_table)
    return seekers,runners
        

def single_goal_training() :
    q = game_((10,10), walls_prob=0.2)
    red = seeker(q, symbol = {"R"}, color = 'red', learning_style='basic')
    red.Q_table = q_table(moves = red.possible_moves)
    blue = runner(q, symbol = {"B"}, color = 'green', learning_style='basic')
    blue.Q_table = q_table(moves = blue.possible_moves)

    yellow = fixed_goal(q, symbol = {"F"}, learning_style='basic')
    yellow.Q_table = q_table(moves = yellow.possible_moves)

    seekers, runners = basic_Q_learning(q , [red], [yellow], game_size=(10,10), game_length=200,num_epocs=20000, walls_prob=0.2,animation_refresh_seconds=0.045, random_games = False)

def Tag_training(strat = 'basic') :
    q = game_((10,10), walls_prob=0.2)
    red = seeker(q, symbol = {"R"}, color = 'red', learning_style=strat)
    red.Q_table = q_table(moves = red.possible_moves)
    blue = runner(q, symbol = {"B"}, color = 'green', learning_style='basic')
    blue.Q_table = q_table(moves = blue.possible_moves)

    print('Small Game')
    seekers, runners = basic_Q_learning(q , [red], [blue], 
                                        game_size=(6,6), 
                                        game_length=200,
                                        num_epocs=20000, 
                                        walls_prob=0.2,
                                        animation_refresh_seconds=0.045, 
                                        random_games = True)
    '''
    print('Medium Game')
    seekers, runners = basic_Q_learning(q , seekers, runners, 
                                        game_size=(10,10), 
                                        game_length=200,
                                        num_epocs=20000, 
                                        walls_prob=0.2,
                                        animation_refresh_seconds=0.045, 
                                        random_games = True)
    print('Large Game')
    seekers, runners = basic_Q_learning(q , seekers, runners, 
                                        game_size=(15,15), 
                                        game_length=200,
                                        num_epocs=20000, 
                                        walls_prob=0.2,
                                        animation_refresh_seconds=0.045, 
                                        random_games = True)

    '''


#single_goal_training()

Tag_training(strat = 'basic_tree')

