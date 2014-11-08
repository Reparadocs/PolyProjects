from django.conf.urls import patterns, url
from listings import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  #url(r'^search/$', views.search, name='search'),
  url(r'^create/$', views.create, name='create'),
  url(r'^(?P<listing_id>[0-9]+)/$', views.detail, name='detail'),
  url(r'^edit/(?P<listing_id>[0-9]+)/$', views.edit, name='edit'),
  url(r'^report/(?P<listing_id>[0-9]+)/$', views.report, name='report'),
  url(r'^report_thankyou/$', views.report_thankyou, name='report_thankyou'),
  url(r'^flip_finished/(?P<listing_id>[0-9]+)/$', views.flip_finished, name='flip_finished'),
)
