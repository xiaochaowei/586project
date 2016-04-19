class Node:

	def __init__(self, id, max_weight = 0):
		self.label = 0
		self.inblossom = id #top-level blossom
		self.parent = -1
		self.dualVar = max_weight
		self.mate = -1
		self.id = i
		self.father = -1
		self.base = i
		self.children = []
		self.endps = []
		self.bestedge = -1
		self.blossombestedges = None

	def addBlossom(self, i):
		self.inblossom = i
	def addMate(self, i):
		self.mate = i
	def __eq__(self, node2):
		if node1.idx == node2.idx:
			return True
		else:
			return False
	def __neq__(self, node2):
		if node1.idx != node2.idx:
			return True
		else:
			return False

def blossomLeaves(self, b):
	if b < self.nvertex:
		yield b
	else:
		for t in self.nodeList[b].children:
			if t < self.nvertex:
				yield t
			else:
				for v in self.blossomLeaves(b):
					yield v

def assignLabel(self, node, t, parent = -1):
	b = node.inblossom
	self.nodeList[b].label = t
	node.label = t
	node.parent = self.nodeList[b].parent = parent
	node.bestedge = self.nodeList[b].bestedge = -1
	if t == 1:
		self.queue.extent(self.blossomLeaves(b))
	elif t == 2:
		assert self.nodeList[self.nodeList[b].base].mate > 0
		base = self.nodeList[b].base
		self.assignLabel(self.endpoint[self.nodeList[base].mate], 1, self.nodeList[base].mate ^ 1)

def scanBlossom(self, v, w):
	path = []
	base = -1 
	while v != -1 or w != -1:
		b = v.inblossom
		if self.nodeList[b].label & 4:
			base = self.nodeList[b].base
			break
			path.append(b)
			self.nodeList[b] = 5

			if self.nodeList[b].parent == -1:
				v = -1
			else:
				v = self.endpoint[self.nodeList[b].parent]
				v = self.nodeList[v]
				#blossom must be in outer layer 
				assert v.label == 2
				assert v.parent > 0
				v = self.endpoint[v.parent]
			if w !=-1:
				v,w = w,v
	for b in path:
		self.nodeList[b].label = 1
	return base

