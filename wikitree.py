from sparql import Sparql
from collections import defaultdict

class Tree:
#family tree
	
	def __init__(self, firstPerson):
		self.allFamilyMembers = defaultdict(list)
		self.allFamilyMembers[firstPerson] = Person(firstPerson)
		self.processNextFamilyMember(self.allFamilyMembers[firstPerson] , [])
		
	
	def processNextFamilyMember(self, person, remaingPersons):
		#get family members
		
		for familyMember in person.returnFamilyMembers():
			self.allFamilyMembers[familyMember] = Person(familyMember)

			#put all unprocessed members on remainPersonlist
			familyMembers = self.allFamilyMembers[familyMember].returnFamilyMembers()
			l = [m for m in familyMembers if m not in self.allFamilyMembers and m not in remaingPersons]	
			remaingPersons.extend(l)
			print(remaingPersons)

		if len(remaingPersons) > 0:			
			next = Person(remaingPersons.pop(0))
			self.processNextFamilyMember(next, remaingPersons)
		else:
			print(self.allFamilyMembers["Beatrix_of_the_Netherlands"])
			

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
		return "Name = {},  Spouse= {}, Mother = {}, Father = {}".format(self.fullName, self.spouse, self.mother, self.father) 

	def returnFamilyMembers(self):
		newlist = [self.mother , self.father , self.spouse]
		return newlist
		
	def getFullName(self):
		return self.fullName

class getWikiInfo:
#retrieves the family from wiki text and infoboxes

	def __init__(self, person):
		self.person = person
		self.query = Sparql(person)
		self.setSpouse()
		self.setMother()
		self.setFather()
	

	def setSpouse(self):
		if 'spouse' in self.query.result:
			self.spouse = self.query.result['spouse']
		else:
			self.spouse = []	
	
	def setMother(self):
		if 'mother' in self.query.result:
			self.mother = self.query.result['mother']
		else:
			self.mother = []	
	
	def setFather(self):
		if 'father' in self.query.result:
			self.father = self.query.result['father']
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





