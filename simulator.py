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
            #contact prediction
            predicted = self.nd.ContactPrediction(storage, self.SIGMA)
            
            #duty cycle adaptation
            dc = self.nd.DutyCycleAdaptation(predicted, cur_t, self.GAMMA)

            #add energy consumption by duty cycle
            self.ENERGY_CONSUMPTION += dc*0.01*self.AWAKE_ENERGY + (100-dc)*0.01*self.SLEEP_ENERGY

            #if there's new log in current time: contact learning
            if(sec == cur_t):
                #read
                if storage.qsize() == self.STORAGE_MAX:
                    storage.get()
                storage.put(sec)    #insert to the storage: sec

                #add to detected contacts case
                #---------여기 수정해야할듯: prediction 안쪽에서 구하는걸로-----------------
                if (dc == self.init_DC):    #detected when DC_DEF
                    self.first_case += 1
                elif (dc > self.init_DC):   #detected during growth
                    self.second_case += 1
                elif (dc > self.sleep_DC and dc < self.init_DC): #detected when seren
                    self.third_case += 1
                elif (dc == self.sleep_DC): #detected when sleep
                    self.fourth_case += 1
                # self._dc += 1
                #---------------------------------------------------

                cur_row = f.readline()
                if cur_row:
                    sec, ID, x_coord, y_coord, AP_ID = list(map(int, cur_row[:-1].split(',')))

            if cur_t == 86400:
                # self._dc = 100*self._dc/(3600.0*4.0*24.0)   #이거 기존코드에서는 slot size가 0.25라서 그런듯 - 하루단위도 아닌거같음 1frame = 100slot
                # detected_contacts = self.first_case + self.second_case + self.third_case + self.fourth_case
                # self.ENERGY_CONSUMPTION = 1.0 - (self._dc*self.AWAKE_ENERGY + (100.0-self._dc)*self.SLEEP_ENERGY)/\
                #     (self.init_DC*self.AWAKE_ENERGY + (100.0-self.init_DC)*self.SLEEP_ENERGY)
                
                #논문식으로 구현 -> duty cycle구하는대로 더하기 
                #식: ENERGY_CONSUMPTION = TOTAL_TIME_AWAKE*AWAKE_ENERGY + TOTAL_TIME_SLEEP*SLEEP_ENERGY


                detected_contacts = self.first_case + self.second_case + self.third_case + self.fourth_case 
                self.accuracy_sigma = self.second_case/detected_contacts
                self.accuracy_gamma = self.third_case/detected_contacts

                #rewards
                effic_s = self.accuracy_sigma/self.ENERGY_CONSUMPTION
                effic_g = self.accuracy_gamma/self.ENERGY_CONSUMPTION

                msg = "efficiency " + str(effic_s)
                print(msg)
                self.rl.rl_env_msg(msg)
                self.rl.rl_step()

                #----------질문: 그러면 업뎃된 시그마, 감마값은 어떻게 반영됨?? -----------

                print("one day passed!")
                print("Energy consumption on day "+str(self.DAY)+": "+str(self.ENERGY_CONSUMPTION))

                #------init------
                self.first_case = 0
                self.second_case = 0
                self.third_case = 0
                self.fourth_case = 0
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