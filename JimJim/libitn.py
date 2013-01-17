#!/usr/bin/python

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

import codecs,os,sys

_CHARSET = 'cp1252'
_LATLONG_MULTIPLIER = 100000

def writeITN(data, filename):
	file = codecs.open(filename, 'w', _CHARSET)

	count = 0
	for itnset in data:
		lat = str(int((float(itnset[0])*_LATLONG_MULTIPLIER)))
		long = str(int((float(itnset[1])*_LATLONG_MULTIPLIER)))
		location = itnset[2]
		type = str(itnset[3])

		itnrow = "%s|%s|%s|%s|\n" % (lat,long,location,type)

		file.write(itnrow)

		count += 1

	file.close()
	return count

def readITN(filename):
	file = codecs.open(filename, 'r', _CHARSET)
	itinary = list()
	for line in file:
		itnrow = line.split('|')
		itinary.append((float(itnrow[0])/_LATLONG_MULTIPLIER, float(itnrow[1])/_LATLONG_MULTIPLIER, itnrow[2], float(itnrow[3])))
	return itinary
	
if __name__ == '__main__':

	loadFilename = sys.argv[1]
	print "Reading %s" % loadFilename
	dataset = readITN(loadFilename)

	saveFilename = sys.argv[2]
	print "Writing %s" % saveFilename
	count = writeITN(dataset,saveFilename)
	print "Written %s records" % count

	print "Reading %s" % saveFilename 
	savedDataset = readITN(saveFilename)

	for node in savedDataset:
		print "%s,%s: %s (%s)" % node


