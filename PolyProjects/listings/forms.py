from django.forms import ModelForm
from django import forms
from listings.models import Listing, Skill, Category, UserProfile

class UserForm(ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = UserProfile
    fields = ['username', 'email', 'password','first_name','last_name','major']

class ListingForm(ModelForm):
  skill = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Skill.objects.all()),
    widget=forms.CheckboxSelectMultiple)
  category = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Category.objects.all()),
    widget=forms.CheckboxSelectMultiple)
  class Meta:
    model = Listing
    fields = ['title', 'description', 'tags', 'sponsored',
              'project_type', 'poster_type', 'category', 'skill']

class SearchForm(ModelForm):
  skill = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Skill.objects.all()),
    widget=forms.CheckboxSelectMultiple)
  category = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Category.objects.all()),
    widget=forms.CheckboxSelectMultiple)
  class Meta:
    model = Listing
    fields = ['tags', 'sponsored','project_type', 
              'poster_type', 'category', 'skill']
