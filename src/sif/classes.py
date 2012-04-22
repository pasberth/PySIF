import os
import yaml
from PIL import Image
from sif.helpers.path import (
    cfgpath,
    issif,
    issif_not_image,
    issif_as_image, )

class SpriteImageFormat(object):
    
    HAS_CONFIG_PARAMS = ("outfile", "outformat", "width", "height", "layers")

    def __init__(self):
        self.config = {}
        self._is_loaded = False
        #super(SpriteImageFormat, self).__init__(*args, **kwargs)

    def load(self):
        if self._is_loaded:
            return False
        self._is_loaded = True
        self._load()
        return True
    
    def build(self, always_list=False):
        ret = self._build()
        if always_list and not isinstance(ret, list):
            ret = [ret]
        if not ret:
            raise TypeError, "_build() should return [image] over than 1 elements"
        return ret

    def _build(self):
        self.load()
        
        base   = self._get_image()
        layers = self._build_layers()
        ret = self._build_with(base, layers)
        if isinstance(ret, list) and len(ret) == 1:
            return ret[0]
        else:
            return ret

    def _build_with(self, base, layers):
        if not layers:
            return [base]
        layer = layers[-1]
        result = []
        for over_image in layer.image.build(always_list=True):
            _base = base.copy()
            over_image_width, over_image_height = over_image.size
            over_image = over_image.crop( (0, 0, layer.width or over_image_width, layer.height or over_image_height) )
            bands = over_image.split()
            if len(bands) == 4:
                alpha = bands[3]
                _base.paste(over_image, (layer.x, layer.y), mask=alpha)
            else:
                _base.paste(over_image, (layer.x, layer.y))
            result += self._build_with(_base, layers[0:-1])
        return result

    def _create_canvas(self):
        return Image.new('RGBA', (self.width(), self.height()), (0, 0, 0, 0))

    def _get_image(self):
        return self._create_canvas()

    def outfile(self):
        return self._build_outfile()

    def outformat(self):
        return self._build_outformat()

    def width(self):
        return self._build_width()

    def height(self):
        return self._build_height()
        
    def _default_outfile(self):
        return "%s.%s" % (os.path.splitext(self.name)[1], self.outformat().lower())

    def _build_outfile(self):
        if not self.config.has_key("outfile"):
            return self._default_outfile()
        else:
            return os.path.join(os.path.dirname(self.name), self.config["outfile"])
    
    def _default_outformat(self):
        return self._get_image().format.lower()

    def _build_outformat(self):
        if not self.config.has_key("outformat"):
            return self._default_outformat()
        else:
            return self.config["outformat"].lower()

    def _default_width(self):
        raise TypeError, "config should has 'width' property"

    def _build_width(self):
        if not self.config.has_key("width"):
            return self._default_width()
        else:
            return int(self.config["width"])

    def _default_height(self):
        raise TypeError, "config should has 'width' property"

    def _build_height(self):
        if not self.config.has_key("height"):
            return self._default_height()
        else:
            return int(self.config["height"])

    def has_config_param(self, param_key):
        return param_key in self.HAS_CONFIG_PARAMS

    def _default_layers(self):
        return []

    def _build_layers(self):
        if not self.config.has_key("layers"):
            return self._default_layers()

        layers = []
        for layer in self.config["layers"]:
            if isinstance(layer, str):
                layers.append(self.Layer(name=os.path.join(self.name, layer)))
            elif isinstance(layer, dict):
                layer = layer.copy()
                if layer.has_key("name") and layer["name"]:
                    layer["name"] = os.path.join(self.name, layer["name"])
                layers.append(self.Layer(**layer))
            else:
                raise TypeError, "layer must be a dict"
        return layers

    def save(self, name=None, format=None):
        name = name or self.outfile()
        format = format or self.outformat()
        img = self.build()
        img.save(name, format)
        return True
    
    class Layer(object):
        def __init__(self, name, x=0, y=0, width=None, height=None):
            self.image = OpenSpriteImageFormat(name)
            self.name = name
            self.x = x
            self.y = y
            self.width = width
            self.height = height


class NewFile(object):
    
    def __init__(self, **kwargs):
        super(NewFile, self).__init__()
        for k, v in kwargs.items():
            if self.has_config_param(k):
                self.config[k] = v

    def _get_image(self):
        return self._create_canvas()
    
    def _load(self):
        return True

class OpenFile(object):

    def __init__(self, name):
        if not name:
            raise TypeError, "Required argument 'name' (pos 1) not found"
        if not os.path.exists(name):
            raise IOError, "No such file or directory: '%s'" % (name,)
        if not issif(name):
            raise IOError, "Not a MMF file: '%s'" % (name,)

        super(OpenFile, self).__init__()
        self.name = name
        self.load()

    def _get_image(self):
        if issif_as_image(self.name):
            return Image.open(self.name)
        else:
            return self._create_canvas()

    def _load(self):
        if issif_as_image(self.name):
            return self._load_as_image()
        else:
            return self._load_not_image()

    def _load_as_image(self):
        self.image = self._get_image()
        width, height = self.image.size
        self.config = {
            "outfile": self.name,
            "outformat": self.image.format,
            "width": width,
            "height": height
        }

    def _load_not_image(self):
        with open(cfgpath(self.name)) as f:
            self.config = yaml.load(f.read())

class NewSpriteImageFormat(NewFile, SpriteImageFormat):
    pass


class OpenSpriteImageFormat(OpenFile, SpriteImageFormat):
    pass
