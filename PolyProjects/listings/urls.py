from django.conf.urls import patterns, url
from listings import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^search/$', views.search, name='search'),
  url(r'^create/$', views.create, name='create'),
  url(r'^(?P<listing_id>[0-9]+)/$', views.detail, name='detail'),
)
