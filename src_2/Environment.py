from tensorforce.environments import Environment
import numpy as np

class Env(Environment):

    def __init__(self):
        super().__init__()

    def states(self):
        
        return dict(type = 'float', shape= (8,))

    def actions(self):

        return dict(type = 'int', num_values = 3)

    def max_episode_timesteps(self):
        return super().max_episode_timesteps()

    def close(self):
        super().close()

    def reset(self):
        state = np.random.random(size=(8,))

        return state

    def execute(self, actions):
        next_state = np.random.random(size = (8,))
        terminal = np.random.random() < 0.5
        reward = np.random.random()

        return next_state, terminal, reward