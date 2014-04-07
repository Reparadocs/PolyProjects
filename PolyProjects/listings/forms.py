from django.forms import ModelForm
from listings.models import Listing

class ListingForm(ModelForm):
  class Meta:
    model = Listing
    fields = ['title', 'description', 'tags', 'sponsored',
      'major', 'project_type', 'poster_type', 'category', 'skill']

