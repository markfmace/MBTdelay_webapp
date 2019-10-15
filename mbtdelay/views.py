##### MTBdelay_app -- view.py
##### (C) Mark Mace 2019
##### Gets data and makes plot for web-app

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

# GENERAL INCLUSIONS
import glob
import requests


# FOR DATES AND TIMES #
import time
import datetime
from dateutil import tz
from datetime import timedelta
import arrow

# MODEL
import lightgbm as lgb

from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

# INCLUDE BACKEND FOR APP
from mbtdelay import my_app
south_bound=my_app.south_bound
north_bound=my_app.north_bound

BASE="/Users/mark/Dropbox/INSIGHT/FLASK/WEBAPP/mbtdelay" # LOCAL
#BASE="/home/ubuntu/application/mbtdelay" # AWS

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():


    list1 = [[str(south_bound[i,0]),i] for i in range(len(south_bound))]
    # List you want for drop-down menu
    list2 = [[str(south_bound[i,0]),i] for i in range(len(south_bound))]

    
    # Initialize output
    # Plot figure, grab using BytesIO, then save
    fig = plt.plot()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Create Base64 image of the plot then decode to 'utf-8'
    # image = base64.b64encode(b''.join(img)).decode('utf-8')
    image = base64.b64encode(img.read()).decode('utf-8')
    
    # Initial values
    station1=0
    station2=0
    
    # If search was performed
    if request.method == "POST":
        
        # Can see in terminal what was input from file
        #print(request.form)
        
        # Get values from form
        station1 = int(dict(request.form)['input1'])
        station2 = int(dict(request.form)['input2'])
        
        origin_station=south_bound[station1][0]
        destination_station=south_bound[station2][0]
        
        stations=[]
        models=[]
        stations,models=my_app.import_models()
        #print("update_graph ",origin_station, destination_station)
        as_df=pd.read_csv(BASE+"/data/"+"AllStations.csv")
        dh_df=pd.read_csv(BASE+"/data/"+"DH_RES.csv")

        all_temps=[]
        all_precip=[]
        all_delays=[]
        
        all_hours=[]
        ts_targ=''


        stat_ids=my_app.get_station_ids(origin_station, destination_station)
    
        for s_id in stat_ids[1]:
            
            s_ind=np.where(stations[:,1]==s_id)[0][0]
            
            loc_model=models[s_ind][0]
            
            # GET STOP LATTIUTE AND LONGITUDE
            loc_as=as_df[as_df['stop_id']==int(s_id)]
            lat_loc=loc_as['stop_lat'].iloc[0]
            lon_loc=loc_as['stop_lon'].iloc[0]
            
            # GET HISTORIC MEAN DWELL AND GAP TIMES
            loc_df=dh_df[dh_df['station_id']==int(s_id)]
            
            #n_days=2
            
            weather_targ,ts_targ=my_app.get_input_data(lat_loc,lon_loc)

            hour_data=weather_targ[:,0]
            all_hours=hour_data
            precip_data=weather_targ[:,2]
            temp_data=weather_targ[:,3]
            
            loc_delay=loc_model.predict(weather_targ)
            all_temps.append(temp_data)
            all_precip.append(precip_data)
            all_delays.append(loc_delay)
        
        all_temps=np.array(all_temps)
        all_precip=np.array(all_precip)
        all_delays=np.array(all_delays)

        avg_temp=0.0
        avg_precip=0.0
        
        tot_head_delay=np.zeros((24))
        
        for i in range(len(all_delays)): # LOOP OVER ALL STATIONS IN ROUTE
            avg_temp+=all_temps[i]/len(all_temps)
            avg_precip+=all_precip[i]/len(all_precip)
            
            # LOOP OVER HOURS
            avg_head_delay=0
            
            for j in range(len(all_delays[i])): # POPULATE FOR ALL HOURS
                tot_head_delay[j]+= all_delays[i][j]

    
        # GET PREDICITON DATE
        date_targ=my_app.conv_unixts_to_east_dateonlys_plot(ts_targ)
        
        # DUMMY VALUES

        
        # Initialize Python plot
        fig, ax = plt.subplots(figsize=(9,2.0))
        #lt.style.use('fivethirtyeight')
        img = BytesIO()
        
        # No plot if same station
        if(station1==station2):
            x = all_hours
            y_raw = 0.0/60.0
            y_ph=[1 for i in range(len(x))]
            df = pd.DataFrame({"x":x,"y":y_ph,"c":y_raw})
            
            cmap = plt.cm.binary
            norm = matplotlib.colors.Normalize(vmin=0, vmax=240.0/60.0)
            ax.bar(df.x, df.y, align='center', width=1.0, color=cmap(norm(df.c.values)))
            ax.set_xticks(df.x)
            plt.xlim([5-0.5,24-0.5])
            plt.ylim([0,1])
            plt.xlabel(' ',fontsize=14)
            plt.tick_params(axis='y',which='both',bottom=False,top=False,labelbottom=False)
            
            plt.yticks([])
            plt.title("Select trip origin and destination",fontsize=10)
        
        # Specify values to plot based on values
        if(station1!=station2):
            x = all_hours
            y_raw = tot_head_delay/60.0
            y_ph=[1 for i in range(len(x))]
            df = pd.DataFrame({"x":x,"y":y_ph,"c":y_raw})
            
            cmap = plt.cm.RdYlGn_r
            norm = matplotlib.colors.Normalize(vmin=0, vmax=240.0/60.0)
            ax.bar(df.x, df.y, align='center', width=1.0, color=cmap(norm(df.c.values)))
            ax.set_xticks(df.x)
            plt.xlim([5-0.5,24-0.5])
            plt.ylim([0,1])
            plt.xlabel('Hour of day',fontsize=14)
            plt.tick_params(axis='y',which='both',bottom=False,top=False,labelbottom=False)
            
            plt.yticks([])
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            plt.text(27,0.00,"Potential minutes""\n""of delay",rotation=90,fontsize=14,horizontalalignment='center')

#            plt.colorbar(im, cax=cax)
            plt.colorbar(sm, fraction=0.046, pad=0.04)

            plt.title("Trip from "+south_bound[station1][0]+" to "+south_bound[station2][0]+" on "+date_targ,fontsize=14)
            plt.tight_layout()

#        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.clf()
        
        # Create Base64 image of the plot then decode to 'utf-8'
        # image = base64.b64encode(b''.join(img)).decode('utf-8')
        image = base64.b64encode(img.read()).decode('utf-8')
    
    # Send lists and image to html file
    return render_template('index.html', list1=list1, list2=list2, image=image, station1=station1, station2=station2)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/presentation')
def presentation():
    return render_template('presentation.html')

