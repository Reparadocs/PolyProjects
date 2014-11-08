from django.db import models
from functions import iterableFromFile
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

CHOICE_LENGTH = 5

def get_expiration_date():
  return timezone.now() + datetime.timedelta(days=30)

class Skill(models.Model):
  name = models.CharField(max_length=30)

  def __unicode__(self):
    return self.name

class Category(models.Model):
  name = models.CharField(max_length=30)

  def __unicode__(self):
    return self.name

class Major(models.Model):
  name = models.CharField(max_length=30)

  def __unicode__(self):
    return self.name

class UserProfile(AbstractUser):
  major = models.ForeignKey(Major, null=True)
  contact = models.CharField(max_length=50, blank=True)

  def __init__(self, *args, **kwargs):
    super(AbstractUser, self).__init__(*args, **kwargs)

  def __unicode__(self):
    return self.username

class Listing(models.Model):
  owner = models.ForeignKey(UserProfile, related_name='owner')
  title = models.CharField(max_length=50)
  description = models.TextField()
  date_posted = models.DateTimeField(auto_now_add=True, blank=True)
  tags = models.CharField(max_length=100, blank=True)

  finished = models.BooleanField(default=False, blank=True)
  sponsored = models.BooleanField(default=False)

  project_type = models.CharField(max_length=CHOICE_LENGTH,
    choices=iterableFromFile('/choices/types.list'))
  poster_type = models.CharField(max_length=CHOICE_LENGTH,
    choices=iterableFromFile('/choices/posters.list'))
  category = models.ManyToManyField(Category,)
  skill = models.ManyToManyField(Skill,)

  team = models.ManyToManyField(UserProfile, related_name='team')

  def can_edit(self, user):
    return user == self.owner

  def __unicode__(self):
    return self.title

class Report(models.Model):
  listing = models.ForeignKey(Listing,)
  message = models.TextField(blank=True)

  def __unicode__(self):
    return self.listing.title

