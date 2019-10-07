### ML SPECIFIC FUNCTIONS
### FOR FEATURE ENGINEERING
# ENCODE EVENT -- 1--event, 0--no event
def bin_event(x):
    x=int(x)
    if(x!=0):
        return 1
    else:
        return 0

# YES OR NO
def bin_weather(x):
    x=float(x)
    if(x>0):
        return 1
    else:
        return 0

# BIN PRECIPITATION TYPE
def bin_ptype(x):
    if(x==1): # None
        return 0
    else: # rain, snow or sleet
        return 0

# BIN IN d_bin SECONDS
d_bin=10
def bin_delay(x):
    x=float(x)
    if(x<=0):
        return 0
    else:
        return int(x/d_bin)

#BIN IN t_bin DEGREES
t_bin=10
def bin_temp(x):
    x=float(x)
    if(x<=0):
        return 0
    else:
        return int(x/t_bin)


# PEAK HOUR BIN
def bin_peak(x):
    x=float(x)
    if(6<=x<=10 or 4<=x<=7):
        return 1
    else:
        return 0

# WEEKDAY BIN
def bin_weekday(x):
    x=float(x)
    if(x<5):
        return 1 # WEEKDAY
    else:
        return 0 # WEEKEND

# SEASON
def bin_season(x):
    x=float(x)
    if(x in {1,2,12}):
        return 0 # WINTER
    elif(x in {3,4,5}):
        return 1 # SPRING
    elif(x in {9,10,11}):
        return 2 # FALL
    elif(x in {6,7,8}):
        return 3 # SUMMER
    else:
        print("NOT A VALID MONTH")
        return -1 # WRONG
