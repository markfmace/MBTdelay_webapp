# FOR DATES AND TIMES #
# From MBTdelay #
# (C) Mark Mace 2019 #

import time
import datetime
from dateutil import tz
from datetime import timedelta
import arrow
from time import strptime

## CONVERT HUMAN READABLE TO UNIX TIMESTAMP
# CONVERT YYYY-mm-dd HH:MM:SS (EASTERN) TO UNIX (utc) TIMESTAMP
def conv_east_to_unixts_hms(dt):
    east=arrow.get(dt,'YYYY-MM-DD HH:mm:ss').replace(tzinfo='US/Eastern')     # NOW HAS TZ ATTACHED
    # RETURN UNIX TIMESTAMP
    return east.timestamp

# CONVERT YYYY-mm-dd HH:MM:SS (UTC/GMT) TO UNIX (utc) TIMESTAMP
def conv_utc_to_unixts_hms(dt):
    utc=arrow.get(dt,'YYYY-MM-DD HH:mm:ss').replace(tzinfo='UTC')     # NOW HAS TZ ATTACHED
    # RETURN UNIX TIMESTAMP
    return utc.timestamp

# CONVERT YYYY-mm-dd HH:MM (EASTERN) TO UNIX (utc) TIMESTAMP
## INCLUDES ROLLOVER FOR HH>23
def conv_east_to_unixts_hm(dt):
    hr=int(dt[11:13])
    remainder=0
    if hr>23:
        remainder=hr-23
        hr=23
        dt=dt[:11]+str(hr)+dt[13:]
    east=arrow.get(dt,'YYYY-MM-DD HH:mm').replace(tzinfo='US/Eastern')     # NOW HAS TZ ATTACHED
    ts=east.timestamp+60*60*remainder
    # RETURN UNIX TIMESTAMP
    return ts

# CONVERT YYYY-mm-dd HH:MM (UTC/GMT) TO UNIX (utc) TIMESTAMP
def conv_utc_to_unixts_hm(dt):
    utc=arrow.get(dt,'YYYY-MM-DD HH:mm').replace(tzinfo='UTC')     # NOW HAS TZ ATTACHED
    # RETURN UNIX TIMESTAMP
    return utc.timestamp

# CONVERT HUMAN READABLE BETWEEN TIMEZONES
# CONVERT YYYY-mm-dd HH:MM:SS (EASTERN) TO YYYY-mm-dd HH:MM:SS (UTC)
def conv_east_to_utc_hms(dt):
    east=arrow.get(dt,'YYYY-MM-DD HH:mm:ss').replace(tzinfo='US/Eastern')     # NOW HAS TZ ATTACHED
    utc=east.to('UTC')
    return utc.format('YYYY-MM-DD HH:mm:ss')

# CONVERT YYYY-mm-dd HH:MM:SS (UTC) TO YYYY-mm-dd HH:MM (EASTERN)
def conv_utc_to_east_hms(dt):
    utc=arrow.get(dt,'YYYY-MM-DD HH:mm:ss').replace(tzinfo='UTC')     # NOW HAS TZ ATTACHED
    east=utc.to('US/Eastern')
    return east.format('YYYY-MM-DD HH:mm:ss')

# CONVERT YYYY-mm-dd HH:MM (EASTERN) TO YYYY-mm-dd HH:MM (UTC)
def conv_east_to_utc_hm(dt):
    east=arrow.get(dt,'YYYY-MM-DD HH:mm').replace(tzinfo='US/Eastern')     # NOW HAS TZ ATTACHED
    utc=east.to('UTC')
    return utc.format('YYYY-MM-DD HH:mm')

# CONVERT YYYY-mm-dd HH:MM (UTC) TO YYYY-mm-dd HH:MM (EASTERN)
def conv_utc_to_east_hm(dt):
    utc=arrow.get(dt,'YYYY-MM-DD HH:mm').replace(tzinfo='UTC')     # NOW HAS TZ ATTACHED
    east=utc.to('US/Eastern')
    return east.format('YYYY-MM-DD HH:mm')

## CONVERT UNIX TIMESTAMP TO HUMAN READABLE
# CONVERT UNIX (utc) TIMESTAMP TO YYYY-mm-dd HH:MM:SS (UTC)
def conv_unixts_to_utc_hms(ts):
    utc=arrow.Arrow.fromtimestamp(ts).to('UTC')
    return utc.format('YYYY-MM-DD HH:mm:ss')

# CONVERT UNIX (utc) TIMESTAMP TO YYYY-mm-dd HH:MM:SS (EASTERN)
def conv_unixts_to_east_hms(ts):
    east=arrow.Arrow.fromtimestamp(ts).to('US/Eastern')
    return east.format('YYYY-MM-DD HH:mm:ss')

# CONVERT UNIX (utc) TIMESTAMP TO YYYY-mm-dd HH:MM (UTC)
def conv_unixts_to_utc_hm(ts):
    utc=arrow.Arrow.fromtimestamp(ts).to('UTC')
    return utc.format('YYYY-MM-DD HH:mm')

# CONVERT UNIX (utc) TIMESTAMP TO YYYY-mm-dd HH:MM (EASTERN)
def conv_unixts_to_east_hm(ts):
    east=arrow.Arrow.fromtimestamp(ts).to('US/Eastern')
    return east.format('YYYY-MM-DD HH:mm')

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

