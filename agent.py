import numpy as np
from env import state
import random 
from env import env

class agent:
    def __init__(self,state: int,tool: bool):
        self.state = env.build_state(state)
        self.tool=tool

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
        reward = -5
        if action == 'left':
            state = self.action_left()
        if action == 'right':
             state = self.action_right()
        if action == 'up':
            state = self.action_up()
        if action == 'down':
            state = self.action_down()
        if action == 'tunnel':
            state = self.action_tunnel()
        if action == 'take':
            state = state
            if (state in env.tools and (not(self.tool))):
                reward = 500
                self.tool=True
        if(self.tool and state.number in self.stations):
            reward = 250
            step = True

        return state, reward, step

    def improve_policy(self,episode:int, gamma:int, alpha:int):
        tool_q_table = np.zeros((32, 7))
        cook_q_table = np.zeros((32, 7))

        for i in range(episode):

            epsilon = 1 / (i + 1)

            # I reset the state of the agent and the beater every episode
            self.state = env.build_state(random.randint(1, 32))
            self.tool = False
            state = self.state
            step = False

            while not step:
                # Choose an action according to the epsilon-greedy policy
                if np.random.uniform(0, 1) < epsilon:
                    action = np.random.choice(self.actions)
                else:
                    # Check if the beater is found and update the Q-table accordingly
                    if not self.tool:
                        action = self.actions[np.argmax(tool_q_table[state.number - 1])]
                    else:
                        action = self.actions[np.argmax(cook_q_table[state.number - 1])]

                # Update the state and the reward according to the action always checking if the beater is found
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

        # Compute the optimal policy
        # The first one is for the agent before the beater is found
        # I used the np.argmax function to find the action with the highest value in the q-table
        tool_policy = np.argmax(tool_q_table, axis=1)
        tool_policy = [env.actions[i] for i in tool_policy]

        # The second one is for the agent after the beater is found
        cook_policy = np.argmax(cook_q_table, axis=1)
        cook_policy = [env.actions[i] for i in cook_policy]

        return tool_policy,cook_policy