import random
import DTNHost
import array as arr
from rlglue.types import Action
from rlglue.types import Observation
from rlglue.utils import TaskSpecVRLGLUE3
from rlglue.agent.Agent import Agent

class agent_rf(Agent):
    sarsa_stepsize = 0.7
    sarsa_epsilon = 1.0
    sarsa_gamma = 1.0

    def __init__(self, host):
        self.Host = host
        self.numActions = 0
        self.numStates = 0
        self.policyFrozen = False
        self.exploringFrozen = False
      

    def agent_init(self, taskSpecification):
        #rlglue taskspec function ->need to be fixed
        theTaskSpec = TaskSpecVRLGLUE3(taskSpecification)
        numStates = theTaskSpec.getDiscreteObservationRange(0).getMax() + 1
        numActions = theTaskSpec.getDiscreteActionRange(0).getMax() + 1
        sarsa_gamma = theTaskSpec.getDiscountFactor()
        valueFunction = [numActions][numStates]

        self.valueFunction = [numActions][numStates]

    
    def agent_start(self, observation):
        newActionInt = egreedy(observation.getInt(0))

        returnAction = Action(1, 0, 0)
        returnAction.intArray[0] = newActionInt
        
        self.lastAction = returnAction.duplicate()
        self.lastObservation = observation.duplicate()

        return returnAction

    def agent_step(self, reward, observation):
        newStateInt = observation.getInt(0)
        lastStateInt = self.lastObservation.getInt(0)
        lastActionInt = self.lastAction.getInt(0)

        newActionInt = egreedy(newStateInt)

        Q_sa = valueFunction[lastActionInt][lastStateInt]
        Q_sprime_aprime = valueFunction[newActionInt][newStateInt]

        new_Q_sa = Q_sa + sarsa_stepsize * (reward + sarsa_gamma *Q_sprime_aprime - Q_sa)
        
        returnAction = Action()
        returnAction.intArray = arr.array(newActionInt)

        self.lastAction = returnAction.duplicate()
        self.lastObservation = observation.duplicate()

        return returnAction

    def agent_end(self, reward):
        lastStateInt = self.lastObservation.getInt(0)
        lastActionInt = self.lastAction.getInt(0)

        Q_sa = self.valueFunction[lastActionInt][lastStateInt]
        new_Q_sa = Q_sa + sarsa_stepsize * (reward - Q_sa)

        if(not self.policyFrozen):
            self.valueFunction[lastActionInt][lastStateInt] = new_Q_sa
        self.lastAction = None
        self.lastObservation = None

    def agent_cleanup(self):
        self.lastAction = None
        self.lastObservation = None
        self.valueFunction = None

    def agent_message(self, message):
        if(message.equals("freeze learning")):
            self.policyFrozen = True
            return "message understood, policy frozen"
        elif(message.equals("unfreeze learning")):
            self.policyFrozen = False
            return "message understood, policy unfrozen"
        elif(message.equals("freeze exploring")):
            self.exploringFrozen = False
            return "message understood, exploration frozen"
        elif(message.equals("unfreeze exploring")):
            self.exploringFrozen = True
            return "message understood, exploration unfrozen"
        return "SampleSarsaAgent does not understand your message"

    
    def egreedy(self, theState):
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
        return maxIndex
