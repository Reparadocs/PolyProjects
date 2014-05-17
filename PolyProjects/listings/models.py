from django.db import models
from functions import iterableFromFile
from django.contrib.auth.models import User

class Skill(models.Model):
  name = models.CharField(max_length=30)

class Category(models.Model):
  name = models.CharField(max_length=30)

class Listing(models.Model):
  CHOICE_LENGTH = 5
  owner = models.ForeignKey(User, related_name='owner')
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

  team = models.ManyToManyField(User, related_name='team')

  def can_edit(self, user):
    return user == self.owner

class Notification(models.Model):
  message = models.CharField(max_length=200)
  user = models.ForeignKey(User,)

class JoinNotification(Notification):
  listing = models.ForeignKey(Listing,)
  requester = models.ForeignKey(User,)
