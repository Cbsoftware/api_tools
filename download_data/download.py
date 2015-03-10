#!/usr/bin/env python

import sys
import os
import json
import requests
import arrow, datetime, time
from config import apikey, startsecond, startminute, starthour, startday, startmonth, startyear, endsecond, endminute, endhour, endday, endmonth, endyear, sleepamount, dataformat, minlat, maxlat, minlon, maxlon
from dateutil.tz import tzutc 

service = 'api/pressure'

FILTERING = minlat > -90 or maxlat < 90 or minlon > -180 or maxlon < 180

def in_bounds(d):
    lat = float(d['latitude'])
    lon = float(d['longitude'])
    fminlat = float(minlat)
    fmaxlat = float(maxlat)
    fminlon = float(minlon)
    fmaxlon = float(maxlon)
    ret = (lat >= fminlat) & (lat <= fmaxlat) & (lon >= fminlon) & (lon <= fmaxlon)
    return ret

def geo_filter(data):
    return [d for d in data if in_bounds(d)]

def make_dirs(jobname):
    dname = 'data'
    if not os.path.exists(dname):
        os.makedirs(dname)

    #downloaded data will be stored in this directory
    if not os.path.exists(os.path.join(dname, jobname)):
        os.makedirs(os.path.join(dname, jobname))

def save_data(data, jobname, stime, etime, dataformat):
    dname = 'data'
    make_dirs(jobname)

    fn = os.path.join(dname, jobname, '{starttime}_{endtime}.{ext}'.format(
            starttime = stime.format('MMMM-DD-YYYY:HH:mm:ss'),
            endtime = etime.format('MMMM-DD-YYYY:HH:mm:ss'),
            ext = dataformat
            ))

    print "Data saved to " + fn

    with open(fn, 'w+') as outfile:
          if dataformat == 'json':
              json.dump(data, outfile)
	  else:
              outfile.write(('\n').join(data))              

def success(r, data):
    if dataformat == 'json':
        items = r.json()
    else:
        items = r.text.split('\n')
    
    print "{} items downloaded".format(len(items))

    if len(items) > 0:
        data += items
  
    return data

def make_call(params, data, t, jobname):
    r = requests.get('https://pressurenet.io/' + service, params=params)
    print "Request made to " + r.url
    print arrow.get(str(params['timestamp']/1000)).format('MMMM-DD-YYYY:HH:mm:ss')
    print "Status: {}".format(r.status_code)
    if r.status_code == 200:
        data = success(r, data)
        if FILTERING:
            data = geo_filter(data)
    else:
        print "an error occurred: " + str(r.status_code)

    return data

def download_stuff(jobname):
    stime = arrow.get(datetime.datetime(startyear, startmonth, startday, starthour, startminute, startsecond, tzinfo=tzutc()))

    etime = arrow.get(datetime.datetime(endyear, endmonth, endday, endhour, endminute, endsecond, tzinfo=tzutc()))

    endtime = etime.timestamp * 1000
    t = stime.timestamp * 1000

    data = []
    while(t < endtime):
        params = {'timestamp': t, 'api_key':apikey, 'format':dataformat}
        data = make_call(params, data, t/1000, jobname)
        t = arrow.get(t / 1000).replace(seconds=+600).timestamp * 1000

    save_data(data, jobname, stime, etime, dataformat)
    print "finished"

if __name__ == "__main__":
    jobname = sys.argv[1]
    download_stuff(jobname)
