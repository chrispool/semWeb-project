from SPARQLWrapper import SPARQLWrapper, JSON

class Sparql():
	def __init__(self, resource):
		self.PROPERTIES = ['mother', 'father', 'spouse', 'abstract']
		self.wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
		self.result = self.queryResource(resource)


	def queryResource(self, resource):
		rs = {}
		resource = "<http://dbpedia.org/resource/" + resource + ">"
		self.wrapper.setQuery("""	    
		PREFIX db: <http://dbpedia.org/resource/>
		select ?property ?value 
		where { 
		{
		   """ + resource + """ ?property ?value. 
		}

		}
		""")
		self.wrapper.setReturnFormat(JSON)
		results = self.wrapper.query().convert()

		for result in results['results']['bindings']:
			if any (prop in result['property']['value'] for prop in self.PROPERTIES): 
				rs[ self.cleanProperty(result['property']['value']) ] = (self.cleanProperty(result['value']['value']) ,result['value']['type'] )

		return rs

	def cleanProperty(self, prop):
		return str(prop.split("/")[-1])


if __name__ == "__main__":
	s = Sparql("Beatrix_of_the_Netherlands")
	print(s.result)
