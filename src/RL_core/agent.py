import random
import DTNHost

from rlglue.types import Action
from rlglue.types import Observation
from rlglue.utils import TaskSpecVRLGLUE3
from rlglue.agent.Agent import Agent

class agent:
    def __init__(self):
        self.sarsa_stepsize = 0.7
        self.sarsa_epsilon = 1.0
        self.sarsa_gamma = 1.0

        

        self.valueFunction = [numActions][numStates]

    def agent_init(self, taskSpecification):
        #rlglue taskspec function ->need to be fixed
        theTaskSpec = TaskSpecVRLGLUE3(taskSpecification)
        numStates = theTaskSpec.getDiscreteObservationRange(0).getMax() + 1
        numActions = theTaskSpec.getDiscreteActionRange(0).getMax() + 1
        sarsa_gamma = theTaskSpec.getDiscountFactor()
        valueFunction = [numActions][numStates]

    def agent_rf(self, host):
        self.Host = host
    
    def agent_start(self, observation):
        newActionInt = egreedy(observation.getInt(0))

        returnAction = Action(1, 0, 0)
        returnAction.intArray[0] = newActionInt
        
        lastAction = returnAction.duplicate()
        lastObservation = observation.duplicate()

        return returnAction

    def agent_step(self, reward, observation):
        newStateInt = observation.getInt(0)
        lastStateInt = lastObservation.getInt(0)
        lastActionInt = lastAction.getInt(0)

        newActionInt = egreedy(newStateInt)

        Q_sa = valueFunction[lastActionInt][lastStateInt]
        Q_sprime_aprime = valueFunction[newActionInt][newStateInt]

        new_Q_sa = Q_sa + sarsa_stepsize * (reward + sarsa_gamma *Q_sprime_aprime - Q_sa)

        returnAction = Action()
        #returnAction.intArray = int[]{newActionInt}

        lastAction = returnAction.duplicate()
        lastObservation = observation.duplicate()

        return returnAction


    def egreedy(self, theState):
        if (not exploringFrozen):
            if (random. <= sarsa_epsilon):
                if(Host.getAddress() == 11):
                    for i in range(numActions):
                        print("\n")

                return random.randint(0, numActions)
        
        maxIndex = 0
        for i in range(numActions):
            if(valueFunction[i][theState] >= valueFunction[maxIndex][theState]):
                maxIndex = i

        if(Host.getAddress() == 11):
            print("\n")
        return maxIndex
    