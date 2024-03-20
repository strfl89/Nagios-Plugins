#!/usr/bin/python

#########################################################################
#
# Nagios Plugin for Checking Blebox Sensors with focus on the tempsensor
#
# Version: 20240319.01
#
# Developer: florian@strunk-media.de
#
#########################################################################
#
# Nagios Exit Codes
#
# 0	=	OK
# 1	=	Warning
# 2	=	Critical
# 3	=	Unknown
#
#########################################################################

import argparse
import requests
import sys

from datetime import datetime, timedelta

parser=argparse.ArgumentParser(description="Nagios Plugin for Blebox Sensors")
parser.add_argument('-H', dest='host', required=True, metavar='<IP or Hostname>', help='IP Adress or Hostname of Sensor')
parser.add_argument('-T', dest='typ', metavar='Type of Check', help='Typ of Check to perform', choices=['temperature','uptime'])
parser.add_argument('-W', dest='warning', metavar='Warn Level', help='Warn Level', default='86400')
parser.add_argument('-C', dest='critical', metavar='Crit Level', help='Critical Level', default='44200')
parser.add_argument('-twl', dest='temp_warn_low', metavar='Low Warning Temperature', help='Low Warning Temperature, default 18°C', default='18')
parser.add_argument('-twh', dest='temp_warn_high', metavar='High Warning Temperature', help='High Warning Temperature, default 25°C', default='25')
parser.add_argument('-tcl', dest='temp_crit_low', metavar='Low Critical Temperature', help='Low Critical Temperature, default 17°C', default='17')
parser.add_argument('-tch', dest='temp_crit_high', metavar='High Critical Temperature', help='High Critical Temperature, default 30°C', default='30')
args=parser.parse_args()

match args.typ:
	# Check Temperature ob TempSensor
    case 'temperature':
        # get state via Device API
        r=requests.get('http://' + args.host + '/state')
        # Format Temperature
        temp=r.json()["tempSensor"]["sensors"][0]["value"]/100
        # Format Temperature Trend
        match r.json()["tempSensor"]["sensors"][0]["trend"]:
            case 1:
                temp_trend="consistent"
            case 2:
                temp_trend="decreasing"
            case 3:
                temp_trend="increasing" 
        # Create Status Text
        statustext="Temperature is " + str(temp) + "°C and Temperature Trend is " + str(temp_trend)
        # Convert args to float
        temp_crit_low=float(args.temp_crit_low)
        temp_crit_high=float(args.temp_crit_high)
        temp_warn_low=float(args.temp_warn_low)
        temp_warn_high=float(args.temp_warn_high)
        # Check Warn + Crit Levles for Status
        status=3
        if temp > temp_warn_low and temp < temp_warn_high:
        	status=0
        elif temp > temp_crit_high and temp_trend == "decreasing":
            status=1
        elif temp < temp_crit_low and temp_trend == "increasing":
            status=1
        elif temp > temp_crit_high or temp < temp_crit_low:
            status=2
        elif temp > temp_warn_high or temp < temp_warn_low:
            status=1
        # Set Check Result and Exit Code
        match status:
            case 0:
                print("OK - " + statustext)
            case 1:
                print("WARNING - " + statustext)
            case 2:
                print("CRITICAL - " + statustext)
            case _:
                print("UNKNOWN - " + statustext)
        # Exit Skript and report Status to Nagios
        sys.exit(status)

    # Check Uptime of Sensor
    case 'uptime':
        # get uptime via Device API
        r=requests.get('http://' + args.host + '/api/device/uptime')
        # Format Uptime from ms to Date
        days = divmod(r.json()["uptimeS"], 86400) # days[0] = whole days and days[1] = seconds remaining after those days
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        uptime="%i days %i hours %i minutes" % (days[0], hours[0], minutes[0])
        #uptime="%i days, %i hours, %i minutes, %i seconds" % (days[0], hours[0], minutes[0], minutes[1])
        # Create Status Text
        statustext="Uptime is " + str(uptime)
        # Set Check Result and Exit Code
        if r.json()["uptimeS"] < int(args.critical):
        	print("CRITICAL - " + statustext)
        	sys.exit(2)
        elif r.json()["uptimeS"] < int(args.warning):
            print("WARNING - " + statustext)
            sys.exit(1)
        elif r.json()["uptimeS"] > int(args.warning):
        	print("OK - " + statustext)
        	sys.exit(0)
        else:
            print("UNKNOWN - " + statustext)
            sys.exit(3)

    # no valid Type was defined
    case _:
        #print('The following Types are available: temperature, uptime')
        parser.print_help()
        sys.exit(3)

