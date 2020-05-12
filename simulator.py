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
        # self._dc = 0
        self.AWAKE_ENERGY = 329.9
        self.SLEEP_ENERGY = 4.02
        self.tSleep = 0
        self.tScanning = 0

        self.first_case = 0
        self.second_case = 0
        self.third_case = 0
        self.fourth_case = 0

        self.init_DC = 8
        self.sleep_DC = 2
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
            #contact prediction
            predicted = self.nd.ContactPrediction(storage, self.SIGMA)
            
            #duty cycle adaptation
            case, dc = self.nd.DutyCycleAdaptation(predicted, cur_t, self.GAMMA)

            #add energy consumption by duty cycle
            self.ENERGY_CONSUMPTION += dc*0.01*self.AWAKE_ENERGY + (100-dc)*0.01*self.SLEEP_ENERGY

            #add to sleep duration | scanning duration
            if(dc == self.sleep_DC):
                self.tSleep += 1
            else:
                self.tScanning += 1

            #if there's new log in current time: contact learning
            if(sec == cur_t):
                #read
                if storage.qsize() == self.STORAGE_MAX:
                    storage.get()
                storage.put(sec)    #insert to the storage: sec

                print("detected: "+str(cur_t))
                print("case: "+str(case))
                #add to detected contacts case
                if (case == 1):    #detected when DC_DEF
                    self.first_case += 1
                elif (case == 2):   #detected during growth
                    self.second_case += 1
                elif (case == 3): #detected when seren
                    self.third_case += 1
                elif (case == 4): #detected when sleep
                    self.fourth_case += 1

                cur_row = f.readline()
                if cur_row:
                    sec, ID, x_coord, y_coord, AP_ID = list(map(int, cur_row[:-1].split(',')))

            if cur_t == 86400:
                #run rl once a day
                detected_contacts = self.first_case + self.second_case + self.third_case + self.fourth_case 
                self.accuracy_sigma = self.second_case/detected_contacts
                self.accuracy_gamma = self.third_case/detected_contacts

                #rewards
                effic_s = self.accuracy_sigma/self.ENERGY_CONSUMPTION
                effic_g = self.accuracy_gamma/self.ENERGY_CONSUMPTION

                msg = "efficiency " + str(effic_s)
                
                self.rl.rl_env_msg(msg)
                self.rl.rl_step()

                #----------업뎃된 시그마, 감마값은 어떻게 반영됨?? -----------
                #----------아직 안짬^^!----------

                print("one day passed!")
                print("Energy consumption on day "+str(self.DAY)+": "+str(self.ENERGY_CONSUMPTION))

                #------init------
                self.first_case = 0
                self.second_case = 0
                self.third_case = 0
                self.fourth_case = 0
                self.tScanning = 0
                self.tSleep = 0
                cur_t = 1
                self.DAY += 1
                
                self.ENERGY_CONSUMPTION = 0
                # self._dc = 0
                
            else:
                cur_t += 1
                #self._dc += dc

        f.close()
        end_time = time.time() - start_time
        #print("Total energy consumption: "+str(self.ENERGY_CONSUMPTION))
        print("Total work done in"+end_time+"seconds")  #타임은 왜잰거??
                                                        #한번돌릴때 얼마나 걸리나 알아둬야 실험할때 편할것같아서,,,