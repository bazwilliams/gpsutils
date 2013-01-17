#!/usr/bin/python

# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

import sys,libigo8,libov2

if __name__ == '__main__':

	igo8poi = libigo8.igo8poi()

	if sys.argv > 1:
		for filename in sys.argv[1:]:
			print "Reading %s" % filename
			dataset = libov2.readOV2(filename)
			(d,f) = filename.split("/")
			igo8poi.add("%s.%s"%(d,f[0:-4]),dataset)

		igo8poi.createFile("user.poi")
