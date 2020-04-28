import math
import array as arr
from capstone2.src.Coord import Coord

class DTNHost:
    def __init__(self, msgLs, movLs, groupId, interf, comBus, mmProto, mRouteProto, disLs):
        self.nextAddress = 0
        self.lmd = 0.0
        self.host_count = 0
        self.Distance_U = 0.0
        self.dx, self.dy = 0.0, 0.0
        self.Dest_x, self.Dest_y = 750, 750
        self.isMoving = False

        #parameters for neighbor discovery with human mobility prediction
        self.previous_contact_time = 0.0
        self.Adaptive_Duty_Cycle = 0.0
        self.total_node_num = 40
        self.moving_node = 20
        self.prev_contact_time_for_report = 0.0
        self.prev_contact_interval = 0.0
        self.last_contact_time = 0.0

        self.condition_1 = False
        self.condition_2 = False
        self.slot_num = -1
        self.SleepOrWake = False
        self.Prev_prediction_time = 0.0
        self.new_contact = False

        #for the report
        self.sensing_no = 0
        self._prediction_flag = False
        self._correct_prediction = False
        self.prediction_no = 0
        self.correct_prediction_no = 0
        self.none_prediction_init_no = 0
        self.none_prediction_pred_no = 0
        self.prediction_contact_no = 0
        self.report_slot_no = 0
        self.days = 1
        self.contact_prediction_flag = False
        self.history_size = 150

        self.accuracy = 0.0
        self.Energy_RD = 0.0
        self.efficiency = 0.0
        self.efficiency_ei = 0.0
        self.efficiency_rf = 0.0

        self.discovery_latency = double[total_node_num]
        self.connection_flag = int[total_node_num]

        self.last_init_contact_time = 0
        self.last_low_contact_time = 0
        #--------------------------------------
    
        self.comBus = comBus
        self.location = Coord(0,0)
        self.address = getNextAddress()
        self.name = groupId + self.address
        self.net = []
        
        for i in interf:
            ni = i.replicate()
            ni.setHost(self)
            net.append(ni)

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

        if (movLs != None):
            for l in movLs:
                l.initialLocation(self, self.location)

        self.Distance_U = math.sqrt(math.pow(self.location.getX() - self.Dest_x, 2) + math.pow(self.location.getY() - self.Dest_y, 2))

        for node in range(total_node_num):
            self.connection_flag[node] = 0
            self.discovery_latency[node] = -1
            self.History_i_time[node] = []
            self.temp_contact_var2[node] = []


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
        router.init(self, self.msgListerners, self.disListerners)
        self.router = router

    def getRouter(self):
        return self.router

    def getAddress(self):
        return self.address

    def getCombus(self):
        return self.comBus

    #def connectionUp(self, con):
    #    self.router.changedConnection(con)

    #def connectionDown(self, con):
    #    self.router.changedConnection(con)

    def getLocation(self):
        return self.location
    
    def getPath(self):
        return self.path

    def setLocation(self, location):
        self.location = location.clone()

    def setName(self, name):
        self.name = name

    #router, net, move
    def getMessageCollection(self):
        return self.router.getMessageCollection()

    def getNrofMessages(self):
        return self.router.getNrofMessages()

    def getBufferOccupancy(self):
        bSize = router.getBufferSize()
        freeBuffer = router.getFreeBufferSize()
        return 100*((bSize-freeBuffer)/bSize)

    def getRoutingInfo(self):
        return self.router.getRoutingInfo

    def getInterfaces(self):
        return self.net

    def getInterface(self, interfaceNo):
        ni = None

        ni = self.net.get(interfaceNo-1)
        return ni

    def forceConnection(self, anotherHost, interfaceId, up):
        if(interfaceId != None):
            ni = getInterface(interfaceId)
            no = anotherHost.getInterface(interfaceId)
        else:
            ni = getInterface(1)
            no = anotherHost.getInterface(1)

        if(up):
            ni.createConnection(no)
        else:
            ni.destroyConnection(no)

    def connect(self, h):
        forceConnection(h, None, True)

    def update(self, simulateConnections):
        if (not isRadioActive()):
            tearDownAllConnections()
            return
        if(simulateConnection):
            for i in net:
                i.update()
        self.router.update()

    def tearDownAllConnections(self):
        for i in net:
            conns = i.getConnections()
            if(conns.size() == 0):
                continue

            removeList = arr.array(conns.size())
            for con in conns:
                removeList.add(con.getOtherInterface(i))
            for inf in removeList:
                i.destroyConnection(inf)
    
    def move(self, timeIncrement):
        if(not isMovementActive() or SimClock.getTime() < self.nextTimeToMove):
            self.isMoving = False
            return
        if(self.destination == None):
            if(not setNextWaypoint()):
                return

        self.isMoving = True

        possibleMovement = timeIncrement * speed
        distance = self.location.distance(self.destination)

        while(possibleMovement >= distance):
            self.location.setLocation(self.destination)
            self.prev_destination = self.prev_destination

            possibleMovement -= distance
            if(not setNextWayPoint()):
                return

            distance = self.location.distance(self.destination)

            self.cur_destination = self.destination

            if(self.cur_destination != self.prev_destination):
                temp_lambda = self.cur_destination.distance(self.prev_destination)/self.speed
                self.host_count += 1
                self.lmd = (self.lmd*host_count + temp_lambda)/(self.host_count + 1)
        dx = (possibleMovement/distance) * (self.destination.getX() - self.location.getX())
        dy = (possibleMovement/distance) * (self.destination.getY() - self.location.getY())

        self.dx = dx
        self.dy = dy
        estimator(self.dx, self.dy, self.lmd, timeIncrement)
        self.location.translate(dx, dy)

    def estimator(self, dx, dy, lmd, timeIncrement):
        self.Distance_U = math.sqrt(math.pow((dx*self.lmd*timeIncrement)+self.location.getX()-Dest_x, 2) + math.pow((dy*self.lmd*timeIncrement)+self.location.getY()-Dest_y, 2))

    def setNextWaypoint(self):
        if(path == None):
            path = movement.getPath()

        if(path == None or (not path.hasNext())):
            self.nextTimeToMove = movement.nextPathAvailable()
            self.path = None
            return False

        self.destination = path.getNextWayPoint()
        self.speed = path.getSpeed()

        if(self.movListeners != None):
            for l in self.movListeners:
                l.newDestination(self, self.destination, self.speed)
        return True

    def sendMessage(self, id, to):
        self.router.sendMessage(id, to)

    def receiveMessage(self, m, frm):
        retVal = self.router.receiveMessage(m, frm)
        if(retVal == MessageRouter.RCV_OK):
            m.addNodeOnPath(self)

        return retVal

    def requestDeliverableMessages(self, con):
        return self.router.requestDeliverableMessages(con)

    def messageTransferred(self, id, frm):
        self.router.messageTransferred(id, rfm)

    def messageAborted(self, id, frm, bytesRemaining):
        self.router.messageAborted(id, frm, bytesRemaining)
    
    def createNewMessage(self, m):
        self.router.createNewMessage(m)

    def deleteMessage(self, id, drop):
        self.router.deleteMessage(id, drop)

    def toString(self):
        return self.name

    def equals(self, otherHost):
        return self == otherHost

    def compareTo(self, h):
        return self.getAddress() - h.getAddress()
            


