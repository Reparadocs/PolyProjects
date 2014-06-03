from django.conf.urls import patterns, url
from listings import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  #url(r'^search/$', views.search, name='search'),
  url(r'^create/$', views.create, name='create'),
  url(r'^(?P<listing_id>[0-9]+)/$', views.detail, name='detail'),
  url(r'^edit/(?P<listing_id>[0-9]+)/$', views.edit, name='edit'),
  url(r'^notifications/$', views.notifications, name='notifications'),
  url(r'^flip_finished/(?P<listing_id>[0-9]+)/$', views.flip_finished, name='flip_finished'),
  url(r'^join_request/(?P<listing_id>[0-9]+)/$', views.join_request, name='join_request'),
  url(r'^accept_join_request/(?P<notification_id>[0-9]+)/$', views.accept_join_request, name='accept_join_request'),
  url(r'^decline_join_request/(?P<notification_id>[0-9]+)/$', views.decline_join_request, name='decline_join_request'),
  url(r'^complete_notification/(?P<notification_id>[0-9]+)/$', views.complete_notification, name='complete_notification'),
  url(r'^renew_listing/(?P<listing_id>[0-9]+)/$', views.renew_listing, name='renew_listing'),
  url(r'^renew_listing_notification(?P<notification_id>[0-9]+)/$', views.renew_listing_notification, name='renew_listing_notification'),
  url(r'^finish_listing_notification/(?P<notification_id>[0-9]+)/$', views.finish_listing_notification, name='finish_listing_notification'),
)
