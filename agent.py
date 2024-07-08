import numpy as np
from env import state
import random 
from env import env

class agent:
    def __init__(self):
        self.state = env.build_state(9)
        self.tool = False

    actions = ['up', 'down', 'left', 'right','tunnel', 'take']

    def action_right(self):
        return env.ask_state(self.state, 'right')
    def action_left(self):
        return env.ask_state(self.state, 'left')
    def action_up(self):
        return env.ask_state(self.state, 'up')
    def action_down(self):
        return env.ask_state(self.state, 'down')
    def action_tunnel(self):
        return env.ask_state(self.state, 'tunnel')
    def action_take(self):
        return env.ask_state(self.state, 'take')
    
    def make_step(self,state:state,action):
        step = False
        reward = -1
        if action == 'left':
            state = self.action_left()
        elif action == 'right':
             state = self.action_right()
        elif action == 'up':
            state = self.action_up()
        elif action == 'down':
            state = self.action_down()
        elif action == 'tunnel':
            state = self.action_tunnel()
            if(state.number not in env.tunnel):
                reward = -2
        elif action == 'take':
            if (state.number in env.tools and (not(self.tool))):
                self.tool=True
                reward = 200
        if(self.tool and (state.number in env.stations)):
            reward = 500
            step = True
        else:
            reward = -50

        return state, reward, step

    def improve_policy(self,episode:int, gamma:int, alpha:int):
        tool_q_table = np.zeros((32, 6))
        cook_q_table = np.zeros((32, 6))

        for i in range(episode):
            print(i)
            epsilon = 1 / (i + 1)

            # I reset the state of the agent and the beater every episode
            self.state = env.build_state(random.randint(0, 31))
            self.tool = False
            state = self.state
            step = False

            while not step:
                if np.random.uniform(0, 1) < epsilon:
                    action = np.random.choice(self.actions)
                else:
                    if self.tool:
                        action = self.actions[np.argmax(cook_q_table[state.number - 1])]
                    else:
                        print(state.number)
                        print(action)
                        action = self.actions[np.argmax(tool_q_table[state.number - 1])]

                if self.tool:
                    
                    next_state, reward, step = self.make_step(state,action)
                    cook_q_table[state.number - 1][self.actions.index(action)] += alpha * (
                            reward + gamma * np.max(cook_q_table[next_state.number - 1]) - cook_q_table[state.number - 1][self.actions.index(action)])
                else: 
                    next_state, reward, step = self.make_step(state, action)
                    tool_q_table[state.number - 1][self.actions.index(action)] += alpha * (
                            reward + gamma * np.max(tool_q_table[next_state.number - 1]) - tool_q_table[state.number - 1][self.actions.index(action)])
                        
                state = next_state
                self.state = state

        tool_policy = np.argmax(tool_q_table, axis=1)
        tool_policy = [self.actions[i] for i in tool_policy]

        # The second one is for the agent after the beater is found
        cook_policy = np.argmax(cook_q_table, axis=1)
        cook_policy = [self.actions[i] for i in cook_policy]

        return tool_policy,cook_policy