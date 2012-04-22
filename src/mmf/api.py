from mmf.classes import (
    OpenMergeableMangaFormat, 
    NewMergeableMangaFormat, )

def open(name):
    return OpenMergeableMangaFormat(name)

def new(*args, **kwargs):
    return NewMergeableMangaFormat(*args, **kwargs)