from django.forms import ModelForm
from django import forms
from functions import iterableFromFile
from listings.models import Listing, Skill, Category, UserProfile, Major
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import math
from itertools import chain

class ColumnCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """
    Widget that renders multiple-select checkboxes in columns.
    Constructor takes number of columns and css class to apply
    to the <ul> elements that make up the columns.
    """
    def __init__(self, columns=2, css_class=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.columns = columns
        self.css_class = css_class

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        choices_enum = list(enumerate(chain(self.choices, choices)))
        
        # This is the part that splits the choices into columns.
        # Slices vertically.  Could be changed to slice horizontally, etc.
        column_sizes = columnize(len(choices_enum), self.columns)
        columns = []
        for column_size in column_sizes:
            columns.append(choices_enum[:column_size])
            choices_enum = choices_enum[column_size:]
        output = []
        for column in columns:
            if self.css_class:
                output.append(u'<ul class="%s">' % self.css_class)
            else:
                output.append(u'<ul>')
            # Normalize to strings
            str_values = set([force_unicode(v) for v in value])
            for i, (option_value, option_label) in column:
                # If an ID attribute was given, add a numeric index as a suffix,
                # so that the checkboxes don't all have the same ID attribute.
                if has_id:
                    final_attrs = dict(final_attrs, id='%s_%s' % (
                            attrs['id'], i))
                    label_for = u' for="%s"' % final_attrs['id']
                else:
                    label_for = ''

                cb = forms.CheckboxInput(
                    final_attrs, check_test=lambda value: value in str_values)
                option_value = force_unicode(option_value)
                rendered_cb = cb.render(name, option_value)
                option_label = conditional_escape(force_unicode(option_label))
                output.append(u'<li><label%s>%s %s</label></li>' % (
                        label_for, rendered_cb, option_label))
            output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))


def columnize(items, columns):
    """
    Return a list containing numbers of elements per column if `items` items
    are to be divided into `columns` columns.

    >>> columnize(10, 1)
    [10]
    >>> columnize(10, 2)
    [5, 5]
    >>> columnize(10, 3)
    [4, 3, 3]
    >>> columnize(3, 4)
    [1, 1, 1, 0]
    """
    elts_per_column = []
    for col in range(columns):
        col_size = int(math.ceil(float(items) / columns))
        elts_per_column.append(col_size)
        items -= col_size
        columns -= 1
    return elts_per_column


class UserForm(ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  major = forms.ModelChoiceField(queryset=Major.objects.all())
  class Meta:
    model = UserProfile
    fields = ['username', 'email', 'password','first_name','last_name','major','email_notifications']

class ListingForm(ModelForm):
  skill = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Skill.objects.all()),
    widget=ColumnCheckboxSelectMultiple(css_class="columns"))
  category = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Category.objects.all()),
    widget=ColumnCheckboxSelectMultiple(css_class="columns"))
  class Meta:
    model = Listing
    fields = ['title', 'description', 'tags', 'sponsored',
              'project_type', 'poster_type', 'category', 'skill']

class SearchForm(forms.Form):
  skill = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Skill.objects.all()),
    widget=ColumnCheckboxSelectMultiple(css_class="columns"), required=False)
  category = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Category.objects.all()),
    widget=ColumnCheckboxSelectMultiple(css_class="columns"), required=False)
  major = forms.MultipleChoiceField(choices=((x.id, x.name) for x in Major.objects.all()),
    widget=ColumnCheckboxSelectMultiple(css_class="columns"), required=False)
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
    if 'major' not in self.cleaned_data:
      self.cleaned_data['category'] = ''
    if 'tags' not in self.cleaned_data:
      self.cleaned_data['tags'] = ''
    return self.cleaned_data
