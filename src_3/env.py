# env calculate reward and return it. (+next state)

class env:
    def __init__(self):
        self.numState = 3

    def env_step(self, action):
        return getReward()

    def getReward(self):
        # r = e = contact predictability / Energy
        # contact 
        #   1) detected when the DC = DCdef
        #   2) detected during DC growth for estimated contactable time
        #   3) detected during DC growth for serendipitous contacts
        #   4) detected when the DC keeps low

        #   CP for sigma = n(2)/n(all detected contacts)
        #   CP for gamma = n(3)/n(all detected contacts)
        reward = 
