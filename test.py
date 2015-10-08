# test.py
import nltk.data

def main():
	textFile = open('beatrix.txt', 'r')
	
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	fp = open("beatrix.txt")
	data = fp.read()
	tokData = tokenizer.tokenize(data)
	#print(tokData)
	for line in tokData:
		#print(line)
	#print('\n'.join(tokenizer.tokenize(data)))

		if 'daughter of' in line:
			print(line)
		if 'son of' in line:
			print(line)
		if 'children' in line:
			print(line)

	# Probleem: afkortingen 'b. ' of 'Drs ' of 'ex. '
	


if __name__ == '__main__':
	main()

