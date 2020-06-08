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
        self.epsilon = 1
        self.gamma = 1

        self.Qval = [[0 for x in range(self.numActions)] for y in range(self.numStates)]
        
        self.lastAction = None
        self.lastState = None

    def egreedy(self, theState):
        if np.random.randint(0,2) == self.epsilon:
            return np.random.randint(0,3)
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
        Q_spap = self.Qval[newAction][newState]

        new_Q_sa = Q_sa + self.stepsize * (reward + self.gamma* Q_spap - Q_sa)
        if((state == 0 and newAction == 2) or (state==2 and newAction==1)):
            #self.Qval[newAction][newState] = 0.0
            self.Qval[newAction][newState]
        else:
            #self.Qval[newAction][newState] = Q_sa + self.stepsize * reward
            self.Qval[self.lastAction][self.lastState] = new_Q_sa
        

        print("-----agent step-----")
        #print("last action:", self.lastAction, "current action:", newAction)
        print("current state:", state, "chosen action:", newAction)
        print("Q-value:", self.Qval)

        self.lastAction = newAction
        self.lastState = newState
        

        return newAction

    def agent_message(self, msg):
        lst = msg.split(' ')
        if (lst[0] == 'action'):
            action = int(lst[1])
            self.lastAction = action
            print ("random action passed")

    

