from django.http import HttpResponse
from django.template import RequestContext, loader
from imageviewer.models import Album_Store, Image_Store, Image_Tags
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404

def index(request):
    last_albums = Album_Store.objects.order_by('name')[:5]
    album_images = []
    for album in last_albums:
        list_images = get_list_or_404(Image_Store,  album=album.id)
        if list_images:
            headline = (album, list_images)
            print list_images[0].image.url
            print headline
            album_images.append(headline)
    return render(request, 'imageviewer/index.html', {'last_albums': last_albums, 'album_images': album_images})

def album_old(request, album_id):
    try:
        album_images = Image_Store.objects.filter(album_id__exact=album_id)
        #album_images = Image_Store.objects.filter(pk=album_id)
    except Image_Store.DoesNotExist:
        raise Http404
    template = loader.get_template('imageviewer/album.html')
    context = RequestContext(request, {
        'album_images': album_images,
    })
    return HttpResponse(template.render(context))

def image(request, image_id):
    return HttpResponse("Display image: %s" % image_id)

def album(request, album_id):
    album = get_object_or_404(Album_Store, pk=album_id)
    album_images = get_list_or_404(Image_Store,  album=album_id)
    return render(request, 'imageviewer/album.html', {'album': album, 'album_images': album_images})

