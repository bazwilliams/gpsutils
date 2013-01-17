#!/usr/bin/python

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

import codecs

def printUserPOIRow(index,category,name,latitude,longitude):
	#Format of the user.poi file is a UTF-16 encoded text file with rows following this format:
	#INDEX|CATEGORY.SUBCATEGORY|NAME||DECIMAL_LAT|DECIMAL_LONG|||||ADDRESS1|ADDRESS2||INFORMATION|TELEPHONE
	rowtext = "%s|%s|%s||%s|%s|||||||%s|\n" % (str(index),category,name.replace("|",":"),latitude,longitude,name.replace("|",":"))
	return rowtext

class igo8poi:
        datamap = dict()

        #categoryname - the category name of this poiset
        #poiset - a set of lists each with the following format:  (NAME, LAT, LONG)
        #          [ (NAME0, LAT0, LONG0) , (NAME1, LAT1, LONG1) , ... ]
        def add(self, categoryname, poiset):
                self.datamap[categoryname] = poiset
                
        #filename - the name of the file to write to (e.g. user.poi)
        def createFile(self, filename):
                if len(self.datamap) > 0:
                        output = codecs.open(filename,"wb","utf-16")
                        index=0
	
                        for category in self.datamap.keys():
                                for row in self.datamap[category]:
                                        rowtext = printUserPOIRow(index,category,row[0],row[1],row[2])
                                        output.write(rowtext)
                                        index+=1

                        print ("%s POIs added to %s" % (str(index),output.name))
                        output.close()
                else:
                        print ("No POIs added")
