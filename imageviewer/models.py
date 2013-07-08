from django.db import models
import os
import datetime

class Album_Store(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    digest = models.CharField(max_length=100)
    def __unicode__(self):
        return self.digest + ': ' + self.name

class Image_Store(models.Model):
    digest = models.CharField(max_length=100)
    upload_date = models.DateTimeField('Date uploaded', default=datetime.datetime.today())
    taken_date = models.DateTimeField('Date taken', default=datetime.datetime.today())
    album = models.ForeignKey(Album_Store)
    tags = models.CharField('image_tags', max_length=140)
    def generate_filename(self, filename):
        #return os.path.join('photos', instance.digest+filename)
        return os.path.join('photos', self.digest)

    image = models.ImageField(upload_to=generate_filename)
    def __unicode__(self):
        return self.digest + ': ' + self.image.url

class Image_Tags(models.Model):
    name = models.CharField(max_length=100)
    images = models.ForeignKey(Image_Store)
