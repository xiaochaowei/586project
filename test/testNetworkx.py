import argparse
import json
from edmonds import Matching
import pickle
import time
import networkx as nx

# import resource, sys
# resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
# sys.setrecursionlimit(10**7)

parser = argparse.ArgumentParser()
parser.add_argument('graph', help='input graph pickle file')
args = parser.parse_args()

G = pickle.load(open(args.graph,'r'))

start = time.time()
mates = nx.max_weight_matching(G)

print "[Networkx] %s takes %s seconds" % (args.graph, time.time() - start)
total = 0
for u, v in mates.items():
	total+= G[u][v]['weight']
total = total / 2
print "[Networkx] max matching: %d" % total
