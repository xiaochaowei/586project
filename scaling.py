# whole process
import math
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
	    self.breaktie = 0

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
	
	def checkBreakTie(self, v):
		node = self.nodeList[v]
		assert node != None
		if abs(node.dualVar - self.breaktie)< 0.01:
			return True
		else:
			return False

	def maxWeightmatching(self, eps, maxcardinality=False):
		nvertex = self.nvertex
		max_weight = self.graph.max_weight
		nodeList = self.nodeList
		delta = eps * max_weight
		N = max_weight

		#init value
		for idx in range(0, nvertex):
			if nodeList[idx] == None:
				nodeList[idx] = Node(idx, max_weight /2.0 - delta / 2)
		max_weight = max_weight / 2.0
		#Main Loop
		delta0 = delta
		self.delta = delta
		L = int(math.log(N,2))
		for t in range(0, L):
			# self.cleanData()
			#label
			# delta = delta / 2.0
			self.breaktie = max_weight / 2.0  - self.delta / 2.0
			max_weight = max_weight / 2
			assert self.breaktie ==(N / math.pow(2,t+2) - delta0/math.pow(2,t+1))
			#check breaktie, repeart the follow step until y_value of gree vertices reach ....
			while 1:

				#step 1 augment the path
				self.cleanData()
				next_stage = False
				for v in range(0, nvertex):
					if self.mate[v] == -1 and nodeList[v].label == 0:
						if self.checkBreakTie(v):
							next_stage = True
							break
						self.assignLabel(v, 1, -1)
				if next_stage == True:
					break
				augmented = 0
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
						   	if self.slack(k,t):
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
								# else:
								#	 #blossom
								#	 self.addBlossom(base, k)

							elif adjacent_node.label == 0:
								adjacent_node.label = 2
								adjacent_node.parent = p ^ 1
				if augmented:
					continue
				self.cleanData()
				for v in range(0, nvertex):
					if self.mate[v] == -1 and nodeList[v].label == 0:
						if self.checkBreakTie(v):
							next_stage = True
							break
						self.assignLabel(v, 1, -1)
				while self.queue:
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
						   	if self.slack(k,t):
								self.allowedge[k] = True
						if self.allowedge[k]:
							#case1 outer unlabel
							if nodeList[adjacent_node.inblossom].label == 0:
								self.assignLabel(w, 2, p ^ 1)

							elif nodeList[adjacent_node.inblossom].label == 1:
								base = self.scanBlossom(v.id, w)
								assert base != -1
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
				inner_zero_blososms = []
				#dual ajustment
				for v in range(self.nvertex):
					node = self.nodeList[v]
					if node == None:
						continue
					if self.nodeList[node.inblossom].label == 1:
						node.dualVar -= self.delta / 2 
					elif self.nodeList[node.inblossom].label == 2:
						node.dualVar += self.delta / 2
				for b in range(self.nvertex, 2 * self.nvertex):
					node = self.nodeList[b]
					if node == None:
						continue
					if node.base >= 0 and node.parent == -1:
						if node.label == 1:
							node.dualVar += self.delta
						elif node.label == 2:
							node.dualVar -= self.delta
							if node.dualVar <= 0:
								assert node.dualVar < 0
								inner_zero_blososms.append(b)
				 #find if there is T blossom have zero value
				#expand T blossom:
				while len(inner_zero_blososms) > 0:
					self.expandBlossom(inner_zero_blososms.pop(), False)
				for b in range(self.nvertex, 2 * self.nvertex):
					if not self.nodeList[b]:
						continue
					node = self.nodeList[b]
					if (node.father == -1 and node.base >= 0 and node.label == 1 and node.dualVar == 0):
						self.expandBlossom(b, True)
			#update value
			self.delta = self.delta/2.0
			for i in range(0, self.nvertex):
				node = nodeList[i]
				if node != None:
					node.dualVar = node.dualVar + self.delta
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
	    if t == 1:
	        self.queue.extend(self.blossomLeaves(b))
	    elif t == 2:
	        assert self.mate[self.nodeList[b].base] >= 0
	        k = self.mate[self.nodeList[b].base]//2
	        if self.slack(k,t):
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
	        node.father = -1
	        if s < self.nvertex:
	            node.inblossom = s
	        elif endstage and node.dualVar == 0:
	            self.expandBlossom(s, endstage)
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
	    blossom_node.label = blossom_node.label = -1
	    blossom_node.children = blossom_node.endps = None
	    blossom_node.base = -1
	    blossom_node.bestedge = -1
	    blossom_node.blossombestedges = None
	    blossom_node = None
	    self.nodeList[b] = None
	    assert self.nodeList[b] == None
	    self.unusedblossomId.append(b)


	def slack(self, k, t):
		(v, w, wt) = self.edges[k]
		delta = self.delta
		node1 = self.nodeList[v]
		node2 = self.nodeList[w]
		if node1.inblossom == node2.inblossom and node1.inblossom > self.nvertex:
			return True
		elif self.mate[v] >= 0 and self.mate[w] >=0:
			
			# assert self.mate[w] >=0
			kslack = self.nodeList[v].dualVar + self.nodeList[w].dualVar - (wt // delta * delta)
			print kslack
			if kslack / delta >= 0:
				return True
			else:
				return False
		elif self.mate[v] <0 or self.mate[w] < 0:
			kslack = node1.dualVar + node2.dualVar - (wt // delta * delta)
			print kslack
			if kslack / delta == -1:
				return True
			else:
				return False
		assert True == False

	def checkBreakTie(self, v):
		node = self.nodeList[v]
		assert node != None
		if abs(node.dualVar - self.breaktie)< 0.01:
			return True
		else:
			return False


# Unit tests
if __name__ == '__main__':
	# unittest.main()
	#test maxcard
	# match = Matching()
	# match.initEdges([ (1,2,5), (2,3,11), (3,4,5) ])
	# print match.maxWeightmatching(True)
	# print [ -1, 2, 1, 4, 3 ]
	# #test nest_tnasty_expand
	# match = Matching()
	# match.initEdges([ (1,2,45), (1,7,45), (2,3,50), (3,4,45), (4,5,95), (4,6,94), (5,6,94), (6,7,50), (1,8,30), (3,11,35), (5,9,36), (7,10,26), (11,12,5) ])
	# print match.maxWeightmatching()
	# print [ -1, 8, 3, 2, 6, 9, 4, 10, 1, 5, 7, 12, 11 ]
	# # create blossom, relabel as T, expand such that a new least-slack S-to-free edge is produced, augment
	# match = Matching()
	# match.initEdges([ (1,2,45), (1,5,45), (2,3,50), (3,4,45), (4,5,50), (1,6,30), (3,9,35), (4,8,28), (5,7,26), (9,10,5) ])
	# print match.maxWeightmatching()
	# print [ -1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ]
	# # create blossom, relabel as T in more than one way, expand, augment
	match = Matching()
	# match.initEdges([(1,2,8), (1,5,4),(1,4,4),(2,3,8),(3,4,8),(4,5,2) ])
	match.initEdges([ (1,2,128), (1,7,45), (2,3,50), (3,4,45), (4,5,95), (4,6,94), (5,6,94), (6,7,50), (1,8,30), (3,11,35), (5,9,36), (7,10,26), (11,12,5) ])
	print match.maxWeightmatching(1/4.0)
	# print  [-1, 6, 3, 2, 8, 7, 1, 5, 4, 10, 9 ]


    # # print match.maxWeightmatching()



