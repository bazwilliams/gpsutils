#!/usr/bin/python

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

import libigo8,codecs

aires = (
	"Parking.csv",
	"Services.csv",
	"Autoroutes.csv",
	"Campings.csv",
	"Autoroutes (Unverified).csv",
	"Parking (Unverified).csv",
	"Services (Unverified).csv",
	"Campings (Unverified).csv")

#Use the GARMIN-csv version
archies_file = "archies_europe.csv"

if __name__ == '__main__':
	datamap = dict()
	for filename in aires:
		poiset = set()
		input_file = codecs.open(filename,"r","cp1252")
		for line in input_file:
			row = line.split(",")
			latitude = row[1]
			longitude = row[0]
			name = row[2][1:-3]
			row = (name,latitude,longitude)
			poiset.add(row)
		datamap["Aires."+filename[0:-4]]=poiset;
		input_file.close()
	
	input_file = codecs.open(archies_file,"r","cp1252")
	poiset = set()
	for line in input_file:
		row = line.split(",")
		latitude = row[1]
		longitude = row[0]
		name = row[2][2:-3]
		row = (name,latitude,longitude)
		poiset.add(row)
	datamap["Archies Campings"]=poiset
	input_file.close()

	libigo8.createFile("user.poi",datamap)
