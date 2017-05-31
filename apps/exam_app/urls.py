from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index),
  url(r'^popular$', views.popular),
  url(r'^secrets$', views.secrets),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^post$', views.post),
  url(r'^logout$', views.logout),
  url(r'^like/(?P<id>\d+)/(?P<sentby>\w+)$', views.like),
  url(r'^delete/(?P<id>\d+)/(?P<sentby>\w+)$', views.delete)
]
