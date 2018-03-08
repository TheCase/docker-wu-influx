#!/usr/bin/env python

#only run every five minutes - for 480 of 500 daily calls

import sys, os
import urllib2
import json
import time

import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

from influxdb import InfluxDBClient
def influx( measurement, location, value):
   client = InfluxDBClient(os.environ['INFLUXHOST'], os.environ['INFLUXPORT'], os.environ['INFLUXUSER'], os.environ['INFLUXPASS'], os.environ['INFLUXDB'])

   json_body = [
      {
         "measurement": str(measurement),
         "tags": { "location": str(location), "source": "wu" },
         "fields": { "value": float(value) }
      }
   ]
   client.write_points(json_body)

apikey = os.environ['WU_KEY']
city = os.environ['WU_CITY'] 
state = os.environ['WU_STATE']
apiurl = "http://api.wunderground.com/api/"+ apikey +"/conditions/q/" + state + "/" + city + ".json";

while True:
    while True:
       count = 0
       f = urllib2.urlopen(apiurl)
       json_string = f.read()
       parsed_json = json.loads(json_string)
       if 'current_observation' in parsed_json:
          break
       elif count > 59:
          print 'retry limit of 60 tries exceeded.  Aborting'
          sys.exit(1)
       else:
          print 'current_observation not found in returned json: '
          print json_string
          print '++ Retrying [{0}]...'.format(count)
       time.sleep(1)
       count += 1

    temp = parsed_json['current_observation']['temp_f'];
    wind = parsed_json['current_observation']['wind_mph'];
    wind_gust = parsed_json['current_observation']['wind_gust_mph'];
    pressure = parsed_json['current_observation']['pressure_in'];
    bar = parsed_json['current_observation']['pressure_mb'];
    humid = parsed_json['current_observation']['relative_humidity'];

    print "temp:"+str(temp)+",wind:"+str(wind)+",gust:"+str(wind_gust)+",pre:"+str(pressure)+",bar:"+str(bar)+",humid:"+str(humid)

    influx('temperature','wu',temp)
    influx('humidity','wu',humid.replace('%',''))
    influx('wind','avg',wind)
    influx('wind','gust',wind_gust)
    influx('pressure','in',pressure)
    influx('pressure','bar',bar)

    f.close()

    time.sleep(int(os.environ['POLL_INTERVAL']) )
