from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from listings.models import Listing
from listings.forms import ListingForm, UserForm

def register(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(form.cleaned_data['username'],
        form.cleaned_data['email'], form.cleaned_data['password'])
      user.save()
      return redirect('/login/')
  else:
    form = UserForm()
  return render(request, 'users/register.html', {'form':form})
    
def index(request):
  listing_list = Listing.objects.all()
  return render(request, 'listings/index.html', {'listing_list':listing_list})

def search(request):
  skill_id = request.GET.get('skill','unset')
  major_id = request.GET.get('major','')
  type_id = request.GET.get('type','')
  cat_id = request.GET.get('cat','unset')
  ptype_id = request.GET.get('ptype','')
  sponsor_id = request.GET.get('sponsor','unset')
  finish_id = 'true' == request.GET.get('finish','false')
  listing_list = Listing.objects.filter(
    major__icontains=major_id, project_type__icontains=type_id,
    poster_type__icontains=ptype_id,
    finished=finish_id)
  if sponsor_id != 'unset':
    sponsor_id = 'true' == sponsor_id
    listing_list = listing_list.filter(sponsored=sponsor_id)
  if cat_id != 'unset':
    listing_list = listing_list.filter(category__in=cat_id)
  if skill_id != 'unset':
    listing_list = listing_list.filter(skill__in=skill_id)
  return render(request, 'listings/search.html', {'listing_list':listing_list})

def detail(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  showedit = listing.can_edit(request.user)
  return render(request, 'listings/detail.html', {'listing':listing,'showedit':showedit})

@login_required(login_url='/login/')
def create(request):
  if request.method == 'POST':
    form = ListingForm(request.POST)
    if form.is_valid():
      listing = form.save(commit=False)
      listing.owner = request.user;
      listing.save()
      form.save_m2m()
      return redirect(reverse('detail', args=(listing.id,)))
  else:
    form = ListingForm()
  return render(request, 'listings/create.html', {'form':form})

@login_required(login_url='/login/')
def edit(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  if not listing.can_edit(request.user):
    raise PermissionDenied;
  if request.method == 'POST':
    form = ListingForm(data=request.POST,instance=listing)
    if form.is_valid():
      listing = form.save()
      return redirect(reverse('detail', args=(listing.id,)))
  else:
    form = ListingForm(instance=listing)
  return render(request, 'listings/edit.html', {'form':form})  

@login_required(login_url='/login')
def notifications(request):
  return render(request, 'users/notifications.html')

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
