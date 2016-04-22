# Test scripts
from edmonds import Matching as MatchingOn3
# import ed 
from test3 import Matching as MatchingBase

import networkx as nx
import random

# generate a random weighted graph gener
def get_random_weighted_graph(n, p=0.5, max_weight=10):
	print "n=%d, p=%f, max_weight=%d" % (n, p, max_weight)
	G = nx.fast_gnp_random_graph(n, p)
	for e in G.edges():
		G[e[0]][e[1]]['weight'] = random.randint(1, max_weight)
	# print list(G.edges(data='weight', default=1))
	return G

def test():
	G = get_random_weighted_graph(random.randint(5, 10),
		random.random(), random.randint(1, 10000))
	edge_list = list(G.edges(data='weight', default=1))
	passed = True     # pass the test?

	# correct answer
	mates = nx.max_weight_matching(G)
	correct = 0
	for u, v in mates.items():
		correct += G[u][v]['weight']
	assert (correct % 2 == 0)
	correct = correct / 2

	# This is our baseline
	match1 = MatchingBase()
	match1.initEdges(edge_list)
	test_answer1 = match1.maxWeightmatching()
	total = 0
	for u, v in enumerate(test_answer1):
		if v != -1:
			total += G[u][v]['weight']
	total = total / 2
	if (total != correct):
		passed = False
		print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
		print "Baseline: "
		print ";;", edge_list
		print ";;;;", test_answer1
		print ";;;;;;", mates
		print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

	# This is an O(n^3) improved version
	match2 = MatchingOn3()
	match2.initEdges(edge_list)
	test_answer2 = match2.maxWeightmatching()
	# test_answer2 = ed.maxWeightMatching(edge_list)
	total = 0
	for u, v in enumerate(test_answer2):
		if v != -1:
			total += G[u][v]['weight']
	total = total / 2
	if (total != correct):
		passed = False
		print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
		print "O(n^3): correct -> %d, tested -> %d" % (correct, total)
		print ";;", edge_list
		print ";;;;", test_answer2
		print ";;;;;;", mates
		print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
	return passed

# generate 1000 random graph
if __name__ == "__main__":
	num_tests = 10000
	num_failed = 0
	for i in range(num_tests):
		passed = test()
		if not passed:
			num_failed += 1
			break
		else:
			print "test %d passed" % (i+1)
	print "num tested: %d, num failed: %d" % (num_tests, num_failed)
