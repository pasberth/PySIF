import os
from nose.tools import eq_
from PIL import Image
from itertools import islice

def expand_path_fixture(fixture_name):
    return os.path.join(os.path.dirname(__file__), "fixtures", fixture_name)

def assertRoughlyEqual(artualImage, expectingImage):
    X, Y = artualImage.size

    for x in islice(range(0, X), 0, (X/50)):
        for y in islice(range(0, Y), 0, (Y/50)):
            apx = artualImage.getpixel((x, y))
            epx = expectingImage.getpixel((x, y))
            eq_(apx, epx)
