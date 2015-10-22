# test.py
import nltk.data
from nltk.tag.stanford import NERTagger 
import re


def main():
	textFile = open('beatrix.txt', 'r')
	classifier = "ner/classifiers/" + "english.all.3class.distsim.crf.ser.gz"
	jar = "ner/stanford-ner-3.4.jar"
	tagger = NERTagger(classifier, jar)
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	fp = open("beatrix.txt")
	data = fp.read()

	tokData = tokenizer.tokenize(data)
	
	i = -1
	for line in tokData:
		i = i + 1
		m = re.search('([^a-z][a-z]\.)', line)
		if m:
			line = line[:-1] + ';;'
			tokData[i] = line
			
	newData = ' '.join(tokData)
	
	tokData = tokenizer.tokenize(newData)
		
	for line in tokData:
		words = ['daughter of', 'son of', 'child of']
		
		# daughter of, son of, child of
		if any(x in line for x in words):
			tagLine(line, 'Mother/Father', tagger)
		



def tagLine(line, name, tagger):
	for line in tagger.tag(line.split()):
		for word in line:
			if word[1] == 'PERSON':
				print(word[0])

if __name__ == '__main__':
	main()

