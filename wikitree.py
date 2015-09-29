class Tree:
#family tree
	
	def __init__(self, firstPerson):
		self.allFamilyMembers = {}
		self.allFamilyMembers[firstPerson] = Person(firstPerson)
		self.processNextFamilyMember(self.allFamilyMembers[firstPerson] , [], 0)
		
	
	def processNextFamilyMember(self, person, remaingPersons, i):
		
		i = i + 1#for testing only 50 iterations


		#get family members
		for familyMember in person.returnFamilyMembers():
			self.allFamilyMembers[familyMember] = Person(familyMember)	
			remaingPersons.extend(self.allFamilyMembers[familyMember].returnFamilyMembers())
		if len(remaingPersons) > 0 and i < 50:
			next = self.allFamilyMembers[remaingPersons.pop(0)]
			self.processNextFamilyMember(next, remaingPersons, i)
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
		return list(self.spouse + self.mother + self.father)	
		
	def getFullName(self):
		return self.fullName

class getWikiInfo:
#retrieves the family from wiki text and infoboxes

	def __init__(self, person):
		self.person = person
		
		
	def getSpouse(self):
		return ['Claus']

	def getMother(self):
		return ['Juliana']

	def getFather(self):
		return ['Bernard']

	def getFullName(self):
		return ['Beatrix van Oranje']


	

		

familyTree = Tree("Beatrix_of_the_Netherlands")





