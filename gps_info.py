# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

import gps,sys,math,liblatlong

# Courtesy of http://www.perrygeo.net/wordpress/?p=13

session = gps.gps()

session.query('xadmosyqp')
# a = altitude, d = date/time, m=mode,
# o=postion/fix, s=status, y=satellites

for arg in sys.argv:
	print arg
	if arg == 'status':
		if session.status == gps.STATUS_FIX:
			print ("ZERO","No Fix","2D Fix","3D Fix")[session.fix.mode]
		else:
			print "No Fix"
	if arg == 'latitude':
		print session.fix.latitude
	if arg == 'longitude':
		print session.fix.longitude
	if arg == 'time utc':
		print session.utc, session.fix.time
	if arg == 'altitude':
		print session.fix.altitude
	if arg == 'speed':
		print session.fix.speed
	if arg == 'numsatellites':
		print str(session.satellites_used),'/',str(len(session.satellites))
	if arg == 'session':
		print session
	if arg == 'distance':
		dist = liblatlong.distance(session.fix.latitude,session.fix.longitude,55.847033,-4.108464)
		print str(round(dist)),'miles'

del session
