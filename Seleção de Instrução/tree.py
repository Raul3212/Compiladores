class Tree:
	def __init__(self, value, right = None, left = None):
		self.pai = None
		self.value = value
		self.left = left
		self.right = right
		self.groupId = -1
		self.cost = 0
		self.expred = False
		if right != None:
			self.right.pai = self
		if left != None:
			self.left.pai = self
		
	def __str__(self):
		return str(self.value)
	
	
def getPosOrderList(tree):
	if tree == None:
		return []
	return getPosOrderList(tree.left) + getPosOrderList(tree.right) + [tree]
		

def printIndented(tree, level=0):
	print '<' + str(tree.value) + ',' + str(tree.groupId) + '>'
	if tree.right != None:
		print '        ' * level + '|' + '------', 
		printIndented(tree.right, level+1)
	if tree.left !=  None:
		print '        ' * level + '|' + '------', 
		printIndented(tree.left, level+1)	 
		
def getTotalCost(tree):
	total = 0
	for t in getPosOrderList(tree):
		total += t.cost
	return total		
	