#!/usr/bin/python

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

import libigo8,codecs

#CSV File to load
csv_file = "poi.csv"
#cp1252 is the default codepage/encoding for Windows ASCII files
character_set = "cp1252"

if __name__ == '__main__':

	igo8poi = libigo8.igo8poi()

	poiset = set()
	input_file = codecs.open(csv_file,"r",character_set)
	for line in input_file:
		row = line.split(",")
		latitude = row[1]
		longitude = row[0]
		name = row[2][1:-3]
		row = (name,latitude,longitude)
		poiset.add(row)

	igo8poi.add(csv_file,poiset);
	input_file.close()
	
	igo8poi.createFile("user.poi")
