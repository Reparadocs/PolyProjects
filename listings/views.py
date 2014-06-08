from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from listings.models import Listing, Notification, UserProfile, NotificationType
from listings.forms import ListingForm, UserForm, SearchForm
from functions import sendMail
import datetime
from django.utils import timezone
import os

def register(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      user = UserProfile.objects.create_user(form.cleaned_data['username'],
        form.cleaned_data['email'], form.cleaned_data['password'])
      user.first_name = form.cleaned_data['first_name']
      user.last_name = form.cleaned_data['last_name']
      user.major = form.cleaned_data['major']
      user.email_notifications = form.cleaned_data['email_notifications']
      user.save()
      if user.email_notifications:
        verify_msg = os.environ['BASE_URL'] + "/verify_email/?verify={}".format(user.email_verification_code)
        sendMail(user.email, 'Verify Your Email', verify_msg)
      return redirect('/login/')
  else:
    form = UserForm()
  return render(request, 'users/register.html', {'form':form})
    
def index(request):
  if request.method == 'POST':
    form = SearchForm(request.POST)
    if form.is_valid():
      skill = form.cleaned_data['skill']
      project_type = form.cleaned_data['project_type']
      poster_type = form.cleaned_data['poster_type']
      category = form.cleaned_data['category']
      sponsored = form.cleaned_data['sponsored']
      listing_list = Listing.objects.filter(
        project_type__icontains=project_type,
        poster_type__icontains=poster_type,
        sponsored=sponsored)
      if skill != []:
        listing_list = listing_list.filter(skill__in=skill)
      if category != []:
        listing_list = listing_list.filter(category__in=category)
      print listing_list
      return render(request, 'listings/search.html', {'listing_list':listing_list})
  else:
    form = SearchForm()
  listing_list = Listing.objects.filter(finished=False)
  return render(request, 'listings/index.html', {'listing_list':listing_list,'form':form})

def detail(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  showedit = listing.can_edit(request.user)
  return render(request, 'listings/detail.html', {'listing':listing,'showedit':showedit})

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

@login_required
def notifications(request):
  notification_list = request.user.notification_set.filter(completed=False)
  return render(request, 'users/notifications.html', {'notification_list':notification_list})

#Endpoints
@login_required
def flip_finished(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  if not listing.can_edit(request.user):
    raise PermissionDenied
  listing.finished = not listing.finished
  if listing.finished == True:
    listing.expiration_date = timezone.now() + datetime.datetime.now()
  listing.save()
  return redirect(reverse('detail', args=(listing.id,)))

@login_required
def verify_email(request):
  verify = request.GET.get('verify','')
  if verify == request.user.email_verification_code:
    request.user.email_verified = True
    request.user.save()
  return redirect(reverse('index'))

#Notification Views
@login_required
def join_request(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  msg = "{} wants to joing the team for {}!".format(request.user.first_name, listing.title)
  notification = Notification(receiver=listing.owner, sender=request.user, 
    message=msg, listing=listing, ntype=NotificationType.JOIN_REQUEST)
  sendMail(listing.owner.email, msg, os.environ['BASE_URL'] + "listings/notifications/",
    listing.owner.email_verified and listing.owner.email_notifications)
  notification.save()
  return redirect(reverse('detail', args=(listing.id,)))


@login_required
def accept_join_request(request, notification_id):
  notification = get_object_or_404(Notification, pk=notification_id)
  if not notification.listing.can_edit(request.user):
    raise PermissionDenied
  notification.completed=True
  notification.save()
  notification.listing.team.add(notification.sender)
  msg = "Your request to join the team for {} has been accepted!".format(notification.listing.title)
  new_notification = Notification(receiver=notification.sender, sender=request.user, message=msg)
  sendMail(notification.sender.email, msg, os.environ['BASE_URL'] + "/detail/" + notification.listing.id,
    notification.sender.email_verified and notification.sender.email_notifications)
  new_notification.save()
  return redirect(reverse('notifications'))

@login_required
def decline_join_request(request, notification_id):
  notification = get_object_or_404(Notification, pk=notification_id)
  if not notification.listing.can_edit(request.user):
    raise PermissionDenied
  notification.completed=True
  notification.save()
  msg = "Your request to join the team for {} has been denied. Sorry :(".format(notification.listing.title)
  new_notification = Notification(receiver=notification.sender, sender=request.user,
    message=msg)
  sendMail(notification.sender.email, msg, os.environ['BASE_URL'] + "/detail/" + notification.listing.id,
    notification.sender.email_verified and notification.sender.email_notifications)
  new_notification.save()
  return redirect(reverse('notifications'))

@login_required
def complete_notification(request, notification_id):
  notification = get_object_or_404(Notification, pk=notification_id)
  if not notification.can_edit(request.user):
    raise PermissionDenied
  notification.completed=True
  notification.save()
  return redirect(reverse('notifications'))

@login_required
def renew_listing_notification(request, notification_id):
  notification = get_object_or_404(Notification, pk=notification_id)
  if not notification.can_edit(request.user):
    raise PermissionDenied
  notification.completed=True
  notification.save()
  notification.listing.expiration_date = timezone.now() + datetime.timedelta(days=30)
  notification.listing.finished=False
  notification.listing.save()
  return redirect(reverse('notifications'))

@login_required
def finish_listing_notification(request, notification_id):
  notification = get_object_or_404(Notification, pk=notification_id)
  if not notification.can_edit(request.user):
    raise PermissionDenied
  notification.completed=True
  notification.save()
  notification.listing.finished=True
  notification.listing.save()
  return redirect(reverse('notifications'))

@login_required
def renew_listing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  if not listing.can_edit(request.user):
    raise PermissionDenied
  listing.expiration_date = timezone.now() + datetime.timedelta(days=30)
  listing.finished=False
  listing.save()
  return redirect(reverse('detail', args=(listing.id,)))

#Static Views
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
