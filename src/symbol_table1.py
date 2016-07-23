class HashTable:
	def __init__(self):
		self.table={}   # a dictionary

	def add_entry (self, name, list_attributes):
		if name in self.table:
			print 'Error: Entry already present - [' + name + ']'
		else:
			self.table[name]= {}	# a dictionary
			for i_key in list_attributes:	
				self.table[name][i_key]=list_attributes[i_key]
		
	def get_attribute_value (self, name, attribute_name):
		
		try:
			return self.table[name][attribute_name]
		except:
			return None			


class Env:
	def __init__(self, prev=None):
		self.current_hashtable = HashTable()
		self.prev_env=prev
		
	#adds entry in current hashtable
	def add_entry(self,name, list_attributes):
		self.current_hashtable.add_entry(name, list_attributes)

	#Returns list of attributes from most recent hashtable (recent ancestor) corresponding to name. Returns None if entry not found
	def get_attribute_value(self,name, attribute_name):
		env=self
		while env!=None:
			found=env.current_hashtable.get_attribute_value(name, attribute_name)
			if found != None:
				return found
			env=env.prev_env
		return None
