from django.db import models
from functions import iterableFromFile
from django.contrib.auth.models import User

class Skill(models.Model):
  name = models.CharField(max_length=30)

class Category(models.Model):
  name = models.CharField(max_length=30)

class Listing(models.Model):
  CHOICE_LENGTH = 5
  owner = models.ForeignKey(User,)
  title = models.CharField(max_length=50)
  description = models.TextField()
  date_posted = models.DateTimeField(auto_now_add=True, blank=True)

  tags = models.CharField(max_length=100, blank=True)

  finished = models.BooleanField(default=False, blank=True)
  sponsored = models.BooleanField(default=False)

  name = models.CharField(max_length=100)
  major = models.CharField(max_length=CHOICE_LENGTH,
    choices=iterableFromFile('/choices/majors.list'))
  project_type = models.CharField(max_length=CHOICE_LENGTH,
    choices=iterableFromFile('/choices/types.list'))
  poster_type = models.CharField(max_length=CHOICE_LENGTH,
    choices=iterableFromFile('/choices/posters.list'))
  category = models.ManyToManyField(Category,)
  skill = models.ManyToManyField(Skill,)

  def can_edit(self, user):
    return user == self.owner
