import argparse
import json
from scaling import Matching
import pickle
import time

import resource, sys
# resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
# sys.setrecursionlimit(10**7)

parser = argparse.ArgumentParser()
parser.add_argument('graph', help='input graph pickle file')
args = parser.parse_args()

G = pickle.load(open(args.graph,'r'))
match = Matching()
edge_list = list(G.edges(data='weight', default=1))
# for e in G.edges(data='weight'):
# 	edge_list.append((e[0],e[1],e[2]['weight']))	
match.initEdges(edge_list)
print "start"
start = time.time()
result = match.maxWeightmatching(1/16.0)

print "[Scale] %s takes %s seconds" % (args.graph, time.time() - start)
total = 0
for u, v in enumerate(result):
	if v != -1:
		total += G[u][v]['weight']
total = total / 2
print "[Scale] max matching: %d" % total
