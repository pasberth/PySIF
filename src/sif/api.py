from sif.classes import (
    OpenSpriteImageFormat,
    NewSpriteImageFormat, )

def open(name):
    return OpenSpriteImageFormat(name)

def new(*args, **kwargs):
    return NewSpriteImageFormat(*args, **kwargs)
