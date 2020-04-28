import pandas as pd
from datetime import datetime
import pickle

def split_file(filename):
    df = pd.read_csv("traceset1/"+filename)
    strt = 0
    prev_time = pd.to_datetime(df.loc[0,'timestamp'])
    for i,time in enumerate(df['timestamp']):
        cur_time = pd.to_datetime(time)
        if(prev_time.day != cur_time.day):
            df[strt:i].to_csv("trace_by_date/"+prev_time.strftime("%Y_%m_%d")+".csv")
            prev_time = cur_time
            strt = i
    df[strt:].to_csv("trace_by_date/"+prev_time.strftime("%Y_%m_%d")+".csv")

def to_sec(df):
    t0 = pd.to_datetime(df.loc[0,'timestamp']).normalize()
    df["sec"] = (pd.to_datetime(df["timestamp"]) -t0).dt.total_seconds()

def to_ID(df):
    c_id_lst = []
    # dictionary, lastcount는 공유해야함: pickle
    with open("ID_dictionary.pickle","rb") as fr:
        dic = pickle.load(fr)
    with open("ID_cnt.pickle","rb") as fr:
        c_id = pickle.load(fr)    
        
    for client in df.client:
            if client in dic:
                c_id_lst.append(dic[client])
            else:
                c_id_lst.append(c_id)
                dic[client] = c_id
                c_id += 1
    df["ID"] = c_id_lst
                
    with open("ID_dictionary.pickle","wb") as fw:
        pickle.dump(dic, fw)
    with open("ID_cnt.pickle","wb") as fw:
        pickle.dump(c_id, fw)