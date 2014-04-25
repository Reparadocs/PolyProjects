import os

def iterableFromFile(filename):
  filepath = os.path.dirname(os.path.abspath(__file__)) + filename
  f = open(filepath, 'r')
  lines = f.readlines()
  iterable = []
  for l in lines:
    splitchar = l.find(' ')
    keypair = [l[:splitchar],l[splitchar+1:].rsplit('\n')[0]]
    iterable.append(keypair)
  return iterable

def listFromFile(filename):
  filepath = os.path.dirname(os.path.abspath(__file__)) + filename
  f = open(filepath, 'r')
  lines = f.readlines()
  returnList = [] 
  for l in lines:
    returnList.append(l)
  return returnList

def createYAMLFixture(infile, outfile, app):
  yList = listFromFile(infile)
  filepath = os.path.dirname(os.path.abspath(__file__)) + outfile
  f = open(filepath, 'w')
  for i in range(len(yList)):
    f.write("- model: {}\n  pk: {}\n  fields:\n".format(app,i+1))
    f.write("    name: {}\n".format(yList[i]))
  f.close()

