'''
    Learning set-up file for different agent, environment configurations.
    -- Currently includes
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
from game_instance import run_game_instance
import numpy as np
import GUI
import pickle
import random
import sys, getopt
import os


possible_moves = ['North', 'East', 'South', 'West', 'Stay_still']
protected_file_names = []

def learning_instance(
            seekers : list[agent],
            runners : list[agent],
            game = None,
            game_type = 'randomGrid',
            num_epocs = 100000,
            game_length = 200,
            game_size = (10,10),
            walls_prob=0.25,
            epsilon = 0.5,
            animation_refresh_seconds=0.02,
            random_games = True,
        ) :
    temp = epsilon
    if game == None : game = game_(game_size, walls_prob=random.random()*walls_prob, fillFunc=game_type)
    for epoc in range(num_epocs) : 
        size = random.randint( 10 , max( [ 10 , game_size[0] ] ) )
        if random_games == True : game = game_(game_size, walls_prob=random.random()*walls_prob, fillFunc=game_type)
        runner_positions = []
        seeker_positions = []
        for A in seekers : 
            A.start_position(game)
            seeker_positions += [A.position]

        for A in runners : 
            A.start_position(game)
            runner_positions += [A.position]

        epsilon = temp*(1-epoc/num_epocs)
        seekers_total_reward = 0
        runners_total_reward = 0
        game_info = run_game_instance(
                                    game,
                                    seekers,
                                    runners,
                                    game_length,
                                    epsilon = epsilon,
                                    update_strategy=True
                                )
        seekers_total_reward , runners_total_reward, ii = game_info['Seeker Reward'],game_info['Runner Reward'], game_info['Game Length']
        states = game_info['states']
        seeker_positions += game_info['Seeker Positions']
        runner_positions += game_info['Runner Positions']

        if epoc%100 == 0: 
            print('Epoc: ' + str(epoc)
                + '\t' + 'Seekers Reward: ' + str(seekers_total_reward) 
                + '\t' + 'Runners Reward: ' + str(runners_total_reward) 
                + '\t' + 'Epsilon: ' + str(epsilon)
                + '\t' + 'Game Length: ' + str(ii))
        if epoc%1000 == 0 : 
            play = GUI.GUI(game)
            play.play_game(game, 
                            seekers=seekers, 
                            runners=runners, 
                            seekers_moves=seeker_positions, 
                            runners_moves=runner_positions, 
                            animation_refresh_seconds=animation_refresh_seconds)
    return seekers, runners

def single_goal_training() :
    q = game_((8,8), walls_prob=0.2)
    red = seeker(q, symbol = {"R"}, color = 'red', learning_style='basic')
    red.Q_table = q_table(moves = red.possible_moves)
    blue = runner(q, symbol = {"B"}, color = 'green', learning_style='basic')
    blue.Q_table = q_table(moves = blue.possible_moves)

    yellow = fixed_goal(q, symbol = {"F"}, learning_style='basic')
    yellow.Q_table = q_table(moves = yellow.possible_moves) 

    seekers, runners = learning_instance(q , 
                                        [red], 
                                        [yellow], 
                                        game_size=(8,8), 
                                        game_length=200,
                                        num_epocs=20000, 
                                        walls_prob=0.2,
                                        animation_refresh_seconds=0.045, 
                                        random_games = False)


def default_curriculum(
        seekers = None,
        runners = None,
        seeker_strat = 'basic',
        runner_strat = 'basic',
        seeker_file = None,
        runner_file = None
    ) :
    game = game_((10,10), walls_prob=0)
    if seekers == None :
        seekers = seeker(game, symbol = {"R"}, color = 'red', learning_style=seeker_strat)
        moves = seekers.possible_moves
        new_moves = {'NortEast' : (-1,1), 'SouthEast' : (1,1) , 'NorthWest' : (-1,-1) , 'SouthWest' : (1,-1)}
        for key , item in new_moves.items() : moves[key] = item
        seekers.Q_table = q_table(moves = moves)

    if runners == None :
        runners = runner(game, symbol = {"B"}, color = 'blue', learning_style=runner_strat)
        moves = runners.possible_moves
        new_moves = {'NortEast' : (-1,1), 'SouthEast' : (1,1) , 'NorthWest' : (-1,-1) , 'SouthWest' : (1,-1)}
        for key , item in new_moves.items() : moves[key] = item
        runners.Q_table = q_table(moves = moves)


    print('Class Schedule: \n \
         1) large randomGrid 10,000 epocs \n \
         2) small roomsGrid 30,000 epocs \n \
         3) large roomsGrid 60,000 epocs')

    print('-'*30)
    print('Starting Training')
    print('-'*30)

    print('1) large randomGrid 10,000 epocs')
    seekers , runners = learning_instance(
            [seekers],
            [runners],
            game = None,
            game_type = 'randomGrid',
            num_epocs = 10000,
            game_length = 200,
            game_size = (15,15),
            walls_prob=0.4,
            epsilon = 0.5,
            animation_refresh_seconds=0.02,
            random_games = True,
        )
    print('-'*30)
    print('phase 1 complete')
    print('states added to q_table: ' + str(len(seekers[0].Q_table.q_table.keys())))
    print('-'*30)
    print('-'*30)
    print('2) small roomsGrid 30,000 epocs')
    seekers , runners = learning_instance(
            seekers,
            runners,
            game = None,
            game_type = 'roomsGrid',
            num_epocs = 30000,
            game_length = 200,
            game_size = (10,10),
            walls_prob=0.4,
            epsilon = 0.5,
            animation_refresh_seconds=0.02,
            random_games = True,
        )
    print('-'*30)
    print('phase 2 complete')
    print('states added to q_table: ' + str(len(seekers[0].Q_table.q_table.keys())))
    print('-'*30)
    print('-'*30)
    print('3) large roomsGrid 60,000 epocs')
    seekers , runners = learning_instance(
            seekers,
            runners,
            game = None,
            game_type = 'roomsGrid',
            num_epocs = 60000,
            game_length = 200,
            game_size = (25,25),
            walls_prob=0.4,
            epsilon = 0.5,
            animation_refresh_seconds=0.02,
            random_games = True,
        )
    print('phase 3 complete')
    print('states added to q_table: ' + str(len(seekers[0].Q_table.q_table.keys())))
    print('-'*30)
    print('-'*30)
    if seeker_file != None : 
        print('saving seekers to ' + str(seeker_file))
        saveAgentToFile(seekers[0] , filename=seeker_file)
    if runner_file != None : 
        print('saving seekers to ' + str(runner_file))
        saveAgentToFile(runners[0] , filename=runner_file)

    return seekers, runners
    



def loadAgents(agentsFileName : list[ str ] ) -> None :
    agents = []

    for file in agentsFileName :
        with open(file, 'rb') as s_file :
            agents += [ pickle.load(s_file) ]
    return agents

def saveAgentToFile( obj , filename ) :
    with open(filename, 'wb') as out:  # Overwrites any existing file.
        pickle.dump(obj, out, pickle.HIGHEST_PROTOCOL)



def main(argv) :
    try :
      opts, args = getopt.getopt(argv, "t:z:n:l:p:e:g:",
                                ["SFile=","RFile="])
    except getopt.GetoptError:
      print('test.py -g <board type>  \
            -n <number of games \
            -l <game length> \
            -p <wall probability> \
            -e <animation refresh speed> \
            -g <collect gif to file location> \
            --SFile <seeker file location> \
            --RFile <Runner file location>')
      sys.exit(2)


if __name__ == "__main__":
    default_curriculum(seeker_strat = 'basic_tree', runner_strat= 'basic_tree', seeker_file = 'Seeker.pkl', runner_file = 'Runner.pkl')
    main(sys.argv[1:])

