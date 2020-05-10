import numpy as np
from tensorforce.agents import Agent


class agent_rl(Agent):
    sarsa_stepsize = 0.7
    sarsa_epsilon = 1.0
    sarsa_gamma = 1.0
    numActions = 3
    numStates = 3

    def __init__(self):
        self.lastAction = None
        self.lastObservation = None
        self.valueFunction = [[0 for x in range(numActions)] for y in range(numStates)]
        
        #self.policyFrozen = False
        #self.exploringFrozen = False

    def rl_act(self, observation):
        newActionInt = egreedy(observation.getInt(0))

        returnAction = [newActionInt]

        self.lastAction = returnAction
        self.lastObservation = observation

        return returnAction

    def rl_step(self, reward, observation):
        newStateInt = observation[0]
        lastStateInt = self.lastObservation[0]
        lastActionInt = self.lastAction[0]

        newActionInt = egreedy(newStateInt)

        Q_sa = valueFunction[lastActionInt][lastStateInt]
        Q_sprime_aprime = valueFunction[newActionInt][newStateInt]

        new_Q_sa = Q_sa + sarsa_stepsize * (reward + sarsa_gamma * Q_sprime_aprime - Q_sa)

        returnAction = [newActionInt]
        self.lastAction = returnAction
        self.lastObservation = observation

        return returnAction

    def rl_end(self, reward):
        lastStateInt = self.lastObservation[0]
        lastActionInt = self.lastAction[0]

        Q_sa = self.valueFunction[lastActionInt][lastStateInt]
        new_Q_sa = Q_sa + sarsa_stepsize * (reward - Q_sa)

        self.valueFunction[lastActionInt][lastStateInt] = new_Q_sa
        self.lastAction = None
        self.lastObservation = None

    def agent_cleanup(self):
        self.lastAction = None
        self.lastObservation = None
        self.valueFunction = None

    """def egreedy(self, theState):
        if (not exploringFrozen):
            if (random.uniform(0,1) <= sarsa_epsilon):
                if(Host.getAddress() == 11):
                    print("\tagent_rf - current state: "+ theState)
                    print("\t\tvalueFunction: ")
                    for i in range(numActions):
                        print(self.valueFunction[i][theState] + "\t")
                    print("\n")

                return random.randint(0, numActions)
        
        maxIndex = 0
        for i in range(numActions):
            if(valueFunction[i][theState] >= valueFunction[maxIndex][theState]):
                maxIndex = i

        if(Host.getAddress() == 11):
            print("\tagent_rf - current state: "+theState)
            print("\t\tvalueFunction: ")
            for j in range(numActions):
                print(self.valueFunction[j][theState] + "\t")
            print("\n")
        return maxIndex """

    def egreedy(self, theState):
        maxIndex = 0
        for i in range(numActions):
            if(valueFunction[i][theState] >= valueFunction[maxIndex][theState]):
                maxIndex = i

        print("\tagent_rl -> current state: "+theState)
        print("\t\tvalueFunction: ")
        for j in range(numActions):
            print(valueFunction[j][theState] + "\t")
        print("\n")
        return maxIndex



