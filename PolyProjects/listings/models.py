from django.db import models
from functions import iterableFromFile
from django.contrib.auth.models import AbstractUser

CHOICE_LENGTH = 5

class NotificationType():
  DEFAULT = 0
  JOIN_REQUEST = 1

class Skill(models.Model):
  name = models.CharField(max_length=30)

class Category(models.Model):
  name = models.CharField(max_length=30)

class UserProfile(AbstractUser):
  major = models.CharField(max_length=CHOICE_LENGTH,
    choices=iterableFromFile('/choices/majors.list'))

  def get_unread_notifications(self):
    return self.notification_set.filter(completed=False)

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

class Notification(models.Model):
  message = models.CharField(max_length=200)
  receiver = models.ForeignKey(UserProfile, )
  completed = models.BooleanField(default=False)
  sender = models.ForeignKey(UserProfile, blank=True, null=True, related_name='sender')
  listing = models.ForeignKey(Listing, blank=True, null=True)
  ntype = models.IntegerField(default=NotificationType.DEFAULT)

  def can_edit(self, user):
    return user == self.receiver

