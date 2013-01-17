#!/bin/sh

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

GPS_SCRIPT=/home/barry/scripts/gps_info.py

while true; do
	if [ -f /tmp/gpsd.pid ]
	then
		STATUS=`python $GPS_SCRIPT status`

		# If the GPS has a fix then update the current location
		if [ "$STATUS" = "2D Fix" ] || [ "$STATUS" = "3D Fix" ]
		then
			python $GPS_SCRIPT latitude > /tmp/GPS_LATITUDE
			python $GPS_SCRIPT longitude > /tmp/GPS_LONGITUDE
			/home/barry/scripts/distance.sh > /tmp/GPS_DISTANCE
		fi
	
		if [ "$STATUS" != "Offline" ]
		then
			python $GPS_SCRIPT numsatellites > /tmp/GPS_NUMSATS	
		fi
	else
		STATUS="No GPSD"
		echo "" > /tmp/GPS_NUMSATS
	fi

	if [ ! -f /tmp/GPS_DISTANCE ]
	then
		/home/barry/scripts/distance.sh > /tmp/GPS_DISTANCE
	fi

	echo "$STATUS" > /tmp/GPS_STATUS
	
	sleep 10
done
