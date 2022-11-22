from agent import agent
import numpy as np
from util import k_quad_tree


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
    S_Repeat_states = {}
    R_Repeat_states = {}
    tree_strat = False
    for A in seekers + runners :
        if A.learning_style == 'k_quad_tree' :
            tree_strat = True
    k_tree = None
    if tree_strat == True :
        k_tree = k_quad_tree(game, (game.size[0]/2,game.size[1]/2), k=2)
        for i in range(game.size[0]) :
            for j in range(game.size[1]) :
                k_tree.add_data(game,(i,j))

    agent_distances = []
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

            seeker_temp_pos = []
            runner_temp_pos = []

            for S,R in zip(seekers, runners) :
                agent_distances += [Manhattan_distance(S.position,R.position)]

    
            for A in seekers : 
                seeker_states.append( A.encode_Q_State(game, A.position, target_pos=runners[0].position, k_tree = k_tree) )
                '''
                if seeker_states[-1] not in S_Repeat_states.keys() :
                    S_Repeat_states[seeker_states[-1]] = '0' 
                seeker_states[-1] += (S_Repeat_states[seeker_states[-1]],S_Repeat_states[seeker_states[-1]])
                '''
                seeker_temp_pos += [A.position]
            for A in runners : 
                runner_states.append( A.encode_Q_State(game, A.position, target_pos=seekers[0].position, k_tree = k_tree) )
                '''
                if runner_states[-1] not in R_Repeat_states.keys() :
                    R_Repeat_states[runner_states[-1]] = '0' 
                runner_states[-1] += (R_Repeat_states[runner_states[-1]],R_Repeat_states[runner_states[-1]])
                '''
                runner_temp_pos += [A.position]

            for A,state in zip(runners, runner_states) : 
                action = A.Q_table.getAction( state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                #   Updated for runner to move randomly every time (training idea....)
                #action = np.random.choice([action, 'Move_Random'], p = [0, 1])
                new_position, action = A.getNewPosition(game, action, A.position )
                if tree_strat : 
                    k_tree.update_data(game, new_position, A.position, rank = 2)
                runner_next_positions.append( new_position )
                A.moveTO(game, new_position)
                runner_positions += [A.position]
                runner_actions.append( action )
            
            for A,state in zip(seekers, seeker_states) : 
                action = A.Q_table.getAction( state )
                action = np.random.choice([action, 'Move_Random'], p = [(1-epsilon), epsilon])
                new_position, action = A.getNewPosition(game, action, A.position )
                if tree_strat : 
                    k_tree = k_tree.update_data(game, new_position, A.position, rank = 3)
                seeker_next_positions.append( new_position )
                A.moveTO(game, new_position)
                seeker_positions += [A.position]
                seeker_actions.append( action )

            for A, new_position in zip( seekers, seeker_next_positions ) :
                seeker_next_state.append(A.encode_Q_State(game, A.position, target_pos=runners[0].position, k_tree = k_tree))
                if seeker_next_state[-1] in S_Repeat_states.keys() :
                    S_Repeat_states[seeker_next_state[-1]] = str(int(S_Repeat_states[seeker_next_state[-1]])+1) 
                else : S_Repeat_states[seeker_next_state[-1]] = '0' 
                seeker_next_state[-1] += (S_Repeat_states[seeker_next_state[-1]],S_Repeat_states[seeker_next_state[-1]])

                reward, end =  A.get_reward(game , seeker_next_state[-1] , new_position , runners[0].symbol)
                seeker_rewards.append( reward )
                if end == True :
                    stop = True

            runner_index = 0
            for A, new_position in zip( runners, runner_next_positions ) :
                runner_next_state.append(A.encode_Q_State(game, A.position, target_pos=seekers[0].position, k_tree = k_tree))
                if runner_next_state[-1] in R_Repeat_states.keys() :
                    R_Repeat_states[runner_next_state[-1]] = str(int(R_Repeat_states[runner_next_state[-1]])+1) 
                else : R_Repeat_states[runner_next_state[-1]] = '0' 
                runner_next_state[-1] += (R_Repeat_states[runner_next_state[-1]],R_Repeat_states[runner_next_state[-1]])
                reward, end =  A.get_reward(game , runner_next_state[-1] , new_position , seekers[0].symbol)
                runner_rewards.append( reward )
                if end == True :
                    stop = True
                if runner_temp_pos[runner_index] in seeker_temp_pos :
                    runner_rewards[-1] = -1000
                    seeker_rewards[-1] = 1000
                runner_index += 1



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
        'Runner Positions' : runner_positions,
        'states' : S_Repeat_states,
        'Distance' : (max(agent_distances)-min(agent_distances))/(max(agent_distances + [1]))
    }
    return game_info





def Manhattan_distance(pos1 : tuple, pos2 : tuple) :
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
