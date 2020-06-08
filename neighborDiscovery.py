#-*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import math
from scipy.stats import norm

class neighborDiscovery:
    def __init__(self):
        self.DIMENSION = 3

        self.DELTA = 900  #Contact prediction->prediction phase에서 같은 집합으로 선정되는 시간 간격 기준
        self.EPS_prd = 0.3 #Contact prediction->prediction phase에서 선정되는 최소 집합 사이즈

        #persentage
        self.DC_MIN = 2     #DC sleep
        self.DC_MAX = 20
        self.DC_DEF = 8     #DC init

        #seconds
        self.L_PRD = 900
        self.L_EXP = 360

        #standart deviation
        self.SIGMA_PRD = self.L_PRD/math.sqrt(8*math.log(self.DC_MAX/self.DC_DEF))
        self.SIGMA_EXP = self.L_EXP/math.sqrt(8*math.log(self.DC_DEF/self.DC_MIN))
        self.A_PRD = self.DC_MAX*self.SIGMA_PRD*math.sqrt(2*math.pi)
        self.A_EXP = self.DC_DEF*self.SIGMA_EXP*math.sqrt(2*math.pi)


    def ContactPrediction(self, storage, SIGMA):
        '''
        input:
            - storage queue
            - SIGMA value from reinforcement learning

        output:
            - list of predicted contactable time
        '''
        #minimum q size 다시 확인
        if(storage.qsize()<self.DIMENSION):
            return []

        #convert to patterns of size DIMENSION
        patterns=[]
        t_list = []
        qsize = storage.qsize()
        for i in range(self.DIMENSION):
            t_list.append(storage.get())

        for i in range(qsize-self.DIMENSION):
            patterns.append(np.array(t_list))
            storage.put(t_list[0])
            t_list = t_list[1:]
            t_list.append(storage.get())

        for i in range(self.DIMENSION):
            storage.put(t_list[i])

        patterns.append(np.array(t_list))
        
        #similarity check
        predicted = self.SimilarityCheck(patterns, SIGMA)

        #prediction
        return self.Prediction(predicted)
        

    def SimilarityCheck(self, patterns, SIGMA):
        predicted = []
        for i,val in enumerate(patterns[:-1]):
            standard_deviation = np.var(patterns[-1])
            v_sigma = standard_deviation * SIGMA
            if np.linalg.norm(patterns[-1]-val, ord = np.inf) < v_sigma:  #maximum norm
                predicted.append(patterns[i+1][0])
        return predicted

    def Prediction(self, predicted):
        if not predicted:
            return []

        R_prd,tmp = [],[]
        for i,val in enumerate(predicted[:-1]):
            tmp.append(val)
            if(predicted[i+1] - val > self.DELTA):
                #separate
                if len(tmp)/len(predicted) > self.EPS_prd:
                    R_prd.append(np.average(tmp))
                tmp = []
        tmp.append(predicted[-1])
        if len(tmp)/len(predicted) > self.EPS_prd:
            R_prd.append(np.average(tmp))

        return R_prd


    def DutyCycleAdaptation(self, predicted, t, GAMMA):
        '''
        input:
            - predicted times from Contact Prediction
            - current time: second
            - GAMMA value from reinforcement learning

        output:
            - current duty cycle
        '''
        if not predicted:
            return (1, self.DC_DEF)

        C, case = 0, 0
        for i,cur_t in enumerate(predicted):
            C_prd = self.A_PRD*norm(cur_t, self.SIGMA_PRD).pdf(t)
            if(i == 0):
                cur_case = 2
                C_exp = 0
            else:
                cur_case = 3
                C_exp = self.Seren(t, predicted[i-1], cur_t, GAMMA)

            if(C < C_prd+C_exp):
                case = cur_case
                C = C_prd+C_exp 
        
        if C<self.DC_MIN:
            case = 4
            C = self.DC_MIN
        return (case, C)


    def Seren(self, t, t_s, t_e, GAMMA):
        div_g = math.ceil((t_e-t_s)/GAMMA)
        if div_g == 0:
            return 0
        n_sub = math.ceil((t_e-t_s)/div_g)
        if n_sub <= 1:
            return 0

        t_exp = 99999 #some big number
        for i in range(1,n_sub):
            t_tmp = t_s+i*(t_e-t_s)/n_sub
            if abs(t-t_exp) > abs(t-t_tmp):
                t_exp = t_tmp
        return self.A_EXP*norm(t_exp, self.SIGMA_EXP).pdf(t)

