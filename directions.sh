#!/bin/sh

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

LAT=`python /home/barry/scripts/gps_info.py latitude`
LONG=`python /home/barry/scripts/gps_info.py longitude`

QUERY=`zenity --entry --text="What are you looking for?" --title="Google Maps Search"`

URL="http://maps.google.co.uk/maps?f=d&source=s_d&saddr=${LAT},${LONG}&daddr=${QUERY}&hl=en&mrcr=0&ie=UTF8&ll=${LAT},${LONG}&z=14"

xdg-open $URL

