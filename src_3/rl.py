# for reinforcement learning
from src_3.agent import agent
from src_3.env import env
from src_3.env import Observation
class rl:
    def __init__(self):
        self.agent = None
        self.env = None
        self.observation = Observation(0,0)

    def rl_init(self, agent, env):
        self.agent = agent
        self.env = env

    def rl_start(self):
        action = 0
        self.observation = self.env.env_start(action)
        state = self.observation.getState()
        reward = self.observation.getReward()
        self.agent.agent_start(reward, state)

    def rl_step(self):
        state = self.observation.getState()
        reward = self.observation.getReward()
        action = self.agent.agent_step(reward, state)
        self.observation = self.env.env_step(action)

    def rl_agent_msg(self, msg):
        self.agent.agent_message(msg)

    def rl_env_msg(self, msg):
        self.env.env_message(msg)
