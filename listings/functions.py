import smtplib
import os
from listings.secret import Key
from email.mime.text import MIMEText
import random
import hashlib

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

def sendMail(receiver, subject, message, send=True):
  if send:
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = "PolyProjects"
    msg['To'] = receiver
    server = smtplib.SMTP('smtp.mailgun.org', 587)
    server.login("postmaster@" + Key.SMTP_EMAIL, Key.SMTP_PASSWORD)
    server.sendmail('admin@' + Key.SMTP_EMAIL,
      receiver, msg.as_string())

def sendMailToInnovation(listing):
  message = "Email: " + listing.owner.username + "\nTitle: " + listing.title + "\nDescription: " + listing.description

  #Uncomment when you have a final email
  #sendMail("reparadocs@gmail.com", "PolyProjects " + listing.title, message)

def delistify(arr):
  return ','.join([str(i) for i in arr])

def listify(arr):
  return [int(x) for x in arr.split(',')]
