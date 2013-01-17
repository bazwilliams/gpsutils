#!/bin/sh

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

GPS_SCRIPT=/home/barry/scripts/gps_info.py

if [ -f /tmp/gpsd.pid ]
then
#	LASTVALID=`python $GPS_SCRIPT valid`
#	if [ -f /tmp/GPS_LAST_SENTENCE ]
#	then
#		PREV_SENTENCE=`cat /tmp/GPS_VALID`
#		if [ "$PREV_SENTENCE" = $LASTVALID ]
#		then
#			STATUS="Offline"
#		else
			STATUS=`python $GPS_SCRIPT status`
#		fi
#	fi
#	echo $LASTVALID > /tmp/GPS_VALID

	if [ "$STATUS" != "Offline" ]
	then
		case $1 in
			"distance")
				if [ "$STATUS" = "2D Fix" ] || [ "$STATUS" = "3D Fix" ]
				then
					DISTANCE=`python $GPS_SCRIPT distance`
					echo $DISTANCE > /tmp/GPS_DISTANCE
				fi
	
				if [ -f /tmp/GPS_DISTANCE ]
				then
					cat /tmp/GPS_DISTANCE
				fi
			;;
			**)
				python $GPS_SCRIPT $1
			;;
		esac
	fi
else
	STATUS="No GPSD"
fi

if [ "$1" = "status" ]
then
	echo $STATUS
fi
