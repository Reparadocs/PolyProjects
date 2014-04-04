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
