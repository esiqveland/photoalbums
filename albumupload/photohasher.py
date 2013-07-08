import hashlib
from PIL import Image
from photostore.settings import MEDIA_ROOT
from cStringIO import StringIO

def hash_photo(photo):
    image = Image.open(photo)
    hash = hashlib.sha512(image.tostring()).hexdigest()
    print hash, image.format
    return hash, image

