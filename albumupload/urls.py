from django.conf.urls import patterns, url

from albumupload import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^upload$', views.upload, name='upload'),

    #url(r'^images/(?P<album_id>\w+)/$', views.images, name='images'),
)
