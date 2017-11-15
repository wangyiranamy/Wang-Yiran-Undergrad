import zen
import csv
import sys
sys.path.append('../zend3js/')
import d3js
from acled_makeGraph import *

#Query user on what gml file to generate
selectYear = raw_input("Do you want to use all the data? Input Y/N\n")

if selectYear == "N":
	startYear = int(raw_input("Please input start year: (earliest possible is 1997)\n"))
	endYear = int(raw_input("Please input end year: (latest possible is 2015)\n"))
	selectYear = True
else:
	selectYear = False
	startYear = 0
	endYear = 0

selectByFatality = int(raw_input("Do you want to weigh the edges by count of events or fatalities? 1 for events, 2 for fatalities\n"))


#Reminder: Put the .csv source file in the SAME folder as this .py file

myGraph = makeGraph(selectYear,selectByFatality,startYear,endYear)

## ====================== Writing the .gml File ======================
## File will be created in the current working directory
fileName = "ACLED_Graph"
if int(selectByFatality)==1:
	fileName += "_Events"
else:
	fileName += "_Fatalities"

if selectYear:
	fileName += "_" + str(startYear) + "_" + str(endYear)

fileName += ".gml"

zen.io.gml.write(myGraph, fileName)
print "GML file with the name", fileName, "has been created."



