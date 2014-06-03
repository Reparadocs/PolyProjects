import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PolyProjects.settings")
from django.conf import settings

from listings.models import Notification,Listing,NotificationType
from listings.functions import sendMail
import datetime
from django.utils import timezone

#Run in heroku scheduler daily
def updateListingsExpiration():
  listings = Listing.objects.filter(finished=False)
  for l in listings:
    if l.expiration_date < timezone.now():
      msg = "{} has just expired".format(l.title)
      notification = Notification(receiver=l.owner,
        message=msg, listing=l, 
        ntype=NotificationType.EXPIRATION_NOTICE)
      notification.save()
      sendMail(l.owner.email, "Your Listing Has Expired!", msg)
      l.finished = True
      l.save()
    elif l.expiration_date - datetime.timedelta(days=5) < timezone.now():
      msg = "{} is going to expire soon!".format(l.title)
      sendMail(l.owner.email, "Your Listing will expire soon!", msg)
      notification = Notification(receiver=l.owner,
        message=msg, listing=l, 
        ntype=NotificationType.EXPIRATION_NOTICE)
      notification.save()
    elif l.expiration_date - datetime.timedelta(days=10) < timezone.now():
      notification = Notification(receiver=l.owner,
        message="{} is going to expire soon!".format(l.title), listing=l, 
        ntype=NotificationType.EXPIRATION_NOTICE)
      notification.save()

updateListingsExpiration()