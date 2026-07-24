import numpy as np
import pandas as pd

class state:
    def __init__(self, number):
        self.number = number

class env:

    ## Here we define the constants of the environment
    DISCOUNT_FACTOR = 0


    def __init__(self,starting_state):
        
        ## STATES AND ACTIONS
        self.states = [env.build_state(i) for i in range(0,32)]
        self.states_index = [state.number for state in self.states]
        self.current_state = self.starting_state    
        
        ## We build the actions
        self.actions = []
        for action in env.actions:
            self.actions.append(env.build_action(env.actions[action], action))    
    
    rewards = {}


    ## ACTIONS
    up_forbidden = [(0),(1),(2),(6),(9),(10),(16),(22),(23),(24),(25),(26),(27),(28),(29),(30),(31)]

    down_forbidden = [(0),(1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(14),(17),(18),(24),(30),(31)]

    right_forbidden = [(3),(7),(11),(13),(15),(16),(19),(21),(23),(27),(31)]

    left_forbidden = [(0),(4),(8),(12),(14),(16),(17),(20),(22),(24),(28)]

    tunnel = [(11),(23)]

    tools = [(16),(22)]

    stations = [(24),(30)]


    def ask_state(state:state,action):
        if action == 'right':
           return env.action_right(state)
        if action == 'left': 
           return env.action_left(state)
        if action == 'up':
            return env.action_up(state)
        if action == 'down':
            return env.action_down(state)
        if action == 'tunnel':
            return env.action_tunnel(state)
        if action == 'take':
            return env.action_take(state)

    ## ACTIONS  
    def action_up(state:state):
        if(state.number in env.up_forbidden):
            return None
        else:
            return env.build_state(state.number +8)
      
    def action_down(state:state):
        if(state.number in env.down_forbidden):
            return None
        else:
            return env.build_state(state.number -8)
    
    def action_right(state:state):
        if(state.number in env.right_forbidden):
            return None
        else:
            return env.build_state(state.number +1)
        
    def action_left(state:state):
        if(state.number in env.left_forbidden):
            return None
        else:
            return env.build_state(state.number -1)
        
    def action_tunnel(state:state):
        if(state.number == 11):
            return env.build_state(23)
        elif(state.number == 23):
            return env.build_state(11)
        else:
            return None
    
    def action_take(state:state):
        return state
        
        
    actions = {'left': action_left, 'right': action_right,'up': action_up, 'down': action_down, 'tunnel': action_tunnel, 'take': action_take}

    def build_state(number):
        action_list = []
        
        for action in env.actions:
            action_list.append( env.actions[action])

        return state(number)
    
    def build_state(number):
        action_list = []
        
        for action in env.actions:
            action_list.append( env.actions[action])

        return state(number)
    
    

