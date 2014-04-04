from django.db import models
from functions import iterableFromFile

class Listing(models.Model):
  CHOICE_LENGTH = 3
  name = models.CharField(max_length=50)
  description = models.TextField()
  date_posted = models.DateTimeField(auto_now_add=True, blank=True)
  
  tags = models.CharField(max_length=100)

  finished = models.BooleanField(default=False, blank=True)
  sponsored = models.BooleanField(default=False)

  major = models.CharField(max_length=CHOICE_LENGTH, 
    choices=iterableFromFile('./choices/majors.list'))
  project_type = models.CharField(max_length=CHOICE_LENGTH, 
    choices=iterableFromFile('choices/types.list'))
  poster_type = models.CharField(max_length=CHOICE_LENGTH,
     choices=iterableFromFile('choices/posters.list'))
  category = models.CharField(max_length=CHOICE_LENGTH,
     choices=iterableFromFile('choices/categories.list'))
  skill = models.CharField(max_length=CHOICE_LENGTH,
     choices=iterableFromFile('choices/skills.list'))
