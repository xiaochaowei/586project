def greedyApproMatching(edges):
	edges.sort(key = lambda tup: tup[2], reverse=True)
	# print edges
	nvertex = -1
	for (i, j, w) in edges:
		assert i >= 0 and j >= 0 and i != j
		if i >= nvertex:
			nvertex = i + 1
		if j >= nvertex:
			nvertex = j + 1
	mate = [-1] * nvertex
	for (i,j,w) in edges:
		if mate[i] == -1 and mate[j] == -1:
			mate[i] = j
			mate[j] = i
	return mate

# def ApproMatching(edges):

import networkx as nx
import pickle
G = pickle.load(open('data/geometric_n1000_e21506.p','r'))
result = greedyApproMatching(list(G.edges(data='weight', default=1)))
total = 0
for u, v in enumerate(result):
	if v != -1:
		total += G[u][v]['weight']
total = total / 2
print total
