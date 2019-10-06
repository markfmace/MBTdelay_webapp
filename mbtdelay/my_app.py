#!/home/ubuntu/anaconda3/bin/python
from flask import Flask, Markup, render_template, request, send_file
from mbtdelay import app
import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import base64
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.axes_grid1 import make_axes_locatable

# GENERAL INCLUSIONS
import glob
import pickle
import requests


# FOR DATES AND TIMES #
import time
import datetime
from dateutil import tz
from datetime import timedelta
import arrow

# MODEL
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
import lightgbm as lgb


# DICTIONARY OF TRAIN STATIONS AND NUMBERS BY MBTA #

# NORTHBOUND -- USUALLY EVEN
north_bound=np.array(
                     [
                      ["Riverside","70160"],
                      ["Woodland","70162"],
                      ["Waban","70164"],
                      ["Eliot","70166"],
                      ["Newton Highlands","70168"],
                      ["Newton Centre","70170"],
                      ["Chestnut Hill","70172"],
                      ["Reservoir","70174"],
                      ["Beaconsfield","70176"],
                      ["Brookline Hills","70178"],
                      ["Brookline Village","70180"],
                      ["Longwood","70182"],
                      ["Fenway","70186"],
                      ["Kenmore","70150"],
                      ["Hynes Convention Center","70152"],
                      ["Copley","70154"],
                      ["Arlington","70156"],
                      ["Boylston","70158"],
                      ["Park Street","70200"],
                      ["Government Center","70201"],
                      ["Haymarket","70203"],
                      ["North Station","70205"],
                      ["Science Park","70207"],
                      ["Lechmere","70210"]
                      ]
                     
                     )


# SOUTHBOUND -- USUALLY ODD
south_bound=np.array(
                     [
                      ["Lechmere","70210"],
                      ["Science Park","70207"],
                      ["North Station","70205"],
                      ["Haymarket","70203"],
                      ["Government Center","70202"],
                      ["Park Street","70200"],
                      ["Boylston","70159"],
                      ["Arlington","70157"],
                      ["Copley","70155"],
                      ["Hynes Convention Center","70152"],
                      ["Kenmore","70150"],
                      ["Fenway","70187"],
                      ["Longwood","70182"],
                      ["Brookline Village","70181"],
                      ["Brookline Hills","70179"],
                      ["Beaconsfield","70177"],
                      ["Reservoir","70175"],
                      ["Chestnut Hill","70173"],
                      ["Newton Centre","70171"],
                      ["Newton Highlands","70169"],
                      ["Eliot","70167"],
                      ["Waban","70165"],
                      ["Woodland","70163"],
                      ["Riverside","70160"]
                      ]
                     )


# API KEYS -- NEED TO SPECIFY APIs
from MY_API_KEYS import *

BASE="/Users/mark/Dropbox/INSIGHT/FLASK/WEBAPP/mbtdelay" # LOCAL
#BASE="/home/ubuntu/application/mbtdelay" # AWS



# CONVERT UNIX (utc) TIMESTAMP TO YYYY-mm-dd HH:MM:SS (EASTERN)
def conv_unixts_to_east_hms(ts):
    east=arrow.Arrow.fromtimestamp(ts).to('US/Eastern')
    return east.format('YYYY-MM-DD HH:mm:ss')

def conv_unixts_to_east_dateonlys(ts):
    east=arrow.Arrow.fromtimestamp(ts).to('US/Eastern')
    return east.format('YYYY-MM-DD')

def conv_unixts_to_east_dateonlys_plot(ts):
    east=arrow.Arrow.fromtimestamp(ts).to('US/Eastern')
    return east.format('MM/DD/YYYY')

# CONVERT YYYY-mm-dd (EASTERN) TO UNIX (utc) TIMESTAMP
def conv_east_to_unixts_dateonly(dt):
    east=arrow.get(dt,'YYYY-MM-DD').replace(tzinfo='US/Eastern')     # NOW HAS TZ ATTACHED
    # RETURN UNIX TIMESTAMP
    return east.timestamp

## CONVERT HUMAN READABLE TO UNIX TIMESTAMP
# CONVERT YYYY-mm-dd HH:MM:SS (EASTERN) TO UNIX (utc) TIMESTAMP
def conv_east_to_unixts_hms(dt):
    east=arrow.get(dt,'YYYY-MM-DD HH:mm:ss').replace(tzinfo='US/Eastern')     # NOW HAS TZ ATTACHED
    # RETURN UNIX TIMESTAMP
    return east.timestamp

# RETURNS DAY OF WEEK
# M-0, Tu-1, W-2, Th-3 F-4 Sa-6 Su-7
# TAKES YYYY-MM-DD HH:MM:SS RETURNS Day (IN WHATEVER TIMEZONE)
def get_day_of_week(dt):
    dtt = arrow.get(dt)
    return dtt.weekday()

# TAKES UNIX TS RETURNS Day (IN EASTERN/BOSTON)
def get_day_of_week_east_unix(ts):
    east=conv_unixts_to_east_hms(ts)
    return get_day_of_week(east)

# TAKES UNIX TS RETURNS Day (IN UTC)
def get_day_of_week_utc_unix(ts):
    utc=conv_unixts_to_utc_hms(ts)
    return get_day_of_week(utc)

def days(x):
    return int(24*60*60*x)

def get_date(dt_str):
    return str(dt_str)[:10]

def get_hour(dt_str):
    return dt_str[11:13]

def get_month_num(dt_str):
    return dt_str[5:7]

# GET AND SAVE WEATHER DATA FROM DARK SKY FOR A GIVEN POSITION AND DATE RANGE
# DATES ARE DEFINED FOR THE LOCAL TIME
def get_input_data(lat,long):
    
    dt_now = datetime.datetime.now() # HUMAN READABLE PRESENT DATE-TIME IN EASTERN
    #print("dt_now",dt_now)
    dt_now=get_date(dt_now) # GET DATE ONLY PART
    unix_ts_stat=conv_east_to_unixts_dateonly(dt_now)
    #print("unix_ts_stat ",unix_ts_stat)
    base_url='https://api.darksky.net/forecast/'+MY_DS_KEY+'/'+str(lat)+','+str(long)
    
    all_days=[] # STORAGE OF WEATHER DATA FOR ALL DAYS REQUESTED
    
    # IMPORT UPCOMING EVENTS
    uce_df=pd.read_csv(BASE+"/data/upcoming_events.csv")
    uce_start=uce_df['start_time_east']
    uce_end=uce_df['end_time_east']
    uce_start_unix=uce_start.apply(lambda x: conv_east_to_unixts_hms(x)) # UNIX TIMESTAMPS
    uce_end_unix=uce_end.apply(lambda x: conv_east_to_unixts_hms(x))
    
    # PULL WEATHER DATA FOR ALL DAYS #
    #for i in range(1,num_days):
    
    loc_ts=str(unix_ts_stat+days(1)) # ADD ONE DAY IN UNIX TIME

    
    request_URL=base_url+','+loc_ts

    # API REQUEST
    response=requests.get(request_URL)
    day_data=response.json()["hourly"]["data"]
    
    ts=0
    temp=0.0
    precip_int=0.0
    precip_pro=0.0
    precip_acc=0.0
    precip_typ='None'
    
    # LOOP THROUGH ALL HOURS IN THE DAY #
    # STORE TIME, TEMPTAUTRE, PRECIPIATION INTENSITY AND PROBA
    for hour_data in day_data:
        
        ts=hour_data['time'] # UTC TIME #
        #print("ts ",ts)
        full_datetime=conv_unixts_to_east_hms(ts)
        #print("ts ",full_datetime)
        
        dow=get_day_of_week_east_unix(ts)
        #print("dow ",dow)
        
        # DETERMINE IF AN EVENT IS HAPPENING OUT OF UPCOMING EVENTS
        event_flag=0
        for i in range(len(uce_start_unix)):
            if(ts>=uce_start_unix[i] and ts<uce_end_unix[i]):
                event_flag=1
                print("AN EVENT IS OCCURING AT ",full_datetime)
    
    
        try:
            temp=float(hour_data['temperature'])
        except BaseException:
            print("NO temperature GIVEN!!")
            print(hour_data)
            # USE VALUE FROM PREVIOUS HOUR
            # FILTER FOR VERY RARE OCCASION WHEN API DOESN'T HAVE DATA
        try:
            precip_int=float(hour_data['precipIntensity'])
        except BaseException:
            print("NO precipIntensity GIVEN!!")
            print(hour_data)
            # USE VALUE FROM PREVIOUS HOUR
        try:
            precip_pro=float(hour_data['precipProbability'])
        except BaseException:
            print("NO precipProbability GIVEN!!")
            print(hour_data)
        # USE VALUE FROM PREVIOUS HOUR
        
        try:
            precip_acc=float(hour_data['precipAccumulation'])
        except BaseException:
            precip_acc=0.0

        try:
            precip_typ=hour_data['precipType']
        except BaseException:
            precip_typ='None'

        norm_time=conv_unixts_to_east_hms(ts)
        #print("norm_time ",norm_time)
        hour=int(get_hour(norm_time))
        month=int(get_month_num(norm_time))
        #print("hour ",hour)
        #print("month ",month)


        #['HOUR_BIN'], ['DOW'], ['MONTH_BIN'],['event'],['PRECIP_INT'], ['PRECIP_ACC'],['PRECIP_PRO'], ['TEMP']]
        all_days.append([hour,dow,month,event_flag,precip_int,precip_acc,precip_pro,temp])

    # RETURN ARRAY OF ALL WEATHER DATA FOR DAYS AND LOCATION
    all_days=np.array(all_days,dtype=np.float32)
    return all_days,loc_ts

# DETERMINES WHICH DIRECTION AND DICTIONARY TO USE
def find_station(stat_name_o,stat_name_d):
    all_stat_names=[
                    "Lechmere", "Science Park", "North Station",
                    "Haymarket", "Government Center", "Park Street", "Boylston",
                    "Arlington", "Copley","Hynes Convention Center", "Kenmore","Fenway","Longwood",
                    "Brookline Village", "Brookline Hills", "Beaconsfield", "Reservoir",
                    "Chestnut Hill", "Newton Centre", "Newton Highlands", "Eliot",
                    "Waban","Woodland", "Riverside"
                    ]
    stat_ind_o=-1
    stat_ind_d=-1
    direction=-1
                    
    if(any(x==stat_name_o for x in all_stat_names) and any(x==stat_name_d for x in all_stat_names)):
        stat_ind_o=all_stat_names.index(stat_name_o)
        stat_ind_d=all_stat_names.index(stat_name_d)
    
        if(stat_ind_o>stat_ind_d):
            direction_flag=0
            return north_bound
        
        else:
            direction_flag=1
            return south_bound


    else:
        raise SystemExit('CRITICAL ERROR -- STATION DOESNT EXIST!')
    
    return

# DETERMINE DICTIONARY AND DETERMINE STATION ID NUMBERS
def get_station_ids(stat_name_o,stat_name_d):
    
    res=find_station(stat_name_o,stat_name_d)
    start_ind=np.where(res[:,0]==stat_name_o)[0][0]
    end_ind=np.where(res[:,0]==stat_name_d)[0][0]
    
    names=res[start_ind:(end_ind+1),0]
    ids=  res[start_ind:(end_ind+1),1]
    return names,ids

# IMPORT MODEL FROM FILE
#

def import_models():
    stations=[]
    models=[]
#    model_files=glob.glob(BASE+"/data/*.pk")
    model_files=glob.glob(BASE+"/lgb_model/*.txt")

    for file in model_files:
        
        model_station,model_id=file.replace(BASE+"/lgb_model/","").replace(".txt","").split("_")
        stations.append([model_station,model_id])
        model_tmp=lgb.Booster(model_file=file)
        models.append([model_tmp])
    
    stations=np.array(stations)
    return stations,models


