def iterableFromFile(filename='choices/majors.list'):
  f = open(filename, 'r')
  lines = f.readlines()
  iterable = []
  for l in lines:
    splitchar = l.find(' ')
    keypair = [l[:splitchar],l[splitchar+1:].rsplit('\n')[0]]
    iterable.append(keypair)
  return iterable
