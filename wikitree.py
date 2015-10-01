from sparql import Sparql
from collections import defaultdict

class Tree:
#family tree
	
	def __init__(self, firstPerson):
		self.allFamilyMembers = {}
		self.allFamilyMembers[firstPerson] = Person(firstPerson)
		self.processNextFamilyMember(self.allFamilyMembers[firstPerson])
		
	
	def processNextFamilyMember(self, person, remaingPersons = set()):
		#get family members
		
		for familyMember in person.returnFamilyMembers():
			
			if familyMember not in self.allFamilyMembers:
				self.allFamilyMembers[familyMember] = Person(familyMember)
				#maybe on remainingpersons list
				if familyMember in remaingPersons:
					remaingPersons.remove(familyMember)

			#put all unprocessed members on remainPersonlist
			familyMembers = self.allFamilyMembers[familyMember].returnFamilyMembers()
			if familyMembers is not None:
				
				for m in set(familyMembers):
					if m not in self.allFamilyMembers.keys() and m not in remaingPersons:
						remaingPersons.add(m)

			

					if len(set(remaingPersons).intersection(set(self.allFamilyMembers.keys()))) > 0:
						print(familyMember)
						print(m)
						print(set(remaingPersons).intersection(set(self.allFamilyMembers.keys())))
						
							
							
				#l = [m for m in familyMembers if m not in self.allFamilyMembers or m not in remaingPersons]	
				

		

		if len(remaingPersons) > 0:
			val = remaingPersons.pop()
			self.allFamilyMembers[val] = Person(val)		
			self.processNextFamilyMember(self.allFamilyMembers[val], remaingPersons)	
		else:
			for key in self.allFamilyMembers:
				print(self.allFamilyMembers[key])
			

class Person:
#nodes in the tree
	def __init__(self, person):
		
		self.name = person
		wiki = getWikiInfo(person)
		self.spouse = wiki.getSpouse()
		self.mother = wiki.getMother()
		self.father = wiki.getFather()
		self.fullName = wiki.getFullName()

	
	def __str__(self):
		return "Spouse= {}, Mother = {}, Father = {}".format(self.spouse, self.mother, self.father) 

	def returnFamilyMembers(self):	
		#properties = [self.mother , self.father , self.spouse]
		properties = [self.mother, self.father]
		if len(properties[0]) > 0 :
			return [value for value, propType in properties if propType == "uri"]
		else:
			return []

	def getFullName(self):
		return self.fullName

class getWikiInfo:
#retrieves the family from wiki text and infoboxes

	def __init__(self, person):
		#print(person)
		self.person = person
		self.query = Sparql(person)
		self.setSpouse()
		self.setMother()
		self.setFather()
	

	def setSpouse(self):
		if 'spouse' in self.query.result:
			self.spouse = list(self.query.result['spouse'])
		else:
			self.spouse = []	
	
	def setMother(self):
		if 'mother' in self.query.result:
			self.mother = list(self.query.result['mother'])
		else:
			self.mother = []	
	
	def setFather(self):
		if 'father' in self.query.result:
			self.father = list(self.query.result['father'])
		else:
			self.father = []	
		
	def getSpouse(self):
		return self.spouse
	
	def getMother(self):
		return self.mother

	def getFather(self):
		return self.father

	def getFullName(self):
		return ['Beatrix van Oranje']


	

		

familyTree = Tree("Beatrix_of_the_Netherlands")





