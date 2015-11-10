#!/usr/bin/env python
import os
import json

def loadJson(gs2_list, filename):
	del gs2_list[:]
	with open(filename, 'r') as json_file:
		data = json.load(json_file)
		for f in data:
			tmpFile = GS2File()
			tmpFile.name = f["name"]
			
			for sec in f["sections"]:
				tmpSection = GS2Section()
				tmpSection.name = sec["name"]
				for propName, propValue in sec["properties"].iteritems():
					tmpSection.properties[propName] = propValue
				tmpFile.sections.append(tmpSection)
			gs2_list.append(tmpFile)

def saveJson(gs2_list, filename):
	with open(filename, "w") as json_file:
		json_file.write(str(gs2_list))

class GS2File(object):
	def __init__(self):
		self.name = None
		self.sections = []

	def __repr__(self):
		retStr = "{\"name\":\""+str(self.name)+"\", \"sections\":["
		for sect in self.sections[:-1]:
			retStr += str(sect) + ","
		retStr += str(self.sections[-1])
		retStr += "]}"

		return retStr

	def ProcessFile(self, filename):
		f = open(filename, 'r') # Open the file so we can read it
		self.name = unicode(os.path.split(filename)[1].strip(),'utf-8') # Set name of object
		currentSection = None
		curLine = 1
		maxLine = 100
		for line in f:

			if curLine > maxLine:
				pass
				#break

			# Skip blank lines
			if line.strip() == "":
				continue

			# Add section to file object
			if line.startswith("##"):
				if currentSection != None:
					self.sections.append(currentSection)
				
				currentSection = GS2Section()
				currentSection.name = unicode(line[2:].strip(),'utf-8') # Get Sectionname
			else:
				#Add property to section
				# print "name: '" + line[1:].split('=')[0].strip()+"', value: '"+ line[1:].split('=')[1].strip()+"'"
				currentSection.properties[unicode(line[1:].split('=')[0].strip(), 'utf-8', 'replace')] = unicode(line[1:].split('=')[1].strip(),'utf-8', 'replace')
			curLine+=1
		f.close()

class GS2Section(object):
		def __init__(self):
			self.name = None
			self.properties = {}

		def __repr__(self):
			return json.dumps(self.__dict__)
