#!/usr/bin/python

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

import os,sys,struct

#OV2 Format extract from: http://lists.gnumonks.org/pipermail/opentom/2005-November/000083.html
#Author:  Tor Arntsen tor at spacetec.no 

# Overview of OV2 Format:
#Byte zero is 2  (this indicates that the record is of "type 2" format)
#Next 4 bytes is the size of the (poi) record, in little endian format. 
# It shall include the length of this and the previous and following 
# fields. *)
#Next 4 bytes is longitude, little endian int, east-positive, divide by
# _LATLONG_MULTIPLIER.0 to get decimal format (e.g. 18.12345E is encoded as 1812345)
#Next 4 bytes is ditto for latitude north.
#Next follows a null-terminated string with the address (e.g. Gatwick Airport\0)

# Other type formats found in the TomTom SDK Manual

_CHARSET = 'cp1252'
_LATLONG_MULTIPLIER = 100000

def writeOV2(data, filename):
	file = open(filename, 'wb')

	typeBuf = struct.pack("<B",2)
	count = 0
	for poiset in data:
		uName = poiset[0] + '\0'
		name = uName.encode(_CHARSET)
		lat = poiset[1]
		long = poiset[2]
		
		latBuf = struct.pack("<i",int(lat*_LATLONG_MULTIPLIER))
		longBuf = struct.pack("<i",int(long*_LATLONG_MULTIPLIER))
		nameBuf = struct.pack("<%ss"%len(uName),name)
		nameLength = struct.calcsize("<%ss"%len(name))
		sizeBuf = struct.pack("<I",nameLength+13)
		
		file.write(typeBuf)
		file.write(sizeBuf)
		file.write(latBuf)
		file.write(longBuf)
		file.write(nameBuf)

		count += 1

	file.close()
	return count

def readOV2(filename):
	file = open(filename, 'rb')

	buf = "Data"
	data = set()
	type0s=0
	type1s=0
	while (buf != ""):
		buf = file.read(1)
		if (buf != ""):
			type = int(struct.unpack_from("<B",buf)[0])
			if (type == 0):
				#Deleted Record
				type0s+=1
				size = int(struct.unpack_from("<I",file.read(4))[0])
				file.read(size-5)
			elif (type == 1):
				#Proprietary Record
				type1s+=1
				file.read(20)
			elif (type == 2):
				#Normal Record
				size = int(struct.unpack_from("<I",file.read(4))[0])
				long = float(struct.unpack_from("<i",file.read(4))[0])/_LATLONG_MULTIPLIER
				lat= float(struct.unpack_from("<i",file.read(4))[0])/_LATLONG_MULTIPLIER
				namesize = size - 13;
				#Presuming a sane limit of 256 characters for the name length
				if namesize < 256:
					name = struct.unpack_from("<%ss"%namesize,file.read(namesize))[0]
					#Remove trailing terminating character
					#Remove any quotes and strip leading and trailing white space
					strippedname = name[0:-1].replace("\"","").strip()
					uName = unicode(strippedname,"cp1252")
					data.add((uName,lat,long))
			elif (type == 3):
				#Extended Record
				size = int(struct.unpack_from("<I",file.read(4))[0])
				long = float(struct.unpack_from("<i",file.read(4))[0])/_LATLONG_MULTIPLIER
				lat= float(struct.unpack_from("<i",file.read(4))[0])/_LATLONG_MULTIPLIER
				datasize = size - 13;
				#Presuming a sane limit of 256 characters for the name length
				if datasize < 256:
					databuffer = struct.unpack_from("<%ss"%datasize,file.read(datasize))[0]
					#The name is the text we want is up until a terminating character
					#Ignore the data after this character within this record block
					dataValues = databuffer.split('\0')
					#Remove any quotes and strip leading and trailing white space
					strippedname = dataValues[0].replace("\"","").strip()
					uName = unicode(strippedname,"cp1252")
					data.add((uName,lat,long))
			else:
				print "FATAL: OV2 Type %s Parsing Not Implemented (%s)" % (type,filename)
				print "Aborting"
				buf = ""
	if type0s > 1:
		print "INFO: %s OV2 Type 0 (Deleted Record) Ignored" % type0s
	if type1s > 1:
		print "INFO: %s OV2 Type 1 (Proprietary Records) Ignored" %type1s
	return data
	file.close()
	
if __name__ == '__main__':

	loadFilename = sys.argv[1]
	print "Reading %s" % loadFilename
	dataset = readOV2(loadFilename)

	for node in dataset:
		print "%s: %s,%s" % node

	#saveFilename = sys.argv[2]
	#print "Writing %s" % saveFilename
	#writeOV2(dataset,saveFilename)

	#print "Reading %s" % saveFilename 
	#savedDataset = readOV2(saveFilename)

	#for node in savedDataset:
		#print "%s: %s,%s" % node


