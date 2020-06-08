#-*- coding:utf-8 -*-

import csv
import queue
import neighborDiscovery
import math
import time
from datetime import datetime

from src_3.agent import agent
from src_3.env import env
from src_3.rl import rl

'''
file format:
sec(int),AP_ID,x_coordinate(m),y_coordinate(m),date,Client_ID\n
(csv)

example:
sec | AP_ID | x_coordinate | y_coordinate | date | Client_ID
53619	69	21804	32683	2014-09-01	62767
54044	184	21836	32737	2014-09-01	62767
54096	57	21804	32683	2014-09-01	62767
54173	58	21804	32683	2014-09-01	62767
....

'''

class Simulator:
    def __init__(self):
        self.STORAGE_MAX = 40

        #------for energy calculation------
        self.ENERGY_CONSUMPTION = 0
        self.ENERGY_FDC = 0
        self.ENERGY_REDUCTION = 0

        self.accuracy_sigma = 0
        self.accuracy_gamma = 0
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
        self.agent_s = agent()
        self.agent_g = agent()
        self.env = env(False, False)
        self.env_s = env(False, True)
        self.env_g = env(True, False)
        self.rl = rl()
        self.rl_s = rl()
        self.rl_g = rl()

        #self.rl.rl_init(self.agent, self.env)
        #self.rl.rl_start()

        self.rl_s.rl_init(self.agent_s, self.env_s)
        self.rl_s.rl_start()

        self.rl_g.rl_init(self.agent_g, self.env_g)
        self.rl_g.rl_start()

        self.INTERVAL_SIGMA = 120
        self.INTERVAL_GAMMA = 0.1

        #------INITIAL VALUE: will be learned by RL-------
        self.SIGMA = 5000
        self.GAMMA = 3
        #self.SIGMA = self.rl_s.rl_getParam()
        self.GAMMA = self.rl_g.rl_getParam()


    def simulate(self, filename):
        '''
            input: filepath+name as string
        '''
        # start_time = time.time()
        f = open(filename,'r')
        cur_t = 0
        cur_row = f.readline()
        sec, AP_ID, x_coord, y_coord, date, Client_ID = cur_row[:-1].split('\t')
        sec, AP_ID, x_coord, y_coord, Client_ID = list(map(int, [sec, AP_ID, x_coord, y_coord,Client_ID]))
        start_date = datetime.strptime(date,"%Y-%m-%d")
        cur_date = start_date
        
        storage = queue.Queue(maxsize=self.STORAGE_MAX)

        while cur_row != "":
            if(cur_t%10000 == 0):
                print(cur_t," seconds passed")

            #contact prediction
            predicted = self.nd.ContactPrediction(storage, self.SIGMA)
            
            #duty cycle adaptation
            case, dc = self.nd.DutyCycleAdaptation(predicted, cur_t, self.GAMMA)

            #add energy consumption by duty cycle
            self.ENERGY_CONSUMPTION += dc*0.01*self.AWAKE_ENERGY + (100-dc)*0.01*self.SLEEP_ENERGY
            self.ENERGY_FDC += self.init_DC*0.01*self.AWAKE_ENERGY + (100-self.init_DC)*0.01*self.SLEEP_ENERGY

            with open("graph.csv",'a') as wf:
                output = "{dc_def},{dc_cur},{detected}\n"
                if sec==cur_t:
                    wf.write(output.format(dc_def=self.init_DC, dc_cur=dc, detected=1))
                else:
                    wf.write(output.format(dc_def=self.init_DC, dc_cur=dc, detected=0))

            #if there's new log in current time: contact learning
            if(sec == cur_t):
                #read
                if storage.qsize() == self.STORAGE_MAX:
                    storage.get()
                storage.put(sec)    #insert to the storage: sec

                print("detected time: ",cur_t,", case: ",case)
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
                    sec, AP_ID, x_coord, y_coord, date, Client_ID = cur_row[:-1].split('\t')
                    sec, AP_ID, x_coord, y_coord, Client_ID = list(map(int, [sec, AP_ID, x_coord, y_coord, Client_ID]))
                    cur_date = datetime.strptime(date,"%Y-%m-%d")

            if cur_t == 86400:
                #run rl once a day
                detected_contacts = self.first_case + self.second_case + self.third_case + self.fourth_case 
                self.accuracy_sigma = self.second_case/detected_contacts
                self.accuracy_gamma = self.third_case/detected_contacts

                #rewards
                effic_s = self.accuracy_sigma/self.ENERGY_CONSUMPTION
                effic_g = self.accuracy_gamma/self.ENERGY_CONSUMPTION

                msg_s = "efficiency " + str(effic_s)
                msg_g = "efficiency " + str(effic_g)
                
                #self.rl.rl_env_msg(msg_s)
                #self.rl.rl_step()

                self.rl_s.rl_env_msg(msg_s)
                self.rl_s.rl_step()

                self.rl_g.rl_env_msg(msg_g)
                self.rl_g.rl_step()

                # 일단은 env에서 시그마 = 0.1~0.3 감마 = 1020~1380 범위로 설정해둬서 rl에서 읽어오면 제대로 안돌아감
                # parameter 관련 식 해결되면 rl_getParam()로 불러올 예정
                #self.SIGMA = self.rl_s.rl_getParam()
                self.GAMMA = self.rl_g.rl_getParam()

                print("############################")
                print("one day have passed! (", self.DAY, ")")
                print("Energy reduction: ",1-self.ENERGY_CONSUMPTION/self.ENERGY_FDC)
                print("Detection accuracy: ",self.accuracy_gamma+self.accuracy_sigma)
                print("############################\n")

                #------init------
                self.first_case = 0
                self.second_case = 0
                self.third_case = 0
                self.fourth_case = 0
                cur_t = 1
                self.DAY += 1
                
                self.ENERGY_CONSUMPTION = 0
                self.ENERGY_FDC = 0

                if((cur_date-start_date).days>=5):
                    break
                
            else:
                cur_t += 1

        f.close()
        # end_time = time.time() - start_time
        #print("Total energy consumption: "+str(self.ENERGY_CONSUMPTION))
        # print("Total work done in"+end_time+"seconds")