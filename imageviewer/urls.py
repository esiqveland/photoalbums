from django.conf.urls import patterns, url

from imageviewer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<album_id>\w+)/$', views.album, name='album'),
    url(r'^(?P<image_id>\w+)/$', views.image, name='image'),
    #url(r'^images/(?P<album_id>\w+)/$', views.images, name='images'),
)
