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

import csv
from statistics import mean
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
            collect_data = False,
            update_strategy = True
        ) :
    temp = epsilon
    run_info = []
    demo_games = []
    if game == None : game = game_(game_size, walls_prob=random.random()*walls_prob, fillFunc=game_type)
    for epoc in range(num_epocs) : 
        size = random.randint( 10 , max( [ 10 , game_size[0] ] ) )
        if random_games == True : game = game_((size,size), walls_prob=random.random()*walls_prob, fillFunc=game_type)
        runner_positions = []
        seeker_positions = []
        for A in seekers : 
            A.start_position(game)
            seeker_positions += [A.position]

        for A in runners : 
            A.start_position(game)
            runner_positions += [A.position]

        #epsilon = temp*(1-epoc/num_epocs)
        seekers_total_reward = 0
        runners_total_reward = 0
        game_info = run_game_instance(
                                    game,
                                    seekers,
                                    runners,
                                    game_length,
                                    epsilon = epsilon,
                                    update_strategy=update_strategy
                                )
        run_info += [game_info]
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
        if epoc%1000 and epoc > num_epocs-10 :
            demo_games += [{'game' : game , 'seeker moves' : game_info['Seeker Positions'] , 'runner moves' : game_info['Runner Positions']}]
    if collect_data == True :
        return seekers , runners, run_info, demo_games
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

def data_collection(
    seekers : list[str],
    runners : list[str],
    game_length_file = None,
    distance_between_agents_file = None,
    num_epocs = 10000,
    game_type = 'randomGrid',
    game_size = (20,20),
    walls_prob = 0.4,
    epsilon = 0,
    animation_refresh_seconds = 0.02,
    GIF_Bool = True,
    GIF_File = 'testGIF'
) :
    if type(seekers) != type([1,2]) : seekers = [seekers]
    if type(runners) != type([1,2]) : runners = [runners]
    seekers = loadAgents(seekers)
    runners = loadAgents(runners)

    seekers , runners , run_info, demos = learning_instance(
                                            seekers,
                                            runners,
                                            game = None,
                                            game_type = game_type,
                                            num_epocs = num_epocs,
                                            game_length = 200,
                                            game_size = game_size,
                                            walls_prob=walls_prob,
                                            epsilon = 1,
                                            animation_refresh_seconds=animation_refresh_seconds,
                                            random_games = True,
                                            collect_data=True,
                                            update_strategy = False
        )
    if game_length_file != None :
        if not os.path.exists('Results/') :
            os.makedirs('Results/')
        game_length_data = []
        window = []
        j = 0
        for i,info in enumerate(run_info) :
            window += [info['Game Length']]
            if i %100 == 0 :
                game_length_data += [{'index' : j, 'average game length' : mean(window)}]
                window = []
                j += 1
        with open('Results/' + game_length_file, 'w') as f:  # You will need 'wb' mode in Python 2.x
            w = csv.DictWriter(f, list(game_length_data[0].keys()))
            w.writeheader()
            for data in game_length_data :
                w.writerow(dict(data))
    
    if distance_between_agents_file != None :
        if not os.path.exists('Results/') :
            os.makedirs('Results/')
        game_distance_data = []
        window = []
        j = 0
        for i,info in enumerate(run_info) :
            window += [info['Distance']]
            if i %100 == 0 :
                game_distance_data += [{'index' : j, 'average distance' : mean(window)}]
                window = []
                j += 1
        with open('Results/' + distance_between_agents_file, 'w') as f:
            w = csv.DictWriter(f, list(game_distance_data[0].keys()))
            w.writeheader()
            for data in game_distance_data :
                w.writerow(dict(data))
    gif_games = []
    k = 0
    for info in demos : 
        play = GUI.GUI(info['game'])
        gif_images = play.play_game(
                info['game'],
                seekers,
                runners,
                info['seeker moves'],
                info['runner moves'],
                animation_refresh_seconds,
                collect_GIF = True,
                FileName='Game ' + str(k) + " Image "
            )
        k += 1
        if GIF_Bool : gif_games += gif_images
    if GIF_Bool : play.save_as_GIF(gif_games, GIF_File, 'GIFs/')



def random_curriculum (
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

        seekers , runners = learning_instance(
                                            [seekers],
                                            [runners],
                                            game = None,
                                            game_type = 'randomGrid',
                                            num_epocs = 40000,
                                            game_length = 200,
                                            game_size = (14,14),
                                            walls_prob=0.4,
                                            epsilon = 0.5,
                                            animation_refresh_seconds=0.02,
                                            random_games = True,
        )
    print('-'*30)
    print('phase 1 complete')
    if seeker_file != None : 
        print('saving seekers to ' + str(seeker_file))
        saveAgentToFile(seekers[0] , filename=seeker_file)
    if runner_file != None : 
        print('saving seekers to ' + str(runner_file))
        saveAgentToFile(runners[0] , filename=runner_file)

    return seekers, runners

    



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



    phase_1 = True
    phase_2 = True
    phase_3 = True
    print('Class Schedule: \n \
         1) large randomGrid 5,000 epocs \n \
         2) small roomsGrid 5,000 epocs \n \
         3) large uniformGrid 5,000 epocs')

    print('-'*30)
    print('Starting Training')
    print('-'*30)

    if phase_1 :
        print('1) large randomGrid 5,000 epocs')
        seekers , runners = learning_instance(
                [seekers],
                [runners],
                game = None,
                game_type = 'randomGrid',
                num_epocs = 5000,
                game_length = 200,
                game_size = (12,12),
                walls_prob=0.4,
                epsilon = 0.5,
                animation_refresh_seconds=0.02,
                random_games = True,
            )
    print('-'*30)
    print('phase 1 complete')
    print('-'*30)
    print('-'*30)
    if phase_2 :
        print('2) small roomsGrid 5,000 epocs')
        seekers , runners = learning_instance(
                seekers,
                runners,
                game = None,
                game_type = 'roomsGrid',
                num_epocs = 5000,
                game_length = 200,
                game_size = (10,10),
                walls_prob=0.3,
                epsilon = 0.5,
                animation_refresh_seconds=0.02,
                random_games = True,
            )
    print('-'*30)
    print('phase 2 complete')
    print('-'*30)
    print('-'*30)
    if phase_3 :
        print('3) large uniformGrid 5000 epocs')
        seekers , runners = learning_instance(
                seekers,
                runners,
                game = None,
                game_type = 'uniformGrid',
                num_epocs = 5000,
                game_length = 200,
                game_size = (20,20),
                walls_prob=0.4,
                epsilon = 0.5,
                animation_refresh_seconds=0.02,
                random_games = True,
            )
        print('phase 3 complete')
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
    seeker_strat = 'basic_tree'
    runner_strat = 'basic_tree'
    seeker_file = None
    runner_file = None
    game_length_outfile = None
    Avg_Distance_outfile = None
    GIF_outfile = None

    run_random = False

    try :
      opts, args = getopt.getopt(argv, "zS:R:",
                                ["SFile=","RFile=", "gm_lng_file=", "AVG_dis_file=", "GIF_file="])
    except getopt.GetoptError:
        print('-z runs long training process \
            -S <seeker strategy>\
                -R <> runner strategy\
            -GIF_file <collect gif to file location> \
            --SFile <seeker file location> \
            --RFile <Runner file location>\
                --gm_lng_file <returns average games per 1000 across training>\
                    --AVG_dis_file <returns normalized average change in distance between agents>')
        sys.exit(2)
    for opt , arg in opts :
        if opt == '-z' :
            run_random = True
        if opt == '-S' :
            seeker_strat = arg
        if opt == '-R' :
            runner_strat = arg
        if opt == '--SFile' :
            seeker_file = arg
        if opt == '--RFile' :
            runner_file = arg
        if opt == '--gm_lng_file' :
            game_length_outfile = arg
        if opt == '--AVG_dis_file' :
            Avg_Distance_outfile = arg
        if opt == '--GIF_file' :
            GIF_outfile = arg


    if run_random : 
        random_curriculum(seeker_strat=seeker_strat,runner_strat=runner_strat,seeker_file=seeker_file,runner_file=runner_file)
        data_collection(seeker_file, runner_file, game_length_outfile, Avg_Distance_outfile, GIF_File = GIF_outfile)
        sys.exit(2)

    default_curriculum(seeker_strat='basic_tree',runner_strat='basic_tree',seeker_file='Default_Seeker.pkl',runner_file='Default_Runner.pkl')


if __name__ == "__main__":
    #default_curriculum(seeker_strat = 'k_quad_tree', runner_strat= 'basic', seeker_file = 'SeekerTest.pkl', runner_file = 'RunnerTest.pkl')
    #random_curriculum(seeker_strat='basic_tree',runner_strat='basic_tree',seeker_file='Seeker_Basic_Tree.pkl',runner_file='Runner_Basic_Tree.pkl')
    data_collection('Seeker.pkl', 'Runner.pkl', 'Random_game_length_file.csv', 'Random_Avg_Distance.csv', GIF_File = None)
    #main(sys.argv[1:])

    # python learn.py -z -S 'basic_tree' -R 'basic_tree' --Sfile Seeker_Basic_Tree.pkl --Rfile Runner_Basic_Tree.pkl --gm_lng_file Test_game_length_file.csv --AVG_dis_file Test_Avg_Distance.csv --GIF_file TreeGIF

