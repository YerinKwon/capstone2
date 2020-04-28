

class DTNHost:
    def __init__(self, msgLs, movLs, groupId, interf, comBus, mmProto, mRouteProto, disLs):
        self.nextAddress = 0
        self.lmd = 0.0
        self.host_count = 0
        self.prev_destination
        self.Distance_U = 0.0
        self.dx, self.dy = 0.0, 0.0
        self.Dest_x, self.Dest_y = 750, 750
        self.isMoving = False

    
        self.comBus = comBus
        self.location = Coord(0,0)
        self.address = getNextAddress()
        self.name = groupId + self.address
        
        for i in interf:
            ni = i.replicate()
            ni.setHost(self)
            net.add(ni)

        self.msgListeners = msgLs
        self.movListeners = movLs
        self.disListeners = disLs
        
        self.movement = mmProto.replicate()
        self.movement.setComBus(comBus)
        self.movement.setHost(self)
        setRouter(mRouteProto.replicate())

        self.location = movement.getInitialLocation()
        self.nextTimeToMove = movement.nextPathAvailable()
        self.path = None




    def getNextAddress(self):
        self.nextAddress += 1
        return self.nextAddress

    def reset(self):
        self.nextAddress = 0

    def isMovementActive(self):
        return self.movement.isActive()

    def isRadioActive(self):
        return self.getInterface(1).isActive()
    
    def setRouter(self, router):
        router.init(self, msgListerners, disListerners)
        self.router = router

    def getRouter(self):
        return self.router

    def getAddress(self):
        return self.address

    def getCombus(self):
        return self.comBus

    #def connectionUp(self, con):

    #def connectionDown(self, con):

    def getLocation(self):
        return self.location
    
    def getPath(self):
        return self.path

    #def setLocation
    def setName(self, name):
        self.name = name

    #router, net, move


