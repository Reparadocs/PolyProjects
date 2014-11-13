from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from listings.models import Listing, UserProfile, Report
from listings.forms import ListingForm, UserForm, SearchForm, ReportForm
from functions import sendMailToInnovation, delistify, listify
import datetime
from django.utils import timezone
import os
import requests

def login(request):
  if request.method != 'GET':
    raise PermissionDenied
  poly_id = request.GET.get('ticket','')
  if poly_id == '':
    return redirect('https://my.calpoly.edu/cas/login?service=https://mypolyprojects.com/login/')
  r = requests.get('https://my.calpoly.edu/cas/validate?ticket='+poly_id+'&service=https://mypolyprojects.com/login/')
  login_values = r.text.split()
  if login_values[0] == 'yes':
    try:
      user = UserProfile.objects.get(username=login_values[1])
      user.backend = 'django.contrib.auth.backends.ModelBackend'
      auth_login(request, user)
      return redirect(reverse('index'))
    except UserProfile.DoesNotExist:
      user = UserProfile.objects.create_user(login_values[1])
      user.backend = 'django.contrib.auth.backends.ModelBackend'
      auth_login(request, user)
      return redirect(reverse('listings.views.register'))
  else:
    return redirect('https://my.calpoly.edu/cas/login?service=https://mypolyprojects.com/login/')

def register(request):
  listings = Listing.objects.filter(owner=request.user)
  if request.method == 'POST':
    form = UserForm(data=request.POST, instance=request.user)
    if form.is_valid():
      user = request.user
      user.contact = form.cleaned_data['contact']
      user.first_name = form.cleaned_data['first_name']
      user.last_name = form.cleaned_data['last_name']
      user.major = form.cleaned_data['major']
      user.save()
      return redirect('/login/')
  else:
    form = UserForm()
  return render(request, 'users/register.html', {'form':form, 'listings': listings})
    
def index(request):
  if request.method == 'POST':
    form = SearchForm(request.POST)
    if form.is_valid():
      querystring = "?"
      skill = form.cleaned_data['skill']
      project_type = form.cleaned_data['project_type']
      poster_type = form.cleaned_data['poster_type']
      category = form.cleaned_data['category']
      major = form.cleaned_data['major']
      listing_list = Listing.objects.filter(
        project_type__icontains=project_type,
        poster_type__icontains=poster_type)
      querystring = "?project_type=" + project_type + "&poster_type=" + poster_type
      if skill != []:
        listing_list = listing_list.filter(skill__in=skill)
        querystring = querystring + "&skill=" + delistify(skill)
      if category != []:
        listing_list = listing_list.filter(category__in=category)
        querystring = querystring + "&category=" + delistify(category)
      if major != []:
        listing_list = listing_list.filter(major__in=major)
        querystring = querystring + "&major=" + delistify(major)
      listing_list = listing_list.order_by('-date_posted')
      paginator = Paginator(listing_list, 5)
      page = request.GET.get('page')
      try:
        listing_list = paginator.page(page)
      except PageNotAnInteger:
        listing_list = paginator.page(1)
      except EmptyPage:
        listing_list = paginator.page(paginator.num_pages)
      form = SearchForm()
      return render(request, 'listings/index.html', {'listing_list':listing_list, 'form':form,
        'querystring':querystring})
  else:
    form = SearchForm()
  skill_id = request.GET.get('skill','unset')
  major_id = request.GET.get('major','unset')
  project_type_id = request.GET.get('project_type','')
  cat_id = request.GET.get('category','unset')
  poster_type_id = request.GET.get('poster_type','')
  querystring1 = "?project_type=" + project_type_id + "&poster_type=" + poster_type_id
  querystring2 = "&skill=" + skill_id + "&category=" + cat_id + "&major=" + major_id
  querystring = querystring1 + querystring2
  listing_list = Listing.objects.filter(
    project_type__icontains=project_type_id,
    poster_type__icontains=poster_type_id, finished=False)
  if major_id != 'unset':
    listing_list = listing_list.filter(major__in=listify(major_id))
  if cat_id != 'unset':
    listing_list = listing_list.filter(category__in=listify(cat_id))
  if skill_id != 'unset':
    listing_list = listing_list.filter(skill__in=listify(skill_id))
  listing_list = listing_list.order_by('-date_posted')
  paginator = Paginator(listing_list, 5)
  page = request.GET.get('page')
  try:
    listing_list = paginator.page(page)
  except PageNotAnInteger:
    listing_list = paginator.page(1)
  except EmptyPage:
    listing_list = paginator.page(paginator.num_pages)
  return render(request, 'listings/index.html', {'listing_list':listing_list,'form':form,'querystring':querystring})

def detail(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  showedit = listing.can_edit(request.user)
  return render(request, 'listings/detail.html',
  {'listing':listing,'showedit':showedit})

def report(request, listing_id):
  reported_listing = Listing.objects.get(pk=listing_id)
  if request.method == 'POST':
    form = ReportForm(request.POST)
    if form.is_valid():
      report = form.save(commit=False)
      report.listing = reported_listing
      report.save()
      return redirect(reverse('report_thankyou',))
  else:
    form = ReportForm()
  return render(request, 'listings/report.html', {'form': form, 'reported_listing' : reported_listing})

@login_required
def create(request):
  if request.method == 'POST':
    form = ListingForm(request.POST)
    if form.is_valid():
      listing = form.save(commit=False)
      listing.owner = request.user
      listing.save()
      listing.team.add(request.user)
      form.save_m2m()
      if form.cleaned_data['innovation_sandbox'] is True:
        sendMailToInnovation(listing)
      return redirect(reverse('detail', args=(listing.id,)))
  else:
    form = ListingForm()
  return render(request, 'listings/create.html', {'form':form})

@login_required
def edit(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  if not listing.can_edit(request.user):
    raise PermissionDenied
  if request.method == 'POST':
    form = ListingForm(data=request.POST,instance=listing)
    if form.is_valid():
      listing = form.save()
      return redirect(reverse('detail', args=(listing.id,)))
  else:
    form = ListingForm(instance=listing)
  return render(request, 'listings/edit.html', {'form':form})  

#Endpoints
@login_required
def flip_finished(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  if not listing.can_edit(request.user):
    raise PermissionDenied
  listing.finished = not listing.finished
  listing.save()
  return redirect(reverse('detail', args=(listing.id,)))

  
#Static Views
def report_thankyou(request):
  return render(request, 'listings/report_thankyou.html')

def about(request):
  return render(request, 'info/about.html')

def calendar(request):
  return render(request, 'info/calendar.html')

def contact(request):
  return render(request, 'info/contact.html')

def faq(request):
  return render(request, 'info/faq.html')

def resources(request):
  return render(request, 'info/resources.html')
