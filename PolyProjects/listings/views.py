from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from listings.models import Listing
from listings.forms import ListingForm

def index(request):
  return render(request, 'listings/index.html')

def search(request):
  skill_id = request.GET.get('skill','')
  major_id = request.GET.get('major','')
  type_id = request.GET.get('type','')
  cat_id = request.GET.get('cat','')
  ptype_id = request.GET.get('ptype','')
  sponsor_id = request.GET.get('sponsor','unset')
  finish_id = 'true' == request.GET.get('finish','false')
  listing_list = Listing.objects.filter(skill__icontains=skill_id,
    major__icontains=major_id, project_type__icontains=type_id,
    category__icontains=cat_id, poster_type__icontains=ptype_id,
    finished=finish_id)
  if sponsor_id != 'unset':
    sponsor_id = 'true' == sponsor_id
    listing_list = listing_list.filter(sponsored=sponsor_id)
  return render(request, 'listings/search.html', {'listing_list':listing_list})

def detail(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  return render(request, 'listings/detail.html', {'listing':listing})

def create(request):
  if request.method == 'POST':
    form = ListingForm(request.POST)
    if form.is_valid():
      listing = form.save()
      return redirect(reverse('detail', args=(listing.id,)))
  else:
    form = ListingForm()
  return render(request, 'listings/create.html', {'form':form})
