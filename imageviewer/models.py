from django.db import models
from photostore.settings import MEDIA_ROOT
import os
import datetime

class Album_Store(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    digest = models.CharField(max_length=100)
    def __unicode__(self):
        return self.digest + ': ' + self.name

max_size = (370, 278)

class Image_Store(models.Model):
    digest = models.CharField(max_length=100)
    upload_date = models.DateTimeField('Date uploaded', default=datetime.datetime.today())
    taken_date = models.DateTimeField('Date taken', default=datetime.datetime.today())
    album = models.ForeignKey(Album_Store)
    tags = models.CharField('image_tags', max_length=140)
    def generate_filename(self, filename):
        #return os.path.join('photos', instance.digest+filename)
        return os.path.join('photos', self.digest)

    def generate_filename_thumb(self, filename):
        #return os.path.join('photos', instance.digest+filename)
        return os.path.join('photos', self.digest)

    image = models.ImageField(upload_to='photos/')
    thumbnail = models.ImageField(upload_to='photos',max_length=500,blank=True,null=True)
    def __unicode__(self):
        return self.digest + ': ' + self.image.url


    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return

        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = max_size

        # Open original photo which we want to thumbnail using PIL's Image
        self.image.seek(0)
        image = Image.open(StringIO(self.image.read()))

        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        #
        # I commented this part since it messes up my png files
        #
        #if image.mode not in ('L', 'RGB'):
        #    image = image.convert('RGB')

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # image type...
        FILE_TYPE = image.format.lower()
        if FILE_TYPE == 'jpeg':
            PIL_TYPE = 'jpeg'
            DJANGO_TYPE = 'image/jpeg'
            FILE_EXTENSION = 'jpeg'
        elif FILE_TYPE == 'png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
            DJANGO_TYPE = 'image/png'

        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                 temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save('%s_thumb.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            self.create_thumbnail()

        super(Image_Store, self).save(*args, **kwargs)


class Image_Tags(models.Model):
    name = models.CharField(max_length=100)
    images = models.ForeignKey(Image_Store)
