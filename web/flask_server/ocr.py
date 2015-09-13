import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO


def process_image(url):
    image = _get_image(url)
    print image
    image.filter(ImageFilter.SHARPEN)
    print 'yay'
    return pytesseract.image_to_string(image)


def _get_image(url):
    return Image.open('test.jpg')