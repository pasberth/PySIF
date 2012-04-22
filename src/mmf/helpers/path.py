import os

MMF_AS_IMAGE_EXTS = ('.jpg', '.gif', '.png',)

def cfgpath(mmf_path):
    return os.path.join(mmf_path, 'config.yml')

def ismmf(mmf_path):
    return ismmf_not_image(mmf_path) or ismmf_as_image(mmf_path)

def ismmf_not_image(mmf_path):
    return os.path.isdir(mmf_path) and os.path.exists(cfgpath(mmf_path))

def ismmf_as_image(mmf_path):
    return os.path.splitext(mmf_path)[1].lower() in MMF_AS_IMAGE_EXTS