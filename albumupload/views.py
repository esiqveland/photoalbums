from StringIO import StringIO
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from imageviewer.models import Image_Store, Album_Store, Image_Tags
from forms import UploadFileForm
from django import forms
from photostore.settings import MEDIA_ROOT
from albumupload.photohasher import hash_photo
from django.template import RequestContext
from PIL import Image

def index(request):
    return render(request, 'albumupload/index.html')


def handle_uploaded_file(postdata, file_uploaded):
    print file_uploaded
    hash, image = hash_photo(file_uploaded)
    path = MEDIA_ROOT + "photos/" + hash + "." + image.format.lower()
    filename = hash+"."+image.format.lower()
    print path
    album, album_was_created = Album_Store.objects.get_or_create(name=postdata['album_name'])
    imagemodel, image_was_created = Image_Store.objects.get_or_create(digest=hash, album=album)
    if image_was_created:
        imagemodel.image.save(filename, file_uploaded)
    imagemodel.save()


def upload(request):
    if request.method == 'POST':
        print "POST"
        for myfile in request.FILES.getlist('myfiles'):
            form = UploadFileForm(request.POST, request.FILES)
            print request.FILES['myfiles']
            print "form?"
            print myfile.content_type
            if form.is_valid():
                print "Form is valid!"
                handle_uploaded_file(request.POST, myfile)
        return render_to_response('imageviewer/album.html', context_instance=RequestContext(request))
    else:
        form = UploadFileForm()
    return render_to_response('albumupload/upload.html', {'form': form}, context_instance=RequestContext(request))

