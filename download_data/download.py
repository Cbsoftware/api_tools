#!/usr/bin/env python

import os
import sys
import requests
import json
import arrow, datetime, time
from dateutil.tz import tzutc 
from config import apikey, startsecond, startminute, starthour, startday, startmonth, startyear, endsecond, endminute, endhour, endday, endmonth, endyear, minlat, maxlat, minlon, maxlon, sleepamount, mins1, mins2


#which API to call
if sys.argv[1] == 'conditions': 
    service = 'conditions/list'
elif sys.argv[1] == 'readings':
    service = 'live'
else:
    print 'Unknown service'

def get_dname():
    if service == 'conditions/list':
        dname = 'conditions'
    else:
        dname = 'data'
       
    return dname

def make_dirs(jobname):
    dname = get_dname()
    if not os.path.exists(dname):
        os.makedirs(dname)

    #downloaded data will be stored in this directory
    if not os.path.exists(os.path.join(dname, jobname)):
        os.makedirs(os.path.join(dname, jobname))

def save_data(data, jobname):
    dname = get_dname()
    make_dirs(jobname)

    fn = os.path.join(dname, jobname, '{startdate}_{enddate}_{minlat}-{maxlat}_{minlon}-{maxlon}.json'.format(
            startdate = origstart.format('MMMM-DD-YYYY:HH:mm:ss'),
             enddate = ftime.format('MMMM-DD-YYYY:HH:mm:ss'),
             minlat = minlat, maxlat = maxlat, 
             minlon = minlon, maxlon = maxlon
            ))

    print "Data saved to " + fn

    with open(fn, 'w+') as outfile:
          json.dump(data, outfile)
          outfile.close()

def success(r, data):
    print "{} items downloaded".format(len(r.json()))

    if len(r.json()) > 0:
        data += r.json()

def attempt(params, data, jobname):
    s = params['start_time']
    f = params['end_time']

    try:
        r = requests.get('https://pressurenet.io/' + service, params=params)
        print "Request made to " + r.url
        print arrow.get(str(s/1000)).format('MMMM-DD-YYYY:HH:mm:ss') + " to " + arrow.get(str(f/1000)).format('MMMM-DD-YYYY:HH:mm:ss')
        print "Status: {}".format(r.status_code)
        if r.status_code == 200:
            success(r, data)

        return r
    except:
        print "An error occured"
        print sys.exc_info()[0] 
        save_data(data, jobname)

def log(r, s, f, jobname):
    make_dirs(jobname)

    errorlog = open('data/' + jobname + '/error_log', 'a+')
    errorlog.write(str(r.status_code) + "\n")
    errorlog.write(r.url + "\n")
    errorlog.write(str(arrow.get(s / 1000).date()) + " " + str(arrow.get(s / 1000).time()) + "\n")
    errorlog.write(str(arrow.get(f / 1000).date()) + " " + str(arrow.get(f / 1000).time()) + "\n")
    return errorlog

def make_call(s, f, data, jobname):
    logfile = None
    params = {'api_key': apikey, 'start_time': s, 'end_time': f,
               'min_lat': minlat, 'max_lat': maxlat,
               'min_lon': minlon, 'max_lon': maxlon 
              }
    
    r = attempt(params, data, jobname)
    
    if r.status_code != 200:
        time.sleep(2*sleepamount)
        print "Retrying"
        r2 = attempt(params, data, jobname)
        time.sleep(30 + sleepamount)
        if r2.status_code != 200:
            logfile = log(r2, s, f, jobname)

    if logfile:
        logfile.close()


if maxlat <=minlat:
    print "The maximum latitude must be greater than the minimum latitude."
    exit()
if maxlon <=minlon:
    print "The maximum longitude must be greater than the minimum longitude."
    exit()

try:
    jobname = sys.argv[2]
except:
    jobname = str(arrow.get())



stime = arrow.get(datetime.datetime(startyear, startmonth, startday, starthour, startminute, startsecond, tzinfo=tzutc()))
origstart = stime

ftime = arrow.get(datetime.datetime(endyear, endmonth, endday, endhour, endminute, endsecond, tzinfo=tzutc()))
origfinish = ftime.timestamp * 1000

data = []

ftimestamp = ftime.timestamp * 1000

#don't ask for more than 1 day's data at a time
while ((((ftime - stime).days >= 1) or ((ftime - stime).seconds > (60*mins1))) and (ftimestamp <= origfinish)):
    stimestamp = stime.timestamp * 1000
    ftimestamp = stime.replace(seconds=+(60*mins1)).timestamp * 1000

    make_call(stimestamp, ftimestamp, data, jobname)

    stime = arrow.get(ftimestamp / 1000)
    time.sleep(sleepamount)

    stimestamp = stime.timestamp * 1000
    ftimestamp = stime.replace(seconds=+(60*mins1)).timestamp * 1000

    make_call(stimestamp, ftimestamp, data, jobname)

    stime = arrow.get(ftimestamp / 1000)
    time.sleep(sleepamount)

while ((ftime - stime).seconds > (60*mins2) and (ftimestamp <= origfinish)):
    stimestamp = stime.timestamp * 1000
    ftimestamp = stime.replace(seconds=+(60*mins2)).timestamp * 1000

    make_call(stimestamp, ftimestamp, data, jobname)

    stime = arrow.get(ftimestamp / 1000)
    time.sleep(sleepamount)

stimestamp = stime.timestamp * 1000
ftimestamp = ftime.timestamp * 1000

make_call(stimestamp, ftimestamp, data, jobname)

save_data(data, jobname)
