#!/bin/sh

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

HOME_LAT=55.847033
HOME_LONG=-4.108464

if [ -f /tmp/GPS_LATITUDE ] && [ -f /tmp/GPS_LONGITUDE ]
then
	CUR_LAT=`cat /tmp/GPS_LATITUDE`
	CUR_LONG=`cat /tmp/GPS_LONGITUDE`
	python /home/barry/scripts/distance.py $HOME_LAT $HOME_LONG $CUR_LAT $CUR_LONG
else
	echo "Unknown"
fi

