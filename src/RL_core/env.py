# environment

import numpy
import random
import DTNHost
from rlglue.environment.Environment import Environment
from rlglue.types import Action
from rlglue.types import Observation
from rlglue.types import Reward_observation_terminal
from rlglue.utils import TaskSpecVRLGLUE3


class env_rf(Environment):
    num_States = 3
    
    

    def __init__(self, host):
        self.Host = host    
        self.startRow, self.startCol = 0, 0
        
    
    def env_init(self):
        PRED_States = attr_rf[num_States]
        self.theWorld = WD_rf(PRED_States, self.Host)
        # taskspec parts need to be fixed
        theTaskSpecObject = TaskSpecVRLGLUE3()
        theTaskSpecObject.setEpisodic()
        theTaskSpecObject.setDiscountFactor(0.8)
        theTaskSpecObject.addDiscreteObservation(IntRange(0, self.theWorld.getNumStates()-1))

        taskSpecString = theTaskSpecObject.toTaskSpec()
        return taskSpecString

    def evn_start(self):
        theObservation = Observation(1, 0, 0)
        theObservation.setInt(0, theWorld.getState())
        if(Host.getAddress() == 11):
            _rf = 0
            if(theWorld.State == 0):
                _rf = 0.1
            elif(theWorld.State == 1):
                _rf = 0.2
            elif(theWorld.State == 2):
                _rf = 0.3
            print("State: "+ theWorld.State + "\trf: "+ _rf)
        return theObservation

    def Reward_observation_terminal(self, thisAction):
        self.theWorld.updatePosition(thisAction.getInt(0))

        theObservation = Observation(1, 0, 0)
        theObservation.setInt(0, self.theWorld.getState())
        RewardObs = Reward_observation_terminal()
        RewardObs.setObservation(theObservation)
        RewardObs.setTerminal(self.theWorld.isTerminal())
        RewardObs.setReward(self.theWorld.getReward())

        return RewardObs
        
    def env_message(self, message):
        return "SampleMinesEnvironment does not understand your message"
    #----------------------------------------
"""
    def states(self):

    def actions(self):

    def close(self):
        super().close()

    def reset(self):
        state = np.random(size=(3,))
        return state
    def execute(self, actions):
        next_state = 
        terminal = 
        reward = 
        return next_state, terminal, reward"""

    #------------------------------------------

class attr_rf:
    def __init__(self):
        self.efficiency = 0

    def attr_rf(self, A):
        self.radius_factor = A

    def set_efficiency(self, effic):
        self.efficiency = effic

class WD_rf:
    def __init__(self):
        self.rf_upper_boundary = 0.4
        self.rf_low_boundary = 0.025

        self.State = 0
        self.efficiency = 0
        self.Prev_State = 0
        self.action = 0

    def WD_rf(self, worldMap, host):
        self.Host = host
        self.theMap = worldMap
        self.numStates = theMap.length

        self.rf = host.radius_factor

        if(self.rf == 0.1):
            self.State = 0
        elif(self.rf == 0.2):
            self.State = 1
        elif(self.rf == 0.3):
            self.State = 2
        
        theMap[0] = attr_rf(0.05)
        theMap[1] = attr_rf(0.1)
        theMap[2] = attr_rf(0.2)

    def getNumStates(self):
        return self.numStates

    def getState(self):
        return self.State

    def get_rf(self):
        return theMap[self.State].radius_factor

    def isValid(self, state):
        valid = False
        if(state >= 0 and state < 3):
            valid = True
        return valid

    def isTerminal(self):
        return False

    def set_efficiency(self, effic):
        theMap[self.State].set_efficiency(effic)
        self.efficiency = effic

    def getReward(self):
        max = [theMap[self.Prev_State].efficiency, theMap[self.State].efficiency][theMap[self.State].efficiency >= theMap[self.Prev_State].efficiency]
        Reward = [(theMap[self.Prev_State].efficiency - theMap[self.State].efficiency)/max, 0.0][max==0]

        if(Host.getAddress() == 11):
            print("rf: cur - " + self.Prev_State + "\tnext - "+ self.State + "\taction: "+ self.action + "\treward: " + Reward)

        return theMap[self.Prev_State].efficiency

    def updatePosition(self, theAction):
        new_state = self.State
        Prev_State = self.State

        if(theAction == 0):
            new_state = self.State
        elif(theAction == 1):
            new_state = self.State + 1
        elif(theAction == 2):
            new_state = self.State - 1

        self.action = theAction

        while(isValid(new_state) == False):
            nextAction = random.randint(0, 3)
            while(nextAction == theAction):
                nextAction = random.randint(0, 3)
            
            if(nextAction == 0):
                new_state = new_state
            elif(nextAction == 1):
                new_state = self.State + 1
            elif(nextAction == 2):
                new_state = self.State - 1

            self.action = nextAction
        
        self.State = new_state
    
    def print_state(self):
        print("Agent with " + self.rf)