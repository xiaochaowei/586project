class Test:
	def __init__(self):
		self.num = 1
	def setNum(self, num, num2 = None):
		self.num = num
		self.getNum()
	def getNum(self):
		print self.num
def change(t):
	t.setNum(2)
t = Test()
change(t)
# t.getNum()
# print t.nu
