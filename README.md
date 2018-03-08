ENV VARS:
```
INFLUXHOST - influxdb host
INFLUXPORT - influxdb port
INFLUXDB -   influxdb database
POLL_INTERVAL - # seconds between API connections

WU_KEY - weatherunderground key
WU_CITY - weatherunderground city 
WU_STATE - weatherunderground state
```
`docker run -d -e WU_KEY=<key> -e WU_CITY='Some City' -e WU_STATE=CA --restart=always --name wu thecase/wu-influx`
