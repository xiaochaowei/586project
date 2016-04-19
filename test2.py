# whole process
class Graph:
    def __init__(self):
        self.nvertex = 0
        self.nedge = 0
        self.max_weight = -1
        self.neighbor = None
        self.edges = None
        self.endpoint = None

    def addEdges(self, edges):
        self.nvertex = -1
        for (i, j, w) in edges:
            if i > self.nvertex:
                self.nvertex = i
            if j > self.nvertex:
                self.nvertex = j
        self.nvertex = self.nvertex + 1
        self.edges = edges
        self.nedge = len(self.edges)
        self.endpoint = [self.edges[p // 2][p % 2] for p in range(0, 2 * self.nedge)]
        self.neighbor = [[] for i in range(self.nvertex)]
        for k in range(self.nedge):
            (i, j, w) = self.edges[k]
            if w > self.max_weight:
                self.max_weight = w
            self.neighbor[i].append(2 * k + 1)
            self.neighbor[j].append(2 * k)

    def getAdjacent(self, i):
        return self.neighbor[i]


class Node:
    def __init__(self, id, max_weight=0):
        self.label = 0
        self.inblossom = id  #top-level blossom
        self.parent = -1
        self.dualVar = max_weight
        self.id = id
        self.father = -1
        self.base = id
        self.children = None
        self.endps = None
        self.bestedge = -1
        self.blossombestedges = None

    def create(self):
        self.base = -1
        self.inblossom = -1

    # def addBlossom(self, i):
    # 	self.inblossom = i
    # def addMate(self, i):
    # 	self.mate = i
    # def __eq__(self, node2):
    # 	if node1.idx == node2.idx:
    # 		return True
    # 	else:
    # 		return False
    # def __neq__(self, node2):
    # 	if node1.idx != node2.idx:
    # 		return True
    # 	else:
    # 		return False


class Matching:
	def initEdges(self, edges):
	    self.graph = Graph()
	    self.graph.addEdges(edges)
	    self.edges = self.graph.edges
	    self.nvertex = self.graph.nvertex
	    self.nedges = self.graph.nedge
	    self.endpoint = self.graph.endpoint
	    self.nvertex = self.graph.nvertex
	    self.nodeList = [None for i in range(0, 2 * self.nvertex)]
	    self.queue = []  #worklist
	    #improve
	    self.mate = self.nvertex * [-1]
	    self.unusedblossomId = range(self.nvertex, self.nvertex * 2)
	    self.allowedge = []

	def cleanData(self):
		#Romove label
		self.queue[:] = []
		self.allowedge[:] = self.nedges * [False]
		for i in range(0, self.nvertex * 2):
			if self.nodeList[i] == None:
				continue
			assert self.nodeList[i] != None
			self.nodeList[i].bestedge = -1
			self.nodeList[i].label = 0
			if i >= self.nvertex:
				self.nodeList[i].blossombestedges = None

	def maxWeightmatching(self, maxcardinality=False):
	    nvertex = self.nvertex
	    max_weight = self.graph.max_weight
	    nodeList = self.nodeList
	    for idx in range(0, nvertex):
	        if nodeList[idx] == None:
	            nodeList[idx] = Node(idx, 2 * max_weight)

	    #Main Loop
	    for t in range(0, nvertex):
	        self.cleanData()
	        #label
	        for v in range(0, nvertex):
	            if self.mate[v] == -1 and nodeList[v].label == 0:
	                self.assignLabel(v, 1, -1)

	        augmented = 0
	        while 1:

	            while self.queue and not augmented:
	                v = self.queue.pop()
	                v = self.nodeList[v]
	                assert nodeList[v.inblossom].label == 1
	                neighbor = self.graph.getAdjacent(v.id)
	                for p in neighbor:
	                    k = p // 2
	                    w = self.endpoint[p]
	                    adjacent_node = nodeList[w]

	                    if v.inblossom == adjacent_node.inblossom:
	                        continue

	                    if not self.allowedge[k]:
	                        kslack = self.slack(k)
	                        if kslack <= 0:
	                            self.allowedge[k] = True
	                    if self.allowedge[k]:
	                        #case1 outer unlabel
	                        if nodeList[adjacent_node.inblossom].label == 0:
	                            self.assignLabel(w, 2, p ^ 1)

	                        elif nodeList[adjacent_node.inblossom].label == 1:
	                            base = self.scanBlossom(v.id, w)

	                            #case2 outer outer no same root  -> augmenting_path
	                            if base == -1:
	                                #finding augumenting path
	                                self.augmentMatching(k)
	                                augmented = 1
	                                break
	                            #case3 outer same root -> blossom
	                            else:
	                                #blossom
	                                self.addBlossom(base, k)

	                        elif adjacent_node.label == 0:
	                            adjacent_node.label = 2
	                            adjacent_node.parent = p ^ 1
	                    elif self.nodeList[self.nodeList[w].inblossom].label == 1:
	                        b = self.nodeList[v.id].inblossom
	                        if self.nodeList[b].bestedge == -1 or kslack < self.slack(self.nodeList[b].bestedge):
	                            self.nodeList[b].bestedge = k
	                    elif self.nodeList[w].label == 0:
	                        if nodeList[w].bestedge == -1 or kslack < self.slack(self.nodeList[w].bestedge):
	                            nodeList[w].bestedge = k
	            if augmented == 1:
	                break
	            deltatype = -1
	            delta = deltaedge = deltablossom = None
	            #dual adjustment
	            #delta 1
	            if not maxcardinality:
	                deltatype = 1
	                delta = min([i.dualVar for i in self.nodeList[:self.nvertex] if i != None])
	            #delta 2
	           	for v in range(self.nvertex):
	           		node = self.nodeList[v]
	           		if node == None:
	           			continue
	           		if self.nodeList[node.inblossom].label == 1:
	           			#find the neighbor and update;
	           			neighbor = self.graph.getAdjacent(node.id)
	           			for p in neighbor:
	           				k = p // 2
	           				w = self.endpoint[p]
	           				adjacent_node = nodeList[w]
	           				if adjacent_node.inblossom == node.inblossom:
	           					continue
	           				elif adjacent_node.label == 0:
	           					d = self.slack(k)
		           				if deltatype == -1 or d < delta:
		           					delta = d
		           					deltaedge = k
		           					deltatype = 2


		        #delta 3
		        for v in range(self.nvertex ):
		        	node = self.nodeList[v]
		        	if node == None:
		        		continue
		        	if self.nodeList[node.inblossom].label == 1:
		        		neighbor = self.graph.getAdjacent(node.id)
		        		for p in neighbor:
		        			k = p//2
		        			w = self.endpoint[p]
		        			adjacent_node = nodeList[w]
		        			if adjacent_node.inblossom == node.inblossom:
		        				continue
		        			elif self.nodeList[adjacent_node.inblossom].label == 1:
		        				d = self.slack(k)
		        				d = d /2 
		        				if deltatype == -1 or d < delta:
		        					deltatype = 3
		        					delta = d
		        					deltaedge = k
		        #delta 3 
		        for v in range(self.nvertex, 2 * self.nvertex):
		        	node = self.nodeList[v]
		        	if node == None:
		        		continue
		        	if node.base >= 0 and node.father == -1 and node.label == 2 \
		        		and (deltatype == -1 or node.dualVar < delta):
		        		deltatype = 4
		        		delta = node.dualVar
		        		deltablossom = v


  			   	# #delta 2
	        #     for v in range(self.nvertex):
	        #         node = self.nodeList[v]
	        #         if node == None:
	        #             continue
	        #         if node.label == 0 and node.bestedge != -1:
	        #             d = self.slack(node.bestedge)
	        #             if deltatype == -1 or d < delta:
	        #                 delta = d
	        #                 deltatype = 2
	        #                 deltaedge = node.bestedge
	        #     #delta3
	        #     for b in range(2 * self.nvertex):
	        #         node = self.nodeList[b]
	        #         if node == None:
	        #             continue
	        #         if (node.father == -1 and node.label == 1 and node.bestedge != -1):
	        #             kslack = self.slack(node.bestedge)
	        #             d = kslack / 2
	        #             if deltatype == -1 or d < delta:
	        #                 delta = d
	        #                 deltatype = 3
	        #                 deltaedge = node.bestedge
	        #     #delta 4
	        #     for b in range(self.nvertex, 2 * self.nvertex):
	        #         node = self.nodeList[b]
	        #         if node == None:
	        #             continue
	        #         if (node.base >= 0 and node.father == -1 and node.label == 2 \
	        #                     and (deltatype == -1 or node.dualVar < delta)):
	        #             deltatype = 4
	        #             delta = node.dualVar
	        #             deltablossom = b

	            if deltatype == -1:
	                assert maxcardinality
	                deltatype = 1
	                delta = max(0, min([i.dualVar for i in self.nodeList[:self.nvertex]]))

	            for v in range(self.nvertex):
	                node = self.nodeList[v]
	                if node == None:
	                    continue
	                if self.nodeList[node.inblossom].label == 1:
	                    node.dualVar -= delta
	                elif self.nodeList[node.inblossom] == 2:
	                    node.dualVar += delta
	            for b in range(self.nvertex, 2 * self.nvertex):
	                node = self.nodeList[b]
	                if node == None:
	                    continue
	                if node.base >= 0 and node.parent == -1:
	                    if node.label == 1:
	                        node.dualVar += delta
	                    elif node.label == 2:
	                        node.dualVar -= delta
	            if deltatype == 1:
	                break
	            elif deltatype == 2:
	                self.allowedge[deltaedge] = True
	                (i, j, wt) = self.edges[deltaedge]
	                if self.nodeList[self.nodeList[i].inblossom].label == 0:
	                    i, j = j, i
	                assert self.nodeList[self.nodeList[i].inblossom].label == 1
	                self.queue.append(i)
	            elif deltatype == 3:
	                self.allowedge[deltaedge] = True
	                (i, j, wt) = self.edges[deltaedge]
	                self.queue.append(i)
	            elif deltatype == 4:
	                self.expandBlossom(deltablossom, False)
	        if not augmented:
	            break

	        for b in range(self.nvertex, 2 * self.nvertex):
	            if not self.nodeList[b]:
	                continue
	            node = self.nodeList[b]
	            if (node.father == -1 and node.base >= 0 and node.label == 1 and node.dualVar == 0):
	                self.expandBlossom(b, True)

	    #transfer mate to pair
	    for v in range(self.nvertex):
	        if self.mate[v] >= 0:
	            self.mate[v] = self.endpoint[self.mate[v]]

	    return self.mate

	def blossomLeaves(self, b):
	    if b < self.nvertex:
	        yield b
	    else:
	        for t in self.nodeList[b].children:
	            if t < self.nvertex:
	                yield t
	            else:
	                for v in self.blossomLeaves(t):
	                    yield v

	def assignLabel(self, w, t, parent=-1):
	    b = self.nodeList[w].inblossom
	    self.nodeList[b].label = self.nodeList[w].label = t
	    self.nodeList[w].parent = self.nodeList[b].parent = parent
	    self.nodeList[w].bestedge = self.nodeList[b].bestedge = -1
	    if t == 1:
	        self.queue.extend(self.blossomLeaves(b))
	    elif t == 2:
	        assert self.mate[self.nodeList[b].base] >= 0
	        base = self.nodeList[b].base
	        self.assignLabel(self.endpoint[self.mate[base]], 1, self.mate[base] ^ 1)


	def scanBlossom(self, v, w):
	    path = []
	    base = -1
	    while v != -1 or w != -1:
	        b = self.nodeList[v].inblossom
	        if self.nodeList[b].label & 4:
	            base = self.nodeList[b].base
	            break
	        path.append(b)
	        assert self.nodeList[b].label == 1
	        self.nodeList[b].label = 5  #relabel mark

	        if self.nodeList[b].parent == -1:
	            v = -1
	        else:
	            v = self.endpoint[self.nodeList[b].parent]
	            b = self.nodeList[v].inblossom
	            assert b != -1
	            b = self.nodeList[b]
	            #blossom must be in outer layer
	            assert b.label == 2
	            v = self.endpoint[b.parent]
	        if w != -1:
	            v, w = w, v
	    for b in path:
	        self.nodeList[b].label = 1
	    return base


	def addBlossom(self, base, k):
	    #find base
	    (v, w, wt) = self.edges[k]
	    bb = self.nodeList[base].inblossom
	    bv = self.nodeList[v].inblossom
	    bw = self.nodeList[w].inblossom

	    #create blossom
	    b_id = self.unusedblossomId.pop()
	    newblossom = self.nodeList[b_id] = Node(b_id)
	    newblossom.create()
	    newblossom.base = base
	    newblossom.father = -1
	    self.nodeList[bb].father = newblossom.id

	    newblossom.children = path = []
	    newblossom.endps = endps = []

	    while bv != bb:
	        path.append(bv)
	        bv = self.nodeList[bv]
	        bv.father = newblossom.id
	        endps.append(bv.parent)

	        assert (bv.label == 2 or (bv.label == 1 and bv.parent == self.mate[bv.base]))

	        v = self.endpoint[bv.parent]
	        bv = self.nodeList[v].inblossom
	    path.append(bb)
	    path.reverse()
	    endps.reverse()
	    endps.append(2 * k)  # indicate which edge contribute to a blossom, use for augment

	    while bw != bb:
	        path.append(bw)
	        bw = self.nodeList[bw]
	        bw.father = newblossom.id
	        endps.append(bw.parent ^ 1)
	        assert (bw.label == 2 or (bw.label == 1 and bw.parent == self.mate[bw.base]))
	        w = self.endpoint[bw.parent]
	        bw = self.nodeList[w].inblossom

	    assert self.nodeList[bb].label == 1
	    newblossom.label = 1
	    newblossom.parent = self.nodeList[bb].parent
	    newblossom.dualVar = 0
	    #Relabel
	    for v in self.blossomLeaves(b_id):
	        if self.nodeList[self.nodeList[v].inblossom].label == 2:
	            self.queue.append(v)
	        self.nodeList[v].inblossom = b_id
	    #update bestEdge
	    bestedgeto = (2 * self.nvertex) * [-1]
	    for bv in path:
	        if self.nodeList[bv].blossombestedges is None:
	            nblists = [[p // 2 for p in self.graph.getAdjacent(v)] for v in self.blossomLeaves(bv)]
	        else:
	            nblists = [self.nodeList[bv].blossombestedges]
	        for nblist in nblists:
	            for k in nblist:
	                (i, j, wt) = self.edges[k]
	                if self.nodeList[j].inblossom == b_id:
	                    i, j = j, i
	                bj = self.nodeList[j].inblossom
	                if (bj != b_id and self.nodeList[bj].label == 1 \
	                            and (bestedgeto[bj] == -1 \
	                                         or self.slack(k) < self.slack(bestedgeto[bj]))):
	                    bestedgeto[bj] = k
	        self.nodeList[bv].blossombestedges = None
	        self.nodeList[bv].bestedge = -1
	    self.nodeList[b_id].blossombestedges = [k for k in bestedgeto if k != 1]
	    self.nodeList[b_id].bestedge = -1
	    for k in self.nodeList[b_id].blossombestedges:
	        if self.nodeList[b_id].bestedge == -1 or self.slack(k) < self.slack(self.nodeList[b_id].bestedge):
	            self.nodeList[b_id].bestedge = k


	def augmentBlossom(self, b, v):
	    t = v
	    while self.nodeList[t].father != b:
	        t = self.nodeList[t].father
	    if t > self.nvertex:
	        self.augmentBlossom(t, v)
	    i = j = self.nodeList[b].children.index(t)
	    if i & 1:  #odd
	        j -= len(self.nodeList[b].children)
	        j_step = 1
	        endptrick = 0
	    else:
	        j = j
	        j_step = -1
	        endptrick = 1
	    # j = len(b.children) - i
	    # j_step = -1
	    while j != 0:
	        j += j_step
	        t = self.nodeList[b].children[j]
	        p = self.nodeList[b].endps[j-endptrick] ^ endptrick
	        if t >= self.nvertex:
	            self.augmentBlossom(t, self.endpoint[p])
	        j += j_step
	        t = self.nodeList[b].children[j]
	        if t >= self.nvertex:
	            self.augmentBlossom(t, self.endpoint[p ^ 1])

	        self.mate[self.endpoint[p]] = p ^ 1
	        self.mate[self.endpoint[p ^ 1]] = p
	    #change the base and Rotate
	    self.nodeList[b].children = self.nodeList[b].children[i:] + self.nodeList[b].children[:i]
	    self.nodeList[b].endps = self.nodeList[b].endps[i:] + self.nodeList[b].endps[:i]
	    self.nodeList[b].base = self.nodeList[self.nodeList[b].children[0]].base
	    assert self.nodeList[b].base == v


	def augmentMatching(self, k):
	    (v, w, wt) = self.edges[k]
	    for (s, p) in ((v, 2 * k + 1), (w, 2 * k)):
	        while 1:
	            bs = self.nodeList[s].inblossom
	            if bs > self.nvertex:
	                self.augmentBlossom(bs, s)
	            #mathc v,w
	            self.mate[s] = p
	            if self.nodeList[bs].parent == -1:
	                break
	            t = self.nodeList[bs].parent
	            t = self.endpoint[t]
	            bt = self.nodeList[t].inblossom
	            #bt must be inner
	            assert self.nodeList[bt].label == 2
	            s = self.endpoint[self.nodeList[bt].parent]
	            j = self.endpoint[self.nodeList[bt].parent ^ 1]
	            if bt >= self.nvertex:
	                self.augmentBlossom(bt, j)
	            self.mate[j] = self.nodeList[bt].parent
	            p = self.nodeList[bt].parent ^ 1


	def expandBlossom(self, b, endstage):
	    for s in self.nodeList[b].children:
	        node = self.nodeList[s]
	        if s < self.nvertex:
	            node.inblossom = s
	        elif endstage and node.dualVar == 0:
	            expandBlossom(s, endps)
	        else:
	            for v in self.blossomLeaves(s):
	                self.nodeList[v].inblossom = s
	    blossom_node = self.nodeList[b]
	    if (not endstage) and blossom_node.label == 2:
	        entrychild = self.nodeList[self.endpoint[blossom_node.parent ^ 1]].inblossom
	        j = blossom_node.children.index(entrychild)
	        if j & 1:
	            #	odd
	            j -= len(blossom_node.children)
	            j_step = 1
	            endptrick = 0
	        else:
	            j_step = -1
	            endptrick = 1
	        p = blossom_node.parent
	        while j != 0:
	            self.nodeList[self.endpoint[p ^ 1]].label = 0
	            self.nodeList[self.endpoint[blossom_node.endps[j - endptrick] ^ endptrick ^ 1]].label = 0
	            self.assignLabel(self.endpoint[p ^ 1], 2, p)
	            self.allowedge[blossom_node.endps[j - endptrick] // 2] = True
	            j += j_step
	            p = blossom_node.endps[j - endptrick] ^ endptrick
	            self.allowedge[p // 2] = True
	            j += j_step

	        bv = blossom_node.children[j]
	        self.nodeList[self.endpoint[p ^ 1]].label = self.nodeList[bv].label = 2
	        self.nodeList[self.endpoint[p ^ 1]].parent = self.nodeList[bv].parent = p
	        self.nodeList[bv].bestedge = -1
	        j += j_step
	        while blossom_node.children[j] != entrychild:
	            bv = blossom_node.children[j]
	            if self.nodeList[bv].label == 1:
	                j += j_step
	                continue
	            for v in self.blossomLeaves(bv):
	                if self.nodeList[v].label != 0:
	                    break
	            if self.nodeList[v].label != 0:
	                assert self.nodeList[v].label == 2
	                self.nodeList[v].label = 0
	                self.nodeList[self.endpoint[self.mate[self.nodeList[bv].base]]].label = 0
	                self.assignLabel(v, 2, self.nodeList[v].parent)
	            j += j_step
	        #clear
	    blossom_node.label = blossom_node.parent = -1
	    blossom_node.children = blossom_node.endps = None
	    blossom_node.base = -1
	    blossom_node.bestedge = -1
	    blossom_node.blossombestedges = None
	    blossom_node = None
	    self.nodeList[b] = None
	    assert self.nodeList[b] == None
	    self.unusedblossomId.append(b)


	def slack(self, k):
	    (v, w, wt) = self.edges[k]
	    return self.nodeList[v].dualVar + self.nodeList[w].dualVar - 2 * wt

# Unit tests
if __name__ == '__main__':
	import unittest, math

	class MaxWeightMatchingTests(unittest.TestCase):

		def test10_empty(self):
		    # empty input graph
		    match = Matching()
		    match.initEdges([])
		    self.assertEqual(match.maxWeightmatching(), [])

		def test11_singleedge(self):
		    # single edge
		    match = Matching()
		    match.initEdges([ (0,1,1) ])
		    self.assertEqual(match.maxWeightmatching(), [1, 0])

	    # def test12(self):
	    # 	match = Matching()
	    # 	match.initEdges([ (1,2,10), (2,3,11) ])
	    #     self.assertEqual( match.maxWeightMatching() , [ -1, -1, 3, 2] )
		def test13(self):
		    match = Matching()
		    match.initEdges([ (1,2,5), (2,3,11), (3,4,5) ])
		    self.assertEqual(match.maxWeightmatching(), [ -1, -1, 3, 2, -1 ])

        def test14_maxcard(self):
            # maximum cardinality
            match = Matching()
            match.initEdges([ (1,2,5), (2,3,11), (3,4,5) ], True)
            print match.maxWeightmatching()
            print [ -1, 2, 1, 4, 3 ]
            self.assertEqual(match.maxWeightmatching(), [ -1, 2, 1, 4, 3 ])

        # def test15_float(self):
        #     # floating point weigths
        #     match = Matching()
        #     match.initEdges([ (1,2,math.pi), (2,3,math.exp(1)), (1,3,3.0), (1,4,math.sqrt(2.0)) ]), [ -1, 4, 3, 2, 1 ])
        #     self.assertEqual(match.maxWeightMatching(),[ -1, 4, 3, 2, 1 ])
        # def test16_negative(self):
        #     # negative weights
        #     self.assertEqual(maxWeightMatching([ (1,2,2), (1,3,-2), (2,3,1), (2,4,-1), (3,4,-6) ], False), [ -1, 2, 1, -1, -1 ])
        #     self.assertEqual(maxWeightMatching([ (1,2,2), (1,3,-2), (2,3,1), (2,4,-1), (3,4,-6) ], True), [ -1, 3, 4, 1, 2 ])

        # def test20_sblossom(self):
        #     # create S-blossom and use it for augmentation
        #     self.assertEqual(maxWeightMatching([ (1,2,8), (1,3,9), (2,3,10), (3,4,7) ]), [ -1, 2, 1, 4, 3 ])
        #     self.assertEqual(maxWeightMatching([ (1,2,8), (1,3,9), (2,3,10), (3,4,7), (1,6,5), (4,5,6) ]), [ -1, 6, 3, 2, 5, 4, 1 ])

    #     def test21_tblossom(self):
    #         # create S-blossom, relabel as T-blossom, use for augmentation
    #         self.assertEqual(maxWeightMatching([ (1,2,9), (1,3,8), (2,3,10), (1,4,5), (4,5,4), (1,6,3) ]), [ -1, 6, 3, 2, 5, 4, 1 ])
    #         self.assertEqual(maxWeightMatching([ (1,2,9), (1,3,8), (2,3,10), (1,4,5), (4,5,3), (1,6,4) ]), [ -1, 6, 3, 2, 5, 4, 1 ])
    #         self.assertEqual(maxWeightMatching([ (1,2,9), (1,3,8), (2,3,10), (1,4,5), (4,5,3), (3,6,4) ]), [ -1, 2, 1, 6, 5, 4, 3 ])

    #     def test22_s_nest(self):
    #         # create nested S-blossom, use for augmentation
    #         self.assertEqual(maxWeightMatching([ (1,2,9), (1,3,9), (2,3,10), (2,4,8), (3,5,8), (4,5,10), (5,6,6) ]), [ -1, 3, 4, 1, 2, 6, 5 ])

    #     def test23_s_relabel_nest(self):
    #         # create S-blossom, relabel as S, include in nested S-blossom
    #         self.assertEqual(maxWeightMatching([ (1,2,10), (1,7,10), (2,3,12), (3,4,20), (3,5,20), (4,5,25), (5,6,10), (6,7,10), (7,8,8) ]), [ -1, 2, 1, 4, 3, 6, 5, 8, 7 ])

    #     def test24_s_nest_expand(self):
    #         # create nested S-blossom, augment, expand recursively
    #         self.assertEqual(maxWeightMatching([ (1,2,8), (1,3,8), (2,3,10), (2,4,12), (3,5,12), (4,5,14), (4,6,12), (5,7,12), (6,7,14), (7,8,12) ]), [ -1, 2, 1, 5, 6, 3, 4, 8, 7 ])

    #     def test25_s_t_expand(self):
    #         # create S-blossom, relabel as T, expand
    #         self.assertEqual(maxWeightMatching([ (1,2,23), (1,5,22), (1,6,15), (2,3,25), (3,4,22), (4,5,25), (4,8,14), (5,7,13) ]), [ -1, 6, 3, 2, 8, 7, 1, 5, 4 ])

    #     def test26_s_nest_t_expand(self):
    #         # create nested S-blossom, relabel as T, expand
    #         self.assertEqual(maxWeightMatching([ (1,2,19), (1,3,20), (1,8,8), (2,3,25), (2,4,18), (3,5,18), (4,5,13), (4,7,7), (5,6,7) ]), [ -1, 8, 3, 2, 7, 6, 5, 4, 1 ])

    #     def test30_tnasty_expand(self):
    #         # create blossom, relabel as T in more than one way, expand, augment
    #         self.assertEqual(maxWeightMatching([ (1,2,45), (1,5,45), (2,3,50), (3,4,45), (4,5,50), (1,6,30), (3,9,35), (4,8,35), (5,7,26), (9,10,5) ]), [ -1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ])

    #     def test31_tnasty2_expand(self):
    #         # again but slightly different
    #         self.assertEqual(maxWeightMatching([ (1,2,45), (1,5,45), (2,3,50), (3,4,45), (4,5,50), (1,6,30), (3,9,35), (4,8,26), (5,7,40), (9,10,5) ]), [ -1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ])

    #     def test32_t_expand_leastslack(self):
    #         # create blossom, relabel as T, expand such that a new least-slack S-to-free edge is produced, augment
    #         self.assertEqual(maxWeightMatching([ (1,2,45), (1,5,45), (2,3,50), (3,4,45), (4,5,50), (1,6,30), (3,9,35), (4,8,28), (5,7,26), (9,10,5) ]), [ -1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ])

    #     def test33_nest_tnasty_expand(self):
    #         # create nested blossom, relabel as T in more than one way, expand outer blossom such that inner blossom ends up on an augmenting path
    #         self.assertEqual(maxWeightMatching([ (1,2,45), (1,7,45), (2,3,50), (3,4,45), (4,5,95), (4,6,94), (5,6,94), (6,7,50), (1,8,30), (3,11,35), (5,9,36), (7,10,26), (11,12,5) ]), [ -1, 8, 3, 2, 6, 9, 4, 10, 1, 5, 7, 12, 11 ])

    #     def test34_nest_relabel_expand(self):
    #         create nested S-blossom, relabel as S, expand recursively
    #         self.assertEqual(maxWeightMatching([ (1,2,40), (1,3,40), (2,3,60), (2,4,55), (3,5,55), (4,5,50), (1,8,15), (5,7,30), (7,6,10), (8,10,10), (4,9,30) ]), [ -1, 2, 1, 5, 9, 3, 7, 6, 10, 4, 8 ])

	# unittest.main()
	#test maxcard
	match = Matching()
	match.initEdges([ (1,2,5), (2,3,11), (3,4,5) ])
	print match.maxWeightmatching(True)
	print [ -1, 2, 1, 4, 3 ]
	#test nest_tnasty_expand
	match = Matching()
	match.initEdges([ (1,2,45), (1,7,45), (2,3,50), (3,4,45), (4,5,95), (4,6,94), (5,6,94), (6,7,50), (1,8,30), (3,11,35), (5,9,36), (7,10,26), (11,12,5) ])
	print match.maxWeightmatching()
	print [ -1, 8, 3, 2, 6, 9, 4, 10, 1, 5, 7, 12, 11 ]
	# create blossom, relabel as T, expand such that a new least-slack S-to-free edge is produced, augment
	match = Matching()
	match.initEdges([ (1,2,45), (1,5,45), (2,3,50), (3,4,45), (4,5,50), (1,6,30), (3,9,35), (4,8,28), (5,7,26), (9,10,5) ])
	print match.maxWeightmatching()
	print [ -1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ]
	# create blossom, relabel as T in more than one way, expand, augment
	match = Matching()
	match.initEdges([ (1,2,45), (1,5,45), (2,3,50), (3,4,45), (4,5,50), (1,6,30), (3,9,35), (4,8,35), (5,7,26), (9,10,5) ])
	print match.maxWeightmatching()
	print  [-1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ]


    # # print match.maxWeightmatching()



