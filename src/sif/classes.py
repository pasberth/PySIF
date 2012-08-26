import os
import yaml
from PIL import Image
from sif.helpers.path import (
    cfgpath,
    issif,
    issif_not_image,
    issif_as_image, )

class SpriteImageFormat(object):
    
    HAS_CONFIG_PARAMS = (
        "outfile",
        "outformat",
        "width",
        "height",
        "layers",
        )

    def __init__(self, config=None):
        self.config = self.verify_config(config)
        self._is_loaded = False
        self.build()
        #super(SpriteImageFormat, self).__init__(*args, **kwargs)

    def _default_outfile(self):
        return "%s.%s" % (os.path.splitext(self.name)[1], self.outformat.lower())
    
    def _default_outformat(self):
        fmt = self._get_image().format
        return fmt.lower() if fmt else "png"

    @property
    def outfile(self):
        if not self.config.has_key("outfile"):
            return self._default_outfile()
        else:
            return self.config["outfile"]

    @property
    def outformat(self):
        if not self.config.has_key("format"):
            return self._default_outformat()
        else:
            return self.config["format"].lower()

    @property
    def name(self):
        if not self.config.has_key("name"):
            raise TypeError, "config should has 'name' property."
        else:
            return self.config["name"]

    @property
    def x(self):
        if not self.config.has_key("x"):
            return 0
        else:
            return int(self.config["x"])

    @property
    def y(self):
        if not self.config.has_key("y"):
            return 0
        else:
            return int(self.config["y"])

    @property
    def width(self):
        if not self.config.has_key("width"):
            raise TypeError, "config should has 'width' property"
        else:
            return int(self.config["width"])

    @property
    def height(self):
        if not self.config.has_key("height"):
            raise TypeError, "config should has 'height' property"
        else:
            return int(self.config["height"])

    @property
    def layers(self):
        if not self.config.has_key("layers"):
            return []
        return [self.open_layer(layer) for layer in self.config["layers"]]

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
        layers = self.layers
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
        for over_image in layer.build(always_list=True):
            _base = base.copy()
            over_image_width, over_image_height = over_image.size
            over_image = over_image.resize( (layer.width or over_image_width, layer.height or over_image_height) )
            #over_image = over_image.crop( (0, 0, layer.width or over_image_width, layer.height or over_image_height) )
            bands = over_image.split()
            if len(bands) == 4:
                alpha = bands[3]
                _base.paste(over_image, (layer.x, layer.y), mask=alpha)
            else:
                _base.paste(over_image, (layer.x, layer.y))
            result += self._build_with(_base, layers[0:-1])
        return result

    def _create_canvas(self):
        return Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))

    def _get_image(self):
        return self._create_canvas()        

    def has_config_param(self, param_key):
        return param_key in self.HAS_CONFIG_PARAMS

    def open_layer(self, config):
        config = self.verify_layer_config(config)
        if config["type"] == "sif":
            return OpenSpriteImageFormat(config=config)
        elif config["type"] == "diff":
            return DiffSpriteImageFormat(config=config)
        else:
            raise TypeError, "unknown type: %s" %s (config["type"],)

    def verify_config(self, config):
        config = self.verify_config1(config)
        if not config.has_key("type"):
            config["type"] = "sif"
        return config

    def verify_config1(self, config):
        if isinstance(config, dict):
            return config.copy()
        elif isinstance(config, str):
            return { "name": config }
        else:
            raise TypeError, "config must be a dict"

    def verify_layer_config(self, config):
        config = self.verify_layer_config1(config)
        if not config.has_key("type"):
            config["type"] = "sif"
        return config

    def verify_layer_config1(self, config):
        if isinstance(config, dict):
            config = config.copy()
        elif isinstance(config, str):
            config = { "name": config }
        else:
            raise TypeError, "config must be a dict"
        if config.has_key("name") and config["name"]:
            config["name"] = os.path.join(self.name, config["name"])
        else:
            config["name"] = self.name
        return config
        

    def save(self, name=None, format=None):
        
        name = name or self.outfile
        format = format or self.outformat
        imgs = self.build(always_list=True)
        for img in imgs:
            img.show()
        img.save(name, format)
        return True

class NewFile(object):
    
    def __init__(self, **kwargs):
        super(NewFile, self).__init__(config=kwargs)

    def _get_image(self):
        return self._create_canvas()
    
    def _load(self):
        return True

class OpenFile(object):

    def __init__(self, name=None, config=None):
        config = config or {}
        config = config.copy()
        if not name and not config or config and not config.has_key("name"):
            raise TypeError, "Required argument 'name' (pos 1) not found"
        name = name or config["name"]
        if not os.path.exists(name):
            raise IOError, "No such file or directory: '%s'" % (name,)
        if not issif(name):
            raise IOError, "Not a SIF file: '%s'" % (name,)
        self.name = name
        config["name"] = name
        super(OpenFile, self).__init__(config=config)

    # Reset @property
    name = None

    @property
    def width(self):
        if not self.config.has_key("width"):
            return self._get_image().size[0]
        else:
            return int(self.config["width"])

    @property
    def height(self):
        if not self.config.has_key("height"):
            return self._get_image().size[1]
        else:
            return int(self.config["height"])

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
        #width, height = self.image.size
        self.config = {
            "name": self.name,
            "outfile": self.outfile,
            "outformat": self.image.format,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }

    def _load_not_image(self):
        with open(cfgpath(self.name)) as f:
            self.config = yaml.load(f.read())
            if not self.config.has_key("name"):
                self.config["name"] = self.name

class DiffFile(object):
    
    def __init__(self, config):
        super(DiffFile, self).__init__(config=config)

    def _get_image(self):
        return self._create_canvas()
    
    def _load(self):
        return True

    def _build(self):
        # todo: nested diff
        return [layer.build() for layer in self.layers]

class NewSpriteImageFormat(NewFile, SpriteImageFormat):
    pass

class OpenSpriteImageFormat(OpenFile, SpriteImageFormat):
    pass

class DiffSpriteImageFormat(DiffFile, SpriteImageFormat):
    pass
