import csv
import queue
import neighborDiscovery
import math


'''
file format:
sec(int),ID,x_coordinate(m),y_coordinate(m),AP_ID\n
(csv)

example:
sec | ID | x_coordinate | y_coordinate | AP_ID
27727,10,21728,32711,141

'''

class Simulator:
    def __init__(self):
        self.STORAGE_MAX = 40

        self.ENERGY_CONSUMPTION = 0
        self.nd = neighborDiscovery.neighborDiscovery()

        #------will be learned by RL-------
        self.SIGMA = 5000
        self.GAMMA = 3


    def simulate(self, filename):
        '''
            input: filepath+name as string
        '''
        f = open(filename,'r')
        f.readline()
        cur_t = 0
        cur_row = list(map(int, f.readline()[:-1].split(',')))
        storage = queue.Queue(maxsize=self.STORAGE_MAX)

        while cur_row != "":
            print(cur_t)
            #contact prediction
            predicted = self.nd.ContactPrediction(storage, self.SIGMA)
            
            #duty cycle adaptation
            dc = self.nd.DutyCycleAdaptation(predicted, cur_t, self.GAMMA)

            #if there's new log in current time: contact learning
            if(cur_row[0] >= cur_t):
                #read
                sec, ID, x_coord, y_coord, AP_ID = list(map(int, f.readline()[:-1].split(',')))
                storage.put(sec)    #insert to the storage: sec

            cur_t += 1
            self.ENERGY_CONSUMPTION += dc
        f.close()
        print("Total energy consumption: "+str(self.ENERGY_CONSUMPTION))