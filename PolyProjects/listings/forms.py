from django.forms import ModelForm
from django import forms
from listings.models import Listing, Skill, Category
from django.contrib.auth.models import User

class UserForm(ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = User
    fields = ['username', 'email', 'password']

class ListingForm(ModelForm):
  skill = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Skill.objects.all()),
    widget=forms.CheckboxSelectMultiple)
  category = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Category.objects.all()),
    widget=forms.CheckboxSelectMultiple)
  class Meta:
    model = Listing
    fields = ['title', 'description', 'tags', 'sponsored', 'name',
      'major', 'project_type', 'poster_type', 'category', 'skill']

