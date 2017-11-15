import zen
import matplotlib.pyplot as plt  	# if matplotlib doesn't work comment this line out
plt.ioff()							# if matplotlib doesn't work comment this line out
from numpy import *
import sys
sys.path.append('../zend3js/')
import d3js
from time import sleep
import random
from acled_makeGraph import *
sourceFile = "acled-all-clean-hell.csv"
import pprint


### SET THE GRAPH HERE =====================================
# The other graph is: 'ACLED_Graph_Fatalities.gml'
gml_file = 'ACLED_Graph_Events.gml'
G = zen.io.gml.read(gml_file, weight_fxn=lambda x:x['weight'])

#G = makeGraph("N",2,2005,2005)


### Introductory calculations ===============================
print "Number of nodes:", G.num_nodes
print "Number of edges:", G.num_edges
print "Diameter:", 

D,P = zen.algorithms.shortest_path.all_pairs_shortest_path_(G)
D1 = ma.masked_invalid(D)
print nanmax(D1)

### Degree/Eigenvector centralities calculation
print "\n===================================\nCentrality Calculations:"

# prints the top five (num) nodes according to the centrality vector v
# v takes the form: v[nidx] is the centrality of node with index nidx
def print_top(G,v, num=5):
	idx_list = [(i,v[i]) for i in range(len(v))]
	idx_list = sorted(idx_list, key = lambda x: x[1], reverse=True)
	for i in range(min(num,len(idx_list))):
		nidx, score = idx_list[i]
		print '  %i. %s (%1.4f)' % (i+1,G.node_object(nidx),score)
		#print '  %i. %s' % (i+1,G.node_object(idx))

# returns the index of the maximum of the array
# if two or more indices have the same max value, the first index is returned
def index_of_max(v):
	return where(v == max(v))[0]
	
print '\nDegree Centrality:'
G.compact()
v = [A[i].sum() for i in range(N)] 
print_top(G, v, num=20)

# Eigenvector Centrality
print '\nEigenvector Centrality (by Zen):'
v = zen.algorithms.centrality.eigenvector_centrality_(G, weighted=True)
print_top(G, v, num=20)


## Plots the degree distribution and calculates the power law coefficent
def calc_powerlaw(G, kmin):
	ddist = zen.degree.ddist(G,normalize=False)
	
	#v = [A[i].sum() for i in range(N)] 
	#H=histogram(v, bins=max(v)-1)
	#ddist = H[0]

	cdist = zen.degree.cddist(G,inverse=True)
	k = arange(len(ddist)) #numpy.arange returns an array. Similar to range()
	
	# *******************************************
	# if matplotlib doesn't work comment this section out
	plt.figure(figsize=(8,12))
	plt.subplot(211)
	plt.bar(k, ddist, width=0.8, bottom=0, color='b')
	
	plt.subplot(212)
	plt.loglog(k, cdist)
	plt.hold(True)
	plt.plot([kmin, kmin], [0.00001, 1])
	plt.hold(False)

	# *******************************************
	# if matplotlib doesn't work, use this instead to export values to excel for plotting
	# list2csv(ddist,'filename.csv')
	
	N = float(G.num_nodes) * cdist[kmin] # number of nodes with degree greater than or equal to k_min
	
	sum_term = 0
	
	for node in G.nodes():
	    if G.degree(node) >= kmin:
	        sum_term += log(G.degree(node)/(kmin-0.5))
	
	alpha = 1 + N/sum_term # calculate using (8.6)!
	sigma = (alpha - 1) / sqrt(N) # calculate using (8.7)!
	print '%1.2f +/- %1.2f' % (alpha,sigma)
	#print '%i, %1.2f,  %1.2f' % (kmin, alpha,sigma)
	plt.show()


### FIND COMPONENTS ========================================
components = zen.algorithms.components(G)   # returns a list of components, each component is a (set) of nodes in the component

component_sizes = [len(component) for component in components]
print "\n===================================\nComponent Calculations:"
print "Size of largest component:" , max(component_sizes)
print "Total number of nodes:", G.num_nodes
print max(component_sizes)/float(G.num_nodes)
component_sizes.sort()
print component_sizes



## Modularity calculations ========================
#This function adds an edge if not present, adds weight if edge is present:
def add_weight(G,nodeA,nodeB,myValue):
	if G.has_edge(nodeA,nodeB):
		myWeight = G.weight(nodeA,nodeB)+myValue
		G.set_weight(nodeA,nodeB,myWeight)
	else:
		G.add_edge(nodeA,nodeB,weight=myValue)

### Following code prepares a dictionary of actor category values for later use
class_Dict = {}
with open(sourceFile) as mycsv:
	reader = csv.DictReader(mycsv)
	for row in reader:
		if row['ACTOR1'] in class_Dict:
			pass
		else:
			class_Dict[row['ACTOR1']]=row['INTER1']
		
		if row['ACTOR2'] in class_Dict:
			pass
		else:
			class_Dict[row['ACTOR2']]=row['INTER2']
		
		#if not (row['ACTOR1'] in class_Dict[int(row['INTER1'])] ):
		    #class_Dict[int(row['INTER1'])].append(row['ACTOR1'])
		
		#if not (row['ACTOR2'] in class_Dict[int(row['INTER2'])] ):
		    #class_Dict[int(row['INTER2'])].append(row['ACTOR2'])

### Following modularity function is adapted from Module 4
def modularity(G,c):
	d = dict()
	for k,v in c.iteritems(): # for Key 'k' and Value 'v' in the dictionary 'c'
		for n in v: # for each node in the group 'k',
			d[n] = k # assign a group to the node 'n'
			# 'd' now becomes a dictionary {node1: class1, node2: class2 ...}
	
	Q, Qmax = 0,1
	
	# for all pairs of nodes,
	for u in G.nodes_iter():
		for v in G.nodes_iter():		    
			if d[u] == d[v]: # if the two nodes belong in the same class,
			    
			    # int(True) = 1, int(False) = 0
				Q += ( int(G.has_edge(v,u)) - G.degree(u)*G.degree(v)/(2*float(G.num_edges)) )/ (2*float(G.num_edges))
				Qmax -= ( G.degree(u)*G.degree(v)/(2*float(G.num_edges)) )/(2*float(G.num_edges))
	return Q, Qmax


def size_of_Dict(myDict):
	myCount = 0
	for key in myDict:
		myCount += len(myDict[key])
	return myCount

### Generating the actual class dictionaries for use
new_class_dict = {}
for i in range(1,9):
	new_class_dict[i] = []

for myNode in G.nodes():
	if int(class_Dict[myNode])==8:
		G.rm_node(myNode)
	else:
		new_class_dict[int(class_Dict[myNode])].append(myNode)

### Now for actual modularity calculations
print "\n=====================\nModularity calculations"

testQ = zen.algorithms.modularity(G, new_class_dict, weighted=False)
Q, Qmax = modularity(G,new_class_dict)
print testQ
print Q
print 'Modularity (Countries): %1.4f / %1.4f' % (Q,Qmax)
print 'Normalised Modularity:', Q/Qmax


# POWER LAW ==============================================
print "\n=====================\nPower law calculations"
calc_powerlaw(G, 0)  # need to change kmin appropriately
