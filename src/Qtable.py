

'''
    -Ian Sinclair-
    Class that contains a Q-table, along with critical functions for updating and 
    querying the table.
    Generality, table is in the form for a dictionary of dictionaries.
        q_table[state][action] = reward for state action pair.
'''

import numpy as np

class q_table() :
    def __init__(self, 
                func = 'basic',
                moves : list = []) :
        self.possible_moves = moves
        self.q_table = eval('self.'+func + '()')
    
    def basic( self ) : # 3X3 In front of target.
        return {}
    
    #  update method for Q table based on Bellman updates.
    #  If a state has not already been recognized it will be initialized with 0 rewards for all actions.
    #  Every action must be in the list of possible moves for the agent.
    def update_q_Table(self, state, reward, action, new_state, discount = 1, alpha = 0.01) :
        if state not in self.q_table.keys() :
            self.q_table[state] = {}
            for a in self.possible_moves :
                self.q_table[state][a] = 0
        if new_state not in self.q_table.keys() :
            self.q_table[new_state] = {}
            for a in self.possible_moves :
                self.q_table[new_state][a] = 0

        if action in self.possible_moves :
            sample = reward
            if abs(reward) != 60 :
                sample = reward + discount*max(self.q_table[new_state].values())
            self.q_table[state][action] = (
                (1-alpha)*self.q_table[state][action] + alpha*sample
                )
            return True
        return False
    
    #  Given a state returns the action with the highest expected reward (Q value).
    def getAction(self, state) :
        if state in self.q_table.keys() : 
            return max(self.q_table[state], key=self.q_table[state].get)
        return np.random.choice(list(self.possible_moves.keys()))
    
    def print_Qtable(self) :
        print(self.q_table)