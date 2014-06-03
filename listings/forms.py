from django.forms import ModelForm
from django import forms
from functions import iterableFromFile
from listings.models import Listing, Skill, Category, UserProfile, Major

class UserForm(ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  major = forms.ModelChoiceField(queryset=Major.objects.all())
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

class SearchForm(forms.Form):
  skill = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Skill.objects.all()),
    widget=forms.CheckboxSelectMultiple, required=False)
  category = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Category.objects.all()),
    widget=forms.CheckboxSelectMultiple, required=False)
  tags = forms.CharField(required=False)
  sponsored = forms.BooleanField(required=False)
  project_type = forms.ChoiceField(choices=[('','-----')]+iterableFromFile('/choices/types.list'), 
    required=False)
  poster_type = forms.ChoiceField(choices=[('','-----')]+iterableFromFile('/choices/posters.list'), 
    required=False)

  def clean(self):
    super(forms.Form, self).clean()
    if 'skill' not in self.cleaned_data:
      self.cleaned_data['skill'] = ''
    if 'category' not in self.cleaned_data:
      self.cleaned_data['category'] = ''
    if 'tags' not in self.cleaned_data:
      self.cleaned_data['tags'] = ''
    return self.cleaned_data
