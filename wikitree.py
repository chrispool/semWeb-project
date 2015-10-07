from sparql import Sparql
from collections import defaultdict
import sys


class Tree:
#family tree
	
	def __init__(self, firstPerson):
		self.allFamilyMembers = {}
		self.processNextFamilyMember(firstPerson)
		parents = tuple( (self.allFamilyMembers[firstPerson].getFather()[0], self.allFamilyMembers[firstPerson].getMother()[0] ))
		self.traverseTree([parents])
		
	
	def processNextFamilyMember(self, person, remaingPersons = set()):
		#add person
		self.allFamilyMembers[person] = Person(person)
		#print( "{} {} - {} ".format(person, len(self.allFamilyMembers.keys()), len(remaingPersons)))
		#get relatives from this person
		relatives = self.allFamilyMembers[person].returnFamilyMembers()

		#add relatives that are not allready retrieved to remainingperson list
		if len(relatives) > 0:
			remaingPersons |= set([relative for relative in relatives if relative not in self.allFamilyMembers])	
				
		#process new person from list is there are any
		if len(remaingPersons) > 0:		
			self.processNextFamilyMember(remaingPersons.pop(), remaingPersons)	
		#else print the tree
		else:
			for key in self.allFamilyMembers:
				pass
				#print(self.allFamilyMembers[key])


		
	def traverseTree(self, parents, result = []):
		newList = []
		val = []
		result.append(parents)
		for parent in parents:
			father = parent[0] 
			mother = parent[1]

			
			if father == 'Unknown':
				motherOfFather = 'Unknown'
				fatherOfFather = 'Unknown'
			else:
				motherOfFather = self.allFamilyMembers[str(father)].getFather()[0]
				fatherOfFather = self.allFamilyMembers[str(father)].getMother()[0]
			
			if mother == 'Unknown':
				motherOfMother = 'Unknown'
				fatherOfMother = 'Unknown'
			else:
				motherOfMother = self.allFamilyMembers[str(mother)].getFather()[0]
				fatherOfMother = self.allFamilyMembers[str(mother)].getMother()[0]

			val.extend([fatherOfFather, motherOfFather, fatherOfMother, motherOfMother]) 
			l = [(fatherOfFather, motherOfFather) , (fatherOfMother, motherOfMother)]
				
			newList.extend(l)
		
	
		
		if len(set(val)) == 1 and 'Unknown' in set(val):
			print("Finished")
			self.printTree(result)
		else:
			self.traverseTree(newList, result)
		




		#self.traverseTree(self.allFamilyMembers[str(father[0])].getFather(), self.allFamilyMembers[str(mother[0])].getMother())

	def printTree(self, result):
		lengthStart = len(result[-1])
		colspan = 0.5
		for i, row in enumerate(reversed(result)):
			colspan = colspan * 2
			print("<tr>")
			for father,mother in row:
				print("<td colspan=" + str(int(colspan)) + ">" + father + " - " + mother + "</td>")
			print("</tr>")
			print()
			



			
		

		


class Person:
#nodes in the tree
	def __init__(self, person):
		
		self.name = person
		wiki = getWikiInfo(person)
		self.spouse = wiki.getSpouse()
		self.mother = wiki.getMother()
		self.father = wiki.getFather()
		self.fullName = wiki.getFullName()
		self.abstract = wiki.getAbstract()

	def getFather(self):
		return self.father
	
	def getMother(self):
		return self.mother
	
	def getSpouse(self):
		return self.spouse


	def __str__(self):
		return "{} ---> S= {}, M = {}, F = {} ".format(self.fullName[0], self.spouse, self.mother, self.father) 

	def returnFamilyMembers(self):	
		#properties = [self.mother , self.father , self.spouse]
		properties = [self.mother, self.father, self.spouse]
		if len(properties[0]) > 0 :
			
			return [value for value, propType in properties if propType == "uri"]
		else:
			return []

	def getFullName(self):
		return self.fullNamels

class getWikiInfo:
#retrieves the family from wiki text and infoboxes

	def __init__(self, person):
		#print(person)
		self.person = person
		self.query = Sparql(person)
		self.setSpouse()
		self.setMother()
		self.setFather()
		self.setFullName()
		self.setAbstract()
	

	def setSpouse(self):
		if 'spouse' in self.query.result:
			self.spouse = list(self.query.result['spouse'])
		else:
			self.spouse = ['Unknown', 'literal']	
	
	def setMother(self):
		if 'mother' in self.query.result:
			self.mother = list(self.query.result['mother'])
		else:
			self.mother = ['Unknown', 'literal']
	
	def setFather(self):
		if 'father' in self.query.result:
			self.father = list(self.query.result['father'])
		else:
			self.father = ['Unknown', 'literal']

	def setFullName(self):
		if 'fullName' in self.query.result:
			self.fullName = list(self.query.result['fullName'])
		else:
			self.fullName = [self.person, 'literal']	

	def setAbstract(self):
		if 'abstract' in self.query.result:
			self.abstract = list(self.query.result['abstract'])
		else:
			self.abstract = ['Unknown', 'literal']	
		
	def getSpouse(self):
		return self.spouse
	
	def getMother(self):
		return self.mother

	def getFather(self):
		return self.father

	def getFullName(self):
		return self.fullName

	def getAbstract(self):
		return self.abstract


	

		
sys.setrecursionlimit(10000)
#familyTree = Tree("Beatrix_of_the_Netherlands")
familyTree = Tree("Caesarion")





