def greedyApproMatching(edges):
	edges.sort(key = lambda tup: tup[2])
	edges = edges.reverse()
	nvertex = -1
	for (i, j, w) in edges:
		assert i >= 0 and j >= 0 and i != j
		if i >= nvertex:
			nvertex = i + 1
		if j >= nvertex:
			nvertex = j + 1
    mate = [-1] * nvertex
	for (i,j,w) in range(0, len(edges)):
		if mate[i] == -1 and mate[j] == -1:
			mate[i] = j
			mate[j] = i

def ApproMatching(edges):
	