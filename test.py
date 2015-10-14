# test.py
import nltk.data
import re


def main():
	textFile = open('beatrix.txt', 'r')

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
		
		if 'daughter of' in line:
			print(line)
		if 'son of' in line:
			print(line)
		if 'children' in line:
			print(line)


if __name__ == '__main__':
	main()

