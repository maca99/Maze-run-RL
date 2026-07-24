import numpy as np
import random
from env import state, env


class Agent:

    ACTIONS = ['up', 'down', 'left', 'right', 'tunnel', 'take']
    ACTION_INDEX = {a: i for i, a in enumerate(ACTIONS)}

    REWARD_STEP = -1
    REWARD_INVALID_MOVE = -15
    REWARD_TUNNEL_BLOCKED = -20
    REWARD_TAKE_TOOL = 200
    REWARD_REACH_STATION = 5000

    def __init__(self):
        self.state = env.build_state(9)
        self.tool = False

    # --- Metodi pubblici di movimento: se env restituisce None, resto fermo ---
    def action_right(self):
        new_state = env.ask_state(self.state, 'right')
        return new_state if new_state is not None else self.state

    def action_left(self):
        new_state = env.ask_state(self.state, 'left')
        return new_state if new_state is not None else self.state

    def action_up(self):
        new_state = env.ask_state(self.state, 'up')
        return new_state if new_state is not None else self.state

    def action_down(self):
        new_state = env.ask_state(self.state, 'down')
        return new_state if new_state is not None else self.state

    def action_tunnel(self):
        new_state = env.ask_state(self.state, 'tunnel')
        return new_state if new_state is not None else self.state

    def move(self, direction: str):
        new_state = env.ask_state(self.state, direction)
        return new_state if new_state is not None else self.state

    # --- Logica di step usata dal training ---
    def make_step(self, state: state, has_tool: bool, action: str):
        reward = self.REWARD_STEP
        done = False
        new_state = state

        if action in ('left', 'right', 'up', 'down'):
            candidate = env.ask_state(state, action)
            if candidate is None:
                reward = self.REWARD_INVALID_MOVE
                # new_state resta = state (nessun cambiamento)
            else:
                new_state = candidate

        elif action == 'tunnel':
            candidate = env.ask_state(state, 'tunnel')
            if candidate is None or candidate.number == state.number:
                reward = self.REWARD_TUNNEL_BLOCKED
                # new_state resta = state
            else:
                new_state = candidate

        elif action == 'take':
            if state.number in env.tools and not has_tool:
                has_tool = True
                reward = self.REWARD_TAKE_TOOL

        if has_tool and new_state.number in env.stations:
            reward = self.REWARD_REACH_STATION
            done = True

        return new_state, has_tool, reward, done

    def _choose_action(self, q_table, state_number, epsilon):
        if np.random.uniform(0, 1) < epsilon:
            return np.random.choice(self.ACTIONS)
        return self.ACTIONS[np.argmax(q_table[state_number])]

    def improve_policy(self, episodes: int, gamma: float, alpha: float):
        n_states = 32
        tool_q_table = np.zeros((n_states, len(self.ACTIONS)))
        cook_q_table = np.zeros((n_states, len(self.ACTIONS)))

        for i in range(episodes):
            epsilon = 1 / (i + 1)
            state = env.build_state(random.randint(0, n_states - 1))
            has_tool = False
            done = False

            while not done:
                q_table = cook_q_table if has_tool else tool_q_table
                action = self._choose_action(q_table, state.number, epsilon)

                next_state, has_tool, reward, done = self.make_step(state, has_tool, action)

                a_idx = self.ACTION_INDEX[action]
                q_table[state.number][a_idx] += alpha * (
                    reward + gamma * np.max(q_table[next_state.number]) - q_table[state.number][a_idx]
                )

                state = next_state

            print(f"episodio {i} completato")

        self.state = state
        self.tool = has_tool

        tool_policy = [self.ACTIONS[i] for i in np.argmax(tool_q_table, axis=1)]
        cook_policy = [self.ACTIONS[i] for i in np.argmax(cook_q_table, axis=1)]

        return {"tool": tool_policy, "cook": cook_policy}