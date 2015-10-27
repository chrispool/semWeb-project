from sparql import Sparql
from collections import defaultdict
import sys
import nltk
from nltk.tag import StanfordNERTagger 
import re
import wikipedia


class Tree:
#family tree
	
	def __init__(self, firstPerson):
		
		self.maxIter = 100
		self.allFamilyMembers = {}
		self.processNextFamilyMember(firstPerson)
		parents = tuple( (self.allFamilyMembers[firstPerson].getFather()[0], self.allFamilyMembers[firstPerson].getMother()[0], self.allFamilyMembers[firstPerson].getAbstractParents() ))
		self.traverseTree([parents])
		
	
	def processNextFamilyMember(self, person, remaingPersons = set()):
		#print(person, len(self.allFamilyMembers.keys()))
		#add person
		self.allFamilyMembers[person] = Person(person)
		#print( "{} {} - {} ".format(person, len(self.allFamilyMembers.keys()), len(remaingPersons)))
		#get relatives from this person
		relatives = self.allFamilyMembers[person].returnFamilyMembers()

		#add relatives that are not allready retrieved to remainingperson list
		if len(relatives) > 0:
			remaingPersons |= set([relative for relative in relatives if relative not in self.allFamilyMembers])	
		

		if len(self.allFamilyMembers.keys()) > self.maxIter:
			remaingPersons = set()
		
		#process new person from list is there are any
		if len(remaingPersons) > 0:		
			self.processNextFamilyMember(remaingPersons.pop(), remaingPersons)	
		


		
	def traverseTree(self, parents, result = []):
		newList = []
		val = []
		result.append(parents)
		for parent in parents:
			
			father = parent[0] 
			mother = parent[1]

			
			if str(father) == 'Unknown':
				motherOfFather = 'Unknown'
				fatherOfFather = 'Unknown'
				fatherAbsParents = 'Unknown'
			else:
				if father in self.allFamilyMembers:
					motherOfFather = self.allFamilyMembers[str(father)].getFather()[0]
					fatherOfFather = self.allFamilyMembers[str(father)].getMother()[0]
					fatherAbsParents = self.allFamilyMembers[str(father)].getAbstractParents()
				else:
					motherOfFather = 'Unknown'
					fatherOfFather = 'Unknown'
					fatherAbsParents = 'Unknown'
			



			
			if str(mother) == 'Unknown':
				motherOfMother = 'Unknown'
				fatherOfMother = 'Unknown'
				motherAbsParents = 'Unknown'
			else:
				if mother in self.allFamilyMembers:
					motherOfMother = self.allFamilyMembers[str(mother)].getFather()[0]
					fatherOfMother = self.allFamilyMembers[str(mother)].getMother()[0]
					motherAbsParents = self.allFamilyMembers[str(mother)].getAbstractParents()
				else:
					motherOfMother = 'Unknown'
					fatherOfMother = 'Unknown'
					motherAbsParents = 'Unknown'
			
			val.extend([fatherOfFather, motherOfFather, fatherOfMother, motherOfMother])

			l = [(fatherOfFather, motherOfFather, fatherAbsParents) , (fatherOfMother, motherOfMother, motherAbsParents)]
			#l = [(fatherOfFather, motherOfFather) , (fatherOfMother, motherOfMother)]	
			newList.extend(l)
		
	
		
		if len(set(val)) == 1 and 'Unknown' in set(val):
			#pass
			self.printTree(result)
		else:
			self.traverseTree(newList, result)
	
	def printTree(self, result):
		nRows = len(result[-1])
		
		i = 0
		x = nRows
		trList = [x]
		while x is not 1:
			x = int(x / 2)
			trList.append(x)
			i += 1
		nCols = i + 1



		print(""" <html>
				<head>
				<style>
				table {
					font-size:10px;
					margin:0px;
					padding:0px;
					border:none;
				}

				.couple  {
					border: 1px solid;
					height: 30px;
					margin:10px;

				}

				.space {

				}
				</style>
				</head>
				<body>
				<table>
				<tr>
		""")

		for i, row in enumerate(result):
			print("<td>")
			print("<table>")
			for father, mother, absParents in row:
				if father == 'Unknown':
					father = "*"
				if mother == 'Unknown':
					mother = "*"

				print("<tr><td class='couple'> " + father + " - " +  mother + " (" + absParents +  ")</td></tr>")
							
			print("</table>")
			print("</td>")
				
				
				
		print(""" 
			</tr>
			</table>
			</body>
			</html>
		""")
	
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
		self.abstractParents = wiki.getAbstractParents()
		

	def getAbstractParents(self):
		return self.abstractParents

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
		properties = [self.mother, self.father]
		if len(properties[0]) > 0 :
			
			return [value for value, propType in properties if propType == "uri"]
		else:
			return []

	def getFullName(self):
		return self.fullNamels

class getWikiInfo:
#retrieves the family from wiki text and infoboxes
	

	def __init__(self, person):
		
		self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		classifier = "ner/classifiers/" + "english.all.3class.distsim.crf.ser.gz"
		jar = "ner/stanford-ner-3.4.jar"
		self.tagger = StanfordNERTagger(classifier, jar)
		self.ap = []
		self.person = person
		self.query = Sparql(person)
		self.setSpouse()
		self.setMother()
		self.setFather()
		self.setFullName()
		self.setAbstract()
		self.setAbstractInfo()

	def setAbstractInfo(self):
		try:
			conObj = wikipedia.page(self.person)
			content = conObj.content
		except wikipedia.exceptions.DisambiguationError as e:
			content = None
		except wikipedia.exceptions.PageError as e:
			content = None
		
		

		if content:
			for sentence in self.tokenizer.tokenize(content):
				words = ['daughter of', 'son of', 'child of']
				
				# daughter of, son of, child of
				if any(x in sentence for x in words):
					person = ''
					for tag in self.tagger.tag(sentence.split()):
							
						if tag[1] == 'PERSON':
							person = person + " " + tag[0]
						else:
							if not person == '':
								self.ap.append(person)
							person = ''

		

	def getAbstractParents(self):
		if len(self.ap) > 0:
			return ", " .join(set(self.ap))
		else:
			return "Unknown"


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


	

		
#sys.setrecursionlimit(100000)
familyTree = Tree("Beatrix_of_the_Netherlands")
#familyTree = Tree("Caesarion")





