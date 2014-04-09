from django.forms import ModelForm
from listings.models import Listing
from django.contrib.auth.models import User

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password']

class ListingForm(ModelForm):
  class Meta:
    model = Listing
    fields = ['title', 'description', 'tags', 'sponsored',
      'major', 'project_type', 'poster_type', 'category', 'skill']

