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

        self.Qval = [[0 for x in range(numActions)] for y in range(numStates)]
        
        self.lastAction = None
        self.lastState = None

    """
    def agent_start(self):
        newActionInt = egreedy()

        returnAction = newActionInt

        return returnAction"""

    def agent_step(self, reward, state):
        newAction = egreedy(state)
        newState = state

        Q_sa = Qval[lastAction][lastState]
        Qval[newAction][newState] = Q_sa + stepsize * reward
        
        return newAction

    def egreedy(self, theState):
        maxIndex = 0
        for i in range(numActions):
            if (Qval[i][theState] >= Qval[maxIndex][theState]):
                maxIndex = i
        return maxIndex

