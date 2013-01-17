# Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

import sys,math

a1 = math.radians(float(sys.argv[1]))
b1 = math.radians(float(sys.argv[2]))
a2 = math.radians(float(sys.argv[3]))
b2 = math.radians(float(sys.argv[4]))

radius = 3963.1676

# Taken from http://www.mathforum.com/library/drmath/view/51711.html

x = math.cos(a1) * math.cos(b1) * math.cos(a2) * math.cos(b2)
y = math.cos(a1) * math.sin(b1) * math.cos(a2) * math.sin(b2)
z = math.sin(a1) * math.sin(a2)

distance = math.acos(x+y+z) * radius
		
print str(round(distance,1)),'miles'
