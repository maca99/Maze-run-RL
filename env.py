import utils
import numpy as np
import pandas as pd

class env:

    ## Here we define the constants of the environment
    len_y = 4 
    len_x = 8
    #Si deve implementare un metodo che dia uno stato iniziale casuale.
    DISCOUNT_FACTOR = 0


    def __init__(self):
        
        ## STATES AND ACTIONS
        self.states = [env.build_state(i,j) for i in range(1,env.len_x+1) for j in range(1,env.len_y+1)]
        self.states_index = [state.name for state in self.states]
        ## STARTING STATE
        number_state=utils.select_first_state()
        #da modificare
        self.starting_state = env.build_state(number_state[0],number_state[1])
        self.current_state = self.starting_state

        ## We build the actions
        self.actions = []
        for action in env.actions:
            self.actions.append(env.build_action(env.actions[action], action))

##Da MOdificare!!!!!!!!
        
        ## PROBABILITY MATRIX AND REWARDS
        #self.probability_matrix, self.stateaction_dict = utils.build_probability_matrix(self.states, self.actions)
        #self.probability_matrix_df = utils.build_df(self.probability_matrix, self.stateaction_dict, self.states_index)

        #self.rewards, self.action_dict = utils.build_rewards(self.states, self.actions)
        #self.rewards_df = utils.build_df(self.rewards, self.action_dict, self.states_index)
        
    
    rewards = {'(1,1)':100,'(1,9)':100,'(6,3)':1000}


    ## ACTIONS
        ##Azioni vietate
    up_forbidden = [(1,1),(1,3),(2,1),(2,2),(3,1),(3,2),(7,1),(7,3),(8,3),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4)]

    down_forbidden = [(1,2),(1,4),(2,2),(2,3),(2,4),(3,2),(3,3),(7,2),(7,4),(8,4),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1)]

    right_forbidden = [(1,3),(6,2),(6,3),(4,1),(4,2),(4,3),(4,4),(5,1),(5,2),(5,3),(5,4),(9,1),(9,2),(9,3),(9,4)]

    left_forbidden = [(2,3),(7,2),(7,3),(1,1),(1,2),(1,3),(1,4),(5,1),(5,2),(5,3),(5,4),(6,1),(6,2),(6,3),(6,4),(8,2),(8,3)]

    def ask_state(state,action):
        if action == 'right':
           return env.action_right(state)
        if action == 'left': 
           return env.action_left(state)
        if action == 'up':
            return env.action_up(state)
        if action == 'down':
            return env.action_down(state)

    ## ACTIONS  
    def action_up(state):
        if((state.x,state.y) in env.up_forbidden):
            return {state:1}
        else:
            return {env.build_state(state.x,state.y+1):1}
      
    def action_down(state):
        if((state.x,state.y) in env.down_forbidden):
            return {state:1}
        else:
            return {env.build_state(state.x,state.y-1):1}
    
    def action_right(state):
        if((state.x,state.y) in env.right_forbidden):
            return {state:1}
        else:
            return {env.build_state(state.x+1,state):1}
        
    def action_left(state):
        if((state.x,state.y) in env.left_forbidden):
            return {state:1}
        else:
            return {env.build_state(state.x-1,state.y):1}
        
    def action_tunnel(state):
        if((state.x,state.y) == (2,4)):
            return {env.build_state(3,9):1}
        if((state.x,state.y) == (3,9)):
            return {env.build_state(2,4):1}
        return {state:1}
        
    actions = {'left': action_left, 'right': action_right,'up': action_up, 'down': action_down, 'tunnel': action_tunnel}
        
    
    def build_action(function, name):
        return utils.action(function, name)

    def build_state(x,y):
        action_list = []

        for action in env.actions:
            if(action == "left" and (x,y) in env.left_forbidden):
                continue
            if(action == "right" and (x,y) in env.right_forbidden):
                continue
            if(action == "up" and (x,y) in env.up_forbidden):
                continue
            if(action == "down" and (x,y) in env.down_forbidden):
                continue

            action_list.append( env.build_action( env.actions[action] ,action ))

        key = "("+str(x)+","+str(y)+")"
        rew = env.rewards[key] if str(key) in env.rewards else 0

        return utils.state(x,y, action_list, rew)
    
    

