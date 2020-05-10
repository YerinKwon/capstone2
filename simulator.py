#-*- coding:utf-8 -*-

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
....

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
        cur_row = f.readline()
        sec, ID, x_coord, y_coord, AP_ID = list(map(int, cur_row[:-1].split(',')))
        storage = queue.Queue(maxsize=self.STORAGE_MAX)

        while cur_row != "":
            if cur_t%10000 == 0:
                print("current time: "+str(cur_t))
            #contact prediction
            predicted = self.nd.ContactPrediction(storage, self.SIGMA)
            
            #duty cycle adaptation
            dc = self.nd.DutyCycleAdaptation(predicted, cur_t, self.GAMMA)

            #if there's new log in current time: contact learning
            if(sec == cur_t):
                print("current time: "+str(cur_t))
                print("Duty Cycle: "+str(dc))
                print("storage size: "+str(storage.qsize()))
                #read
                if storage.qsize == self.STORAGE_MAX:
                    storage.get()
                storage.put(sec)    #insert to the storage: sec
                cur_row = f.readline()
                if cur_row:
                    sec, ID, x_coord, y_coord, AP_ID = list(map(int, cur_row[:-1].split(',')))

            if cur_t == 86400:
                cur_t = 1
            else:
                cur_t += 1
            self.ENERGY_CONSUMPTION += dc
        f.close()
        print("Total energy consumption: "+str(self.ENERGY_CONSUMPTION))