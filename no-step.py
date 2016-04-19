#whole process
#O(n**3)
import copy
class Graph:

	def __init__(self):
		self.graph = {}
		self.nvertex = 0
		self.nedge = 0
		self.max_weight = -1
		self.neighbor = None
		self.edges = []

	def addEdges(self, edges):
		self.nvertex = -1
		for (i,j,w) in edges:
			if i > self.nvertex:
				self.nvertex = i
			if j > self.nvertex:
				self.nvertex = j
		self.nvertex =  self.nvertex + 1
		self.edges = edges
		self.nedge = len(self.nedges)
		self.endpoint = [self.edges[p//2][p%2] for p in range(0, 2 * self.nedge)]
		self.neighbor = [[] for i in range(self.nvertex)]
		for k in range(self.nedge):
			(i,j,w) = self.edges[k]
			if w > self.max_weight:
				self.max_weight = w
			self.neighbor[i].append(2*k+1)
			self.neighbor[j].append(2*k)


	def getAdjacent(self, i):
		 return self.neighbor[i]


class Matching:
	def __init__(self):
	def initEdges(sef, edges):
		self.graph = Graph()
		self.graph.addEdges(edges)
		self.nvertex = self.graph.nvertex
		self.edges = self.nedges
		self.endpoint = self.graph.endpoint
		self.n_vertex = self.graph.nvertex
		self.nodeList = [None for i in range(0, n_vertex)]
		self.queue[:] = []
		self.mate = n_vertex * [-1]
		
	def MaxWightmatching(self, edges):
		n_vertex = self.nvertex
		max_weight = self.graph.max_weight
		nodeList = self.nodeList
		for idx in range(0, n_vertex):
			if self.nodeList[idx] == None:
				nodeList[idx] = node(idx, max_weight)
		#Main Loop
		for t in range(0, n_vertex):
			#label 
			for v in range(0, n_vertex):
				if nodeList[v].mate == -1 and nodeList[v].label = 0:
					self.assignLabel(nodeList[v], 1, -1)
			
			augmented = 0
			while 1:

				while self.queue and not augmented:
					v = self.queue.pop()
					v = self.nodeList[v]
					assert v.label = 1 and nodeList[v.inblossom].label = 1
					neighbor = self.graph.getAdjacent(v.id)
					for p in neighbor:
						k = p//2
						w = self.endpoint[p]
						adjacent_node = nodeList[w]
						if v.inblossom = adjacent_node.inblossom:
							continue
						if self.slack(v, adjacent_node) <= 0:
							#case1 outer unlabel
							if nodeList[adjacent_node.inblossom].label == 0:
								self.assignLabel(adjacent_node, 2, p^1)
							elif nodeList[adjacent_node.inblossom].label == 1:
								base = self.scanBlossom(v, w)
							#case2 outer outer no same root  -> augmenting_path
								if base == -1:
									#finding augumenting path 
									self.augmentMatching(v, adjacent_node)
									augmented = 1
							#case3 outer same root -> blossom
								else:
									#blossom
									self.addBlossom(base, k)

							elif adjacent_node.label == 0:
								adjacent_node.label = 2
								adjacent_node.parent = p^1
				if augmented == 1:
					break




	def addBlossom(self, base, k):
		#find base
		(v, w, wt) = self.edges[k]
		bb = self.nodeList[base].inblossom
		bv = self.nodeList[v].inblossom
		bw = self.nodeList[w].inblossom

		#create blossom
		b_id = self.unusedblossomId.pop()
		newblossom = self.nodeList[b_id] = node(b_id)
		newblossom.base = base
		newblossom.father = -1
		nodeList[bb].father = newblossom.id

		newblossom.children = path = []
		newblossom.endps = endps = []

		while bv != bb:
			path.append(bv)
			bv = self.nodeList[bv]
			bv.father = newblossom.id
			endps.append(bv.parent)
			assert(bv.label == 2 or (bv.label == 1 and bv.parent == self.mate[bv.base]))
			v = self.endpoint[bv.id]
			bv = self.nodeList[v].inblossom
		path.append(bb)
		path.reverse()
		endps.reverse()
		endps.append(2*k)# indicate which edge contribute to a blossom, use for augment

		while bw != bb:
			path.append(bw)
			bw = self.nodeList[bw]
			bw.father = newblossom.id
			endps.append(bw.parent^1)
			assert(bw.label == 2 or (bw.label == 1 and bw.parent == self.mate[bw.base]))
			w = self.endpoint[bw.id]
			bw = self.nodeList[w].inblossom

		assert nodeList[bb].label == 1
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
		if t > self.n_vertex
			self.augmentBlossom(t, v)
		i = j = nodeList[b].children.index(t)
		if i & 1: #odd
			j -= len(nodeList[b].children) 
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
			p = self.nodeList[b].endps[j] ^ endptrick
			if t >= self.nvertex:
				self.augmentBlossom(t, self.endpoint[p])
			j += j_step
			t = self.nodeList[b].children[j]
			if t >= self.vertex:
				self.augmentBlossom(t, self.endpoint[p^1])

			mate[self.endpoint[p]] = p ^ 1
			mate[self.endpoint[p^1]] = p
		#change the base and Rotate
		self.nodeList[b].children = self.nodeList[b].children[i:] + self.nodeList[b].children[:i]
		self.nodeList[b].endps = self.nodeList[b].endps[i:] + self.nodeList[b].endps[:i]
		self.nodeList[b].base = self.nodeList[b].children[0].base

	def augmentMatching(self, k):
		(v, w, wt) = self.edges[k]
		for (s,p) in ((v, 2*k+1), (w, 2*k)):
			while 1:
				bs = self.nodeList[s].inblossom
				if bs > self.nvertex:
					self.augmentBlossom(bs, s)
				#mathc v,w
				mate[s] = p
				if self.nodeList[bs].parent == -1:
					break
				t= self.nodeList[bs].parent
				t = self.endpoint[t]
				bt = self.nodeList[t].inblossom
				#bt must be inner
				assert self.nodeList[bt].label == 2
				s = self.endpoint[self.nodeList[bt].parent]
				j = self.endpoint[self.nodeList[bt].parent^1]
				if bt >= self.nvertex:
					self.augmentBlossom(bt, j)
				self.mate[j] = self.nodeList[bt].parent
				p = self.nodeList[bt].parent ^ 1

	
	def expandBlossom(b, endstage):

	def slack(self, node1, node2):
		return node1.dualVar + node2.dualVar - this.graph.getweight(node1.idx, node2.idx)

