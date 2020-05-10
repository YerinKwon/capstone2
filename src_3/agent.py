import numpy as np

# agent changes Qval and returns action

class agent:
    
    # initialize:   set # of actions and states which is 3 here
    #               learning rate = 0.7
    #               Qval is for Q-value


    def __init__(self):
        self.numActions = 3
        self.numStates = 3
        self.stepsize = 0.7

        self.Qval = [[0 for x in range(self.numActions)] for y in range(self.numStates)]
        
        self.lastAction = None
        self.lastState = None

    def egreedy(self, theState):
        maxIndex = 0
        for i in range(self.numActions):
            if (self.Qval[i][theState] >= self.Qval[maxIndex][theState]):
                maxIndex = i
        return maxIndex
    
    def agent_start(self, state, reward):
        newAction = self.egreedy(state)
        newState = state

        self.lastAction = newAction
        self.lastState = newState
        print("agent start\n")
        return newAction

    def agent_step(self, reward, state):
        newAction = self.egreedy(state)
        newState = state

        Q_sa = self.Qval[self.lastAction][self.lastState]
        self.Qval[newAction][newState] = Q_sa + self.stepsize * reward
        
        print("-----agent step-----")
        print("last state:", self.lastState, "current state:", state)
        print("Q-value:", self.Qval)

        self.lastAction = newAction
        self.lastState = newState
        

        return newAction

    

