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
import pickle


possible_moves = ['North', 'East', 'South', 'West', 'Stay_still']



def run_game_instance(
    game,
    seekers : list[agent],
    runners : list[agent],
    game_length = 100,
    epsilon = 0,
    update_strategy = False
) :
    seekers_total_reward = 0
    runners_total_reward = 0
    seeker_positions = []
    runner_positions = []
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


            for A in seekers : seeker_states.append( A.encode_Q_State(game, A.position, target_pos=runners[0].position) ) #  Need to refactor for list of target agents.
            for A in runners : runner_states.append( A.encode_Q_State(game, A.position, target_pos=seekers[0].position) )

            for A,state in zip(seekers, seeker_states) : 
                action = A.Q_table.getAction( state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_position, action = A.getNewPosition(game, action, A.position )
                seeker_next_positions.append( new_position )
                A.moveTO(game, new_position)
                seeker_positions += [A.position]
                seeker_actions.append( action )
                
            
            for A,state in zip(runners, runner_states) : 
                action = A.Q_table.getAction( state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_position, action = A.getNewPosition(game, action, A.position )
                runner_next_positions.append( new_position )
                A.moveTO(game, new_position)
                runner_positions += [A.position]
                runner_next_state.append(A.encode_Q_State(game, A.position, target_pos=seekers[0].position))
                runner_actions.append( action )
                reward, end =  A.get_reward(game , runner_next_state[-1] , new_position , seekers[0].symbol)
                runner_rewards.append( reward )
                if end == True :
                    stop = True
            
            for A, new_position in zip( seekers, seeker_next_positions ) :
                seeker_next_state.append(A.encode_Q_State(game, A.position, target_pos=runners[0].position))
                reward, end =  A.get_reward(game , seeker_next_state[-1] , new_position , runners[0].symbol)
                seeker_rewards.append( reward )
                if end == True :
                    stop = True

            for R in seeker_rewards :
                seekers_total_reward += R
            for R in runner_rewards :
                runners_total_reward += R

            if update_strategy == True :
                for A, state, reward, action, new_state in zip(seekers, seeker_states, seeker_rewards, seeker_actions, seeker_next_state) :
                    A.Q_table.update_q_Table( state,reward,action,new_state )
                for A, state, reward, action, new_state in zip(runners, runner_states, runner_rewards, runner_actions, runner_next_state) :
                    A.Q_table.update_q_Table( state,reward,action,new_state )
            
            if stop == True :
                break
    game_info = {
        'Seeker Reward' : seekers_total_reward,
        'Runner Reward' : runners_total_reward,
        'Game Length' : ii,
        'Seeker Positions' : seeker_positions,
        'Runner Positions' : runner_positions
    }
    return game_info



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
    random_games = True,
    collect_GIF = False
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
        game_info = run_game_instance(
                                    q,
                                    seekers,
                                    runners,
                                    game_length,
                                    epsilon,
                                    update_strategy=True
                                )
        seekers_total_reward , runners_total_reward, ii = game_info['Seeker Reward'],game_info['Runner Reward'], game_info['Game Length']
        seeker_positions += game_info['Seeker Positions']
        runner_positions += game_info['Runner Positions']

        if epoc%100 == 0: 
            print('Epoc: ' + str(epoc)
                + '\t' + 'Seekers: ' + str(seekers_total_reward) 
                + '\t' + 'Runners: ' + str(runners_total_reward) 
                + '\t' + 'Epsilon: ' + str(epsilon)
                + '\t' + 'Game Length: ' + str(ii))
        if epoc%1000 == 0: 
            play = GUI.GUI(q)
            play.play_game(q, seekers=seekers, runners=runners, seekers_moves=seeker_positions,runners_moves=runner_positions, animation_refresh_seconds=animation_refresh_seconds , collect_GIF = collect_GIF )

    return seekers, runners
        

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
    blue = runner(q, symbol = {"B"}, color = 'blue', learning_style='basic')
    blue.Q_table = q_table(moves = blue.possible_moves)

    print('Small Game')
    seekers, runners = basic_Q_learning(q , [red], [blue], 
                                        game_size=(7,7), 
                                        game_length=200,
                                        num_epocs=10000, 
                                        walls_prob=0.2,
                                        animation_refresh_seconds=0.045, 
                                        random_games = True
                                        )
    '''
    print('Medium Game')
    seekers, runners = basic_Q_learning(q , seekers, runners, 
                                        game_size=(10,10), 
                                        game_length=200,
                                        num_epocs=10000, 
                                        walls_prob=0.1,
                                        animation_refresh_seconds=0.045, 
                                        random_games = True)
    print('Large Game')    
    seekers, runners = basic_Q_learning(q , seekers, runners, 
                                        game_size=(15,15), 
                                        game_length=200,
                                        num_epocs=10000, 
                                        walls_prob=0.1,
                                        animation_refresh_seconds=0.045, 
                                        random_games = True)
    '''                                    
    saveAgentToFile(seekers[0] , filename='Seeker.pkl')
    saveAgentToFile(runners[0] , filename='Runner.pkl')



def loadAgents(agentsFileName : list[ str ] ) -> None :
    agents = []

    for file in agentsFileName :
        with open(file, 'rb') as s_file :
            agents += [ pickle.load(s_file) ]
    return agents

def demoAgents(seekers, runners,
                game = None,
                game_length = 200,
                game_size = (7,7),
                walls_prob=0.2,
                epsilon = 0.5,
                animation_refresh_seconds=0.02,
                num_games = 5,
                Random_games = True,
                collect_GIF = False
                ) :
    if all(isinstance(item, str) for item in seekers) :
        seekers = loadAgents(seekers)
    if all(isinstance(item, str) for item in runners) :
        runners = loadAgents(runners)
    if game == None :
        game = game_(size=game_size, walls_prob=walls_prob)
    if collect_GIF : gif_games = []

    for i in range(num_games) :
        if Random_games == True : 
            game = game_(size=game_size, walls_prob=walls_prob)
        for A in seekers + runners :
            A.start_position(game)

        game_info = run_game_instance(
                                    game,
                                    seekers,
                                    runners,
                                    game_length,
                                    epsilon,
                                    update_strategy=False
                                )
        seekers_moves = game_info['Seeker Positions']
        runners_moves = game_info['Runner Positions']
        play = GUI.GUI(game)
        gif_images = play.play_game(
                game,
                seekers,
                runners,
                seekers_moves,
                runners_moves,
                animation_refresh_seconds,
                collect_GIF = True,
                FileName='Game ' + str(i) + " Image "
            )
        if collect_GIF : gif_games += gif_images
    if collect_GIF : play.save_as_GIF(gif_games, 'Test_GIF', 'testGame/')



def saveAgentToFile( obj , filename ) :
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

#single_goal_training()

def testAgents() :
    demoAgents(['Runner.pkl'], ['Seeker.pkl'], num_games = 5, collect_GIF = True)

Tag_training(strat = 'basic_tree')

testAgents()

