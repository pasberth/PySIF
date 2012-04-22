import os

SIF_AS_IMAGE_EXTS = ('.jpg', '.gif', '.png',)

def cfgpath(path):
    return os.path.join(path, 'config.yml')

def issif(path):
    return issif_not_image(path) or issif_as_image(path)

def issif_not_image(path):
    return os.path.isdir(path) and os.path.exists(cfgpath(path))

def issif_as_image(path):
    return os.path.splitext(path)[1].lower() in SIF_AS_IMAGE_EXTS
