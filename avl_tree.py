from utilities import *

	
	

class Languages:
	def __init__(self):
		self.data_by_year = {}
	def build_test(self, fname):
		file_object = open(fname, 'r')
		return self.build_trees_from_file(file_object)
		
	def build_trees_from_file(self, file_object):
		lines=[]
		for line in file_object:
			lines.append(line)
		lines.pop(0)
		for i in range(len(lines)):
			lines[i] = lines[i].replace('\n', '') 	
		
		lmao=[]
		for line in lines:
			comma_count=0;
			element=''
			name=''
			count=''
			year=''
			
			for char in line:
				
				if char==',':
					
					if comma_count==0:
						year=element
						
						element=''
						comma_count=comma_count+1	
					elif comma_count==1:
						name=element
						
						element=''
						comma_count=comma_count+1	
				
				else:
					element = element + char
					
				count = element	
				
				
			lmao.append(LanguageStat(name, year, int(count)))	
		
		prev_year=int(lmao[0].year)
		LangList=[]
		yeet={}
		for LangStat in lmao:
			year = int(LangStat.year)
			if year==prev_year:
				
				LangList=LangList+[LangStat]
				
			else: 
				if yeet=={}:
					yeet={prev_year: LangList}
				else: 
					yeet.update({prev_year: LangList})
					
				LangList=[LangStat]
				
			prev_year = year
		if yeet=={}:
			yeet={prev_year: LangList}
		else: 
			yeet.update({prev_year: LangList})		
		
		#turn languagesstat into nodes lmaoooooo
		
		for key, LangList in yeet.items():
			
			tree=None
			for language in LangList:
				node=Node(language)
				if not tree:
					tree=BalancingTree(node)
					
				else:	
					tree.balanced_insert(node)
					
				
			if self.data_by_year=={}:
				self.data_by_year={key: tree}
			else:
				self.data_by_year.update({key: tree})
				
			
				
				
		return self.data_by_year			
	
			
			
	def query_by_name(self, language_name):
		d={}
		for key, tree in self.data_by_year.items():
			node= tree.search_name(language_name)
			if node:
				if d=={}:
					d={key:node.val.count}
				else:
					d.update({key:node.val.count})
				
		return d	

	def query_by_count(self, threshold = 0):
		d={}
		for key, tree in self.data_by_year.items():
			l=tree.search_count(tree.root, threshold)
			if l:
				
				if d=={}:
					d={key: l}
				else:
					d.update({key:l})
		return d



class BalancingTree:
	def __init__(self, root_node):
		self.root = root_node
		
	def search_count(self, curr, threshhold):
		result = []
		if curr:
			if curr.val.count>threshhold:
				result.append(curr.val.name)
			result += self.search_count(curr.left, threshhold)
			result += self.search_count(curr.right, threshhold)
			
		return result
		
		
	def search_name(self, name):
		if self.root.val.name==name:
			return self.root
		elif self.root==None:
			return None
		else:
			return self.search_name_helper(self.root, name)
	def search_name_helper(self, current, name):
		if current==None:
			return None
		if current.val.name==name:
			return current
		
		if self.search_name_helper(current.left, name):
			return self.search_name_helper(current.left,name)
		if self.search_name_helper(current.right,name):
			return self.search_name_helper(current.right,name)
	
	
		        
		
	def balanced_insert(self, node, curr = None):
		curr = curr if curr else self.root
		self.insert(node, curr)
		
		self.balance_tree(node)

	def update(self, curr):
		if not curr.parent==None:
			self.update_height(curr.parent)
			self.update(curr.parent)
			
	
		
	def insert(self, node, curr = None):
		curr = curr if curr else self.root
		
		if node._val < curr._val:
			if curr.left is not None:
				self.insert(node, curr.left)
			else:
				node.parent = curr
				
				curr.left = node
		else:
			if curr.right is not None:
				self.insert(node, curr.right)
			else:
				node.parent = curr
				curr.right = node
		return
	
	
	def balance_tree(self, node):
		
		bf=self.find_balance_factor(node)
		node.bf=bf
		if abs(bf)>1:
			if node.bf >0:
				if node.right and self.find_balance_factor(node.right) > 0:
					self.left_rotate(node)
				else:
					self.right_rotate(node.right)
					self.left_rotate(node)
			else:
				
				if node.left and self.find_balance_factor(node.left) < 0:
					self.right_rotate(node)
				else:
					self.left_rotate(node.left)
					self.right_rotate(node)	
					
		if not node.parent==None:
			self.update_height(node.parent)
			self.balance_tree(node.parent)
							
	
	def update_height(self, node):
		node.height = 1 + max(self.height(node.left), self.height(node.right))

	
	def height(self, node):
		return node.height if node else -1
	
	
	
	def left_rotate(self, z):
		
		y = z.right
		y.parent = z.parent
		if y.parent is None:
			self.root = y
		else:
			if y.parent.left is z:
				y.parent.left = y
			elif y.parent.right is z:
				y.parent.right = y
		z.right = y.left
		if z.right is not None:
			z.right.parent = z
		y.left = z
		z.parent = y
		
		self.update_height(z)
		self.update_height(y)
		y.bf=self.find_balance_factor(y)
		z.bf=self.find_balance_factor(z)

	
	def right_rotate(self, z):
		
		y = z.left
		y.parent=z.parent
		if y.parent is None:
			self.root = y
		else:
			if y.parent.left is z:
				y.parent.left = y
			elif y.parent.right is z:
				y.parent.right = y
		z.left = y.right
		if z.left is not None:
			z.left.parent=z
		y.right=z
		z.parent = y
		
		self.update_height(z)
		self.update_height(y)
		y.bf=self.find_balance_factor(y)
		z.bf=self.find_balance_factor(z)		
				
	def find_balance_factor(self, node):
		'''
		if node.right==None:
			r=0
		else:
			r=1+node.right.height
		if node.left==None:
			l=0
		else:
			l=1+node.left.height
		'''
		return node.right.height-node.left.height

	
	def is_balanced(self):
		if abs(self.find_balance_factor(self.root)) <=1:
			return True
		else:
			return False
		

	
	
