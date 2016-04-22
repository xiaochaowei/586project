# Test scripts
# from edmonds import Matching as MatchingOn3
# # import ed 
# from test3 import Matching as MatchingBase

from greedymatching import greedyApproMatching
from randommatching import random_Matching 
from scaling import Matching

import networkx as nx
import random
import time
skip_scale = 0
error_scale = 0
error_greed = 0
error_randm = 0
timedelta = 0
# generate a random weighted graph gener
def get_random_weighted_graph(n, p=0.5, max_weight=500):
	# print "n=%d, p=%f, max_weight=%d" % (n, p, max_weight)
	if p < 0.1:
		p = 0.1
	G = nx.fast_gnp_random_graph(n, p)
	for e in G.edges():
		G[e[0]][e[1]]['weight'] = random.randint(1, max_weight)
	# print list(G.edges(data='weight', default=1))
	return G

def test(vertex_num, weight,scale_num= 1/16.0):
	global skip_scale, error_scale, error_greed, error_randm
	G = get_random_weighted_graph(vertex_num, random.random(), 2**weight)
	#G = get_random_weighted_graph(random.randint(10, 50),
	#	random.random(), 2 ** random.randint(1, 10))
	edge_list = list(G.edges(data='weight', default=1))
	# for e in G.edges(data='weight'):
	# 	edge_list.append((e[0],e[1],e[2]['weight']))

	# correct answer
	mates = nx.max_weight_matching(G)
	correct = 0
	for u, v in mates.items():
		correct += G[u][v]['weight']
	assert (correct % 2 == 0)
	correct = correct / 2

	# This is Scaling algorithm
	scale= Matching()
	scale.initEdges(edge_list)
	try:
		re = scale.maxWeightmatching(scale_num)
		scale_ans = 0		
		for u, v in enumerate(re):
			if v != -1:
				scale_ans += G[u][v]['weight']
		scale_ans = scale_ans / 2
		error_scale += (abs(correct - scale_ans) * 1.0 / correct)
	except:
	#	print "error scale"
		skip_scale += 1
	greed = greedyApproMatching(edge_list)
	greed_ans = 0
	for u, v in enumerate(greed):
		if v != -1:
			greed_ans += G[u][v]['weight']
	greed_ans = greed_ans / 2		
	randm = random_Matching(edge_list)
	randm_ans = 0
	for u, v in enumerate(randm):
		if v != -1:
			randm_ans += G[u][v]['weight']
	randm_ans = randm_ans / 2
	error_greed += (abs(correct - greed_ans) * 1.0 / correct)
	error_randm += (abs(correct - randm_ans) * 1.0 / correct)
def test2(scale_num= 1/16.0):
	global skip_scale, error_scale, error_greed, error_randm
	# G = get_random_weighted_graph(vertex_num, random.random(), 2**weight)
	G = get_random_weighted_graph(random.randint(10, 50),
		random.random(), 2 ** random.randint(1, 10))
	edge_list = list(G.edges(data='weight', default=1))
	# for e in G.edges(data='weight'):
	# 	edge_list.append((e[0],e[1],e[2]['weight']))

	# correct answer
	mates = nx.max_weight_matching(G)
	correct = 0
	for u, v in mates.items():
		correct += G[u][v]['weight']
	assert (correct % 2 == 0)
	correct = correct / 2

	# This is Scaling algorithm
	scale= Matching()
	scale.initEdges(edge_list)
	try:
		global timedelta 
		start = time.clock()
		re = scale.maxWeightmatching(scale_num)
		end_time = time.clock()
		timedelta = timedelta + (end_time - start)
		scale_ans = 0		
		for u, v in enumerate(re):
			if v != -1:
				scale_ans += G[u][v]['weight']
		scale_ans = scale_ans / 2
		error_scale += (abs(correct - scale_ans) * 1.0 / correct)
	except Exception,e:
		print e
		print "error scale"
		skip_scale += 1
	# greed = greedyApproMatching(edge_list)
	# greed_ans = 0
	# for u, v in enumerate(greed):
	# 	if v != -1:
	# 		greed_ans += G[u][v]['weight']
	# greed_ans = greed_ans / 2		
	# randm = random_Matching(edge_list)
	# randm_ans = 0
	# for u, v in enumerate(randm):
	# 	if v != -1:
	# 		randm_ans += G[u][v]['weight']
	# randm_ans = randm_ans / 2
	# error_greed += (abs(correct - greed_ans) * 1.0 / correct)
	# error_randm += (abs(correct - randm_ans) * 1.0 / correct)

# generate 1000 random graph
def save(matrix, filename):
	fid = open(filename, 'w')
	for i in range(0,len(matrix[0])):
		for j in range(len(matrix)):
			fid.write(str(matrix[j][i]))
			fid.write(" ")
		fid.write("\n")
	fid.close()

if __name__ == "__main__":

	num_tests = 200
	num_failed = 0
	result1 = [[] for i in range(0,3)]
	result2 = [[]for i in range(0,3)]
	result3 = [[]for i in range(0,2)]
	
	for j in range(20,200,10):
		error_scale = 0
		error_greed = 0
		error_randm = 0
		skip_scale = 0
		for i in range(num_tests):
			passed = test(j,10)
		result1[0].append(error_scale *1.0 / (num_tests - skip_scale))
		result1[1].append(error_greed * 1.0 / num_tests)
		result1[2].append(error_randm * 1.0 / num_tests)
	save(result1, "result1.txt")
		# print "error scale,",j," %f" % (error_scale * 1.0 / (num_tests - skip_scale))
		# print "error greed",j," %f" % (error_greed * 1.0 / num_tests)
		# print "error randm",j," %f" % (error_randm * 1.0 / num_tests)
	for j in range(2,10,1):
		error_scale = 0
		error_greed = 0
		error_randm = 0
		skip_scale = 0
		for i in range(num_tests):
			passed = test(50, j)
		result2[0].append( error_scale *1.0 / (num_tests - skip_scale)	)
		result2[1].append( error_greed * 1.0 / num_tests)
		result2[2].append(error_randm * 1.0 / num_tests)
	save(result2, "result2.txt")
		# print "error scale",j," %f" % (error_scale * 1.0 / (num_tests - skip_scale))
		# print "error greed",j," %f" % (error_greed * 1.0 / num_tests)
		# print "error randm",j," %f" % (error_randm * 1.0 / num_tests)
	for j in range(2,8):
		scale_num = 1.0 / 2**j
		error_scale = 0
		error_greed = 0
		error_randm = 0
		skip_scale = 0
		timedelta = 0
		for i in range(num_tests):
			passed = test2(j)

		result3[0].append( timedelta / (num_tests - skip_scale))
		result3[1].append(error_scale * 1.0 /(num_tests - skip_scale))
	save(result3, "result3.txt")
