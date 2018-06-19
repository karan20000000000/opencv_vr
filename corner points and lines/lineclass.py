class Line:
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2
		import math
		self.len = math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )
	def __repr__(self):
		return "Line("+str(self.p1)+", "+str(self.p2)+", "+str(self.len)+")"
