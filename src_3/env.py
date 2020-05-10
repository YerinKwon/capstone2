# env calculate reward and return it. (+next state)
from agent import agent
from numpy import random
class env:
    def __init__(self):
        self.numState = 3
        self.observation = Observation(0,0)
        self.lastState = 0
        self.state = 0
        self.reward = 0

    def env_start(self, action):
        _rf = 0.2
        print("env_start", action)

        return self.observation

    def env_step(self, action):
        self.state = self.observation.getState()
        if action == 0:
            nextState = self.state
        elif action == 1:
            nextState = self.state + 1
        elif action == 2:
            nextState = self.state - 1
        while(nextState == -1 or nextState == 3):
            nextAction = random.randint(0,2)
            while(nextAction == action):
                nextAction = random.randint(3)
            if nextAction == 0:
                nextState = self.state
            elif nextAction == 1:
                nextState = self.state + 1
            elif nextAction == 2:
                nextState = self.state - 1
            action = nextAction
        reward = self.getReward()

        self.observation.setState(nextState)
        self.observation.setReward(reward)
        print("-----env_step-----")
        print("next action:", action)
        print("next state:", nextState, "reward:", reward)

        return self.observation

    

    def getReward(self):
        # r = e = contact predictability / Energy
        # contact 
        #   1) detected when the DC = DCdef
        #   2) detected during DC growth for estimated contactable time
        #   3) detected during DC growth for serendipitous contacts
        #   4) detected when the DC keeps low

        #   CP for sigma = n(2)/n(all detected contacts)
        #   CP for gamma = n(3)/n(all detected contacts)
        reward = random.randint(100)

        return reward

class Observation:
    def __init__(self, state=None, reward=None):
        self.state = state
        self.reward = reward

    def setState(self, state):
        self.state = state

    def setReward(self, reward):
        self.reward = reward

    def getState(self):
        return self.state

    def getReward(self):
        return self.reward