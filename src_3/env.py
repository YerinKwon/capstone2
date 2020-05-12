# env calculate reward and return it. (+next state)
from src_3.agent import agent
from numpy import random
class env:
    def __init__(self, isG, isS):
        self.numState = 3
        self.observation = Observation(0,0,0,0)
        self.lastState = 0
        self.state = 0
        self.reward = 0
        self.efficiency = 0
        self.INTERVAL_GAMMA = 120
        self.INTERVAL_SIGMA = 0.1
        self.isGAMMA = isG
        self.isSIGMA = isS

    def env_start(self, state):
        
        self.observation.setState(state)
        if(self.isGAMMA):
            self.observation.setParam(1020)
        elif(self.isSIGMA):
            self.observation.setParam(0.1)
        print("env_start with state", state)

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
            self.observation.setAction(nextAction)

        if nextState == 0:
            if(self.isGAMMA):
                self.observation.setParam(1020)
            elif(self.isSIGMA):
                self.observation.setParam(0.1)
        elif nextState == 1:
            if(self.isGAMMA):
                self.observation.setParam(1200)
            elif(self.isSIGMA):
                self.observation.setParam(0.2)
        elif nextState == 2:
            if(self.isGAMMA):
                self.observation.setParam(1380)
            elif(self.isSIGMA):
                self.observation.setParam(0.3)
        reward = self.getReward()

        self.observation.setState(nextState)
        self.observation.setReward(reward)
        print("-----env_step-----")
        print("next action:", action)
        print("next state:", nextState, "reward:", reward)
        print("GAMMA:",self.isGAMMA, "SIGMA:",self.isSIGMA, self.observation.getParam(),"\n")

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
        

        return self.efficiency

    def env_message(self, msg):
        lst = msg.split(' ')
        if (lst[0] == 'efficiency'):
            self.efficiency = float(lst[1])


class Observation:
    def __init__(self, state=None, reward=None, action=None, param=None):
        self.state = state
        self.reward = reward
        self.action = action
        self.param = param

    def setState(self, state):
        self.state = state

    def setReward(self, reward):
        self.reward = reward

    def setAction(self, action):
        self.action = action

    def setParam(self, param):
        self.param = param

    def getState(self):
        return self.state

    def getReward(self):
        return self.reward

    def getAction(self):
        return self.action

    def getParam(self):
        return self.param