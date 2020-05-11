#-*- coding:utf-8 -*-

import csv
import queue
import neighborDiscovery
import math
import time

from src_3.agent import agent
from src_3.env import env
from src_3.rl import rl

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

        #------for energy calculation------
        self.ENERGY_CONSUMPTION = 0
        self.accuracy_sigma = 0
        self.accuracy_gamma = 0
        self._dc = 0
        self.AWAKE_ENERGY = 329.9
        self.SLEEP_ENERGY = 4.02

        self.first_case = 0
        self.second_case = 0
        self.third_case = 0
        self.fourth_case = 0

        self.init_DC = 8
        self.sleep_DC = 0
        #------------------------------

        self.DAY = 1
        self.nd = neighborDiscovery.neighborDiscovery()

        self.agent = agent()
        self.env = env()
        self.rl = rl()

        self.rl.rl_init(self.agent, self.env)
        self.rl.rl_start()

        #------will be learned by RL-------
        self.SIGMA = 5000
        self.GAMMA = 3


    def simulate(self, filename):
        '''
            input: filepath+name as string
        '''
        start_time = time.time()
        f = open(filename,'r')
        f.readline()
        cur_t = 0
        cur_row = f.readline()
        sec, ID, x_coord, y_coord, AP_ID = list(map(int, cur_row[:-1].split(',')))
        storage = queue.Queue(maxsize=self.STORAGE_MAX)

        while cur_row != "":
            #if cur_t%10000 == 0:
                #print("current time: "+str(cur_t))
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
                if storage.qsize() == self.STORAGE_MAX:
                    storage.get()
                storage.put(sec)    #insert to the storage: sec

                #add to detected contacts case
                if (dc == self.init_DC):
                    self.first_case += 1
                elif (dc > self.init_DC):
                    self.second_case += 1
                elif (dc > self.sleep_DC and
                    dc < self.init_DC):
                    self.third_case += 1
                elif (dc == self.sleep_DC):
                    self.fourth_case += 1


                cur_row = f.readline()
                if cur_row:
                    sec, ID, x_coord, y_coord, AP_ID = list(map(int, cur_row[:-1].split(',')))

            if cur_t == 86400:
                detected_contacts = self.first_case + self.second_case + self.third_case + self.fourth_case
                self.ENERGY_CONSUMPTION = 1.0 - (self._dc*self.AWAKE_ENERGY + (100.0-self._dc)*self.SLEEP_ENERGY)/\
                    (self.init_DC*self.AWAKE_ENERGY + (100.0-self.init_DC)*self.SLEEP_ENERGY)
                self.accuracy_sigma = self.second_case/detected_contacts
                self.accuracy_gamma = self.third_case/detected_contacts

                effic_s = self.accuracy_sigma/self.ENERGY_CONSUMPTION
                effic_g = self.accuracy_gamma/self.ENERGY_CONSUMPTION

                msg = "efficiency" + str(effic_s)
                self.rl.rl_env_msg(msg)
                self.rl.rl_step()

                #------init------
                self.first_case = 0
                self.second_case = 0
                self.third_case = 0
                self.fourth_case = 0
                cur_t = 1
                self.DAY += 1
                self.ENERGY_CONSUMPTION = 0
                self._dc = 0
                print("one day passed!\n")
                
            else:
                cur_t += 1
                self._dc += dc

        f.close()
        end_time = time.time() - start_time
        #print("Total energy consumption: "+str(self.ENERGY_CONSUMPTION))
        print("Total work done in"+end_time+"seconds")