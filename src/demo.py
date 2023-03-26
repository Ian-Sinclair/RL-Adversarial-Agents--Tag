'''
    -Ian Sinclair-
    File handles displaying games and running the AI for each agents.
    This is the main function to call when exploring the quality of agents learning
    after training.

'''
from game_instance import run_game_instance
from game import game as game_
import GUI
import sys, getopt
import os
import random
import pickle



def loadAgents(agentsFileName : list[ str ] ) -> None :
    agents = []
    for file in agentsFileName :
        with open(file, 'rb') as s_file :
            agents += [ pickle.load(s_file) ]
    return agents



def demo_run(seekers, 
                runners,
                game_length = 200,
                game_size = (15,15),
                walls_prob=0.3,
                animation_refresh_seconds=0.02,
                num_games = 10,
                Random_games = True,
                collect_GIF = None,
                GIF_Bool = False,
                game_type = 'randomGrid') :
    if collect_GIF != None :
        GIF_Bool = True
        gif_games = []

    seekers = loadAgents(seekers)
    runners = loadAgents(runners)
    
    for i in range(num_games) :
        game = game_(size=game_size, walls_prob=random.random()*walls_prob, fillFunc=game_type)
        for A in seekers + runners :
            A.position = None
        for A in seekers + runners :
            A.start_position(game)
        
        game_info = run_game_instance(
                                    game,
                                    seekers,
                                    runners,
                                    game_length = game_length,
                                    epsilon = 0,
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
                collect_GIF = GIF_Bool,
                FileName='Game ' + str(i) + " Image "
            )
        if GIF_Bool : gif_games += gif_images
    if GIF_Bool : play.save_as_GIF(gif_games, collect_GIF, 'GIFs/')






def main(argv) :
    try :
      opts, args = getopt.getopt(argv, "t:z:n:l:p:e:g:",
                                ["SFile=","RFile="])
    except getopt.GetoptError:
      print('test.py -g <board type>  \
            -n <number of games \
            -l <game length> \
                -p <wall probability>\
                    -e <animation refresh speed> \
                        -g <collect gif to file location>\
                            SFile <seeker file location>\
                                RFile <Runner file location>')
      sys.exit(2)
    
    Seekers = 'Q_tables/Seeker.pkl'
    Runners = 'Q_tables/Runner.pkl'
    game_size = (15,15)
    collect_GIF = None
    game_type = 'randomGrid'
    num_games = 10
    game_length = 200
    wall_prob = 0.3
    animation_refresh_speed = 0.02
    for opt , arg in opts :
        if opt == '-t' :
            if arg not in ['uniformGrid' , 'randomGrid' , 'roomsGrid', 'emptyGrid'] :
                raise ValueError('game type (-g <type>) must be in -g <' + str(['uniformGrid' , 'randomGrid' , 'roomsGrid']) + '>')
            game_type = arg
        
        if opt == '-z' :
            if type(int(arg)) != type(1) :
                raise TypeError('game board size -z <size> must be of type INT.')            
            game_size = (int(arg),int(arg))
        if opt == '-n' :
            if type(int(arg)) != type(int(1)) :
                raise TypeError('number of games -n <num games> must be of type INT.')
            num_games = int(arg)

        if opt == '-l' :
            if type(int(arg)) != type(1) :
                raise TypeError('game length -l <length> must be of type INT.')
            if int(arg) < 0 :
                raise ValueError('game length -l <length> must be greater than 0')
            game_length = int(arg)
        
        if opt == '-p' :
            if not 0<= float(arg) <= 1 :
                raise ValueError('wall probability -p <prob> must be of be in [0,1].')
            wall_prob = float(arg)
        
        if opt == '-e' :
            animation_refresh_speed = float(arg)
        
        if opt == '-g' :
            if type(arg) != type(' ') :
                raise TypeError('collect GIF -g <file location> must be of type string')
            #if not os._exists(arg) :
            #    raise ValueError(' -g <GIF file save location> Cannot find file for GIF location under path: ' +str(arg) )
            collect_GIF = arg
        
        if opt == '--SFile' :
            if type(arg) != type(' ') :
                raise TypeError('Seeker file --SFile <file location> must be of type string')
            #if not os._exists(arg) :
            #    raise ValueError(' --SFile <seeker file location> Cannot find file for seeker location under path: ' +str(arg) )
            Seekers = arg

        if opt == '--RFile' :
            if type(arg) != type(' ') :
                raise TypeError('Runner file --RFile <file location> must be of type string')
            #if not os.exists(arg) :
            #    raise ValueError(' --RFile <runner file location> Cannot find file for seeker location under path: ' +str(arg) )
            Runners = arg
    if Runners == None or Seekers == None :
        raise ValueError('Argument Error: File locations for seeker and runner agents are required.  --SFile <seeker file location> , --RFile <Runner File location>')
    
    demo_run(seekers = [Seekers], 
            runners = [Runners],
            game_length = game_length,
            game_size = game_size,
            walls_prob=wall_prob,
            animation_refresh_seconds=animation_refresh_speed,
            num_games = num_games,
            collect_GIF = collect_GIF,
            game_type = game_type)


        

if __name__ == "__main__":
    '''
    #####  Input Key #####
    -t : game board type  -> ['uniformGrid' , 'randomGrid' , 'roomsGrid', 'emptyGrid']
    -z : game board size -> default 15
    -n : number of games (int) -> default 10
    -l : game length -> default 200
    -p : wall probability (only for random grid) -> default 0.3
    -e : animation refresh speed
    -g : collects GIF of run at file location of argument
    -SFile : file location of seeker
    -RFile : file location of runner
    '''
    main(sys.argv[1:])



