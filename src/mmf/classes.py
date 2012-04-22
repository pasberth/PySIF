import os
import yaml
from PIL import Image
import sif

from mmf.helpers.path import (
    cfgpath,
    ismmf,
    ismmf_as_image, )

class MergeableMangaFormat(sif.SpriteImageFormat):
    
    
    HAS_CONFIG_PARAMS = sif.SpriteImageFormat.HAS_CONFIG_PARAMS + ("blocks",)

    def _default_blocks(self):
        return []
    
    def _build(self):
        return self._build_with_blocks(super(MergeableMangaFormat, self)._build(), self._build_blocks())

    def _build_with_blocks(self, base, blocks, top=0, left=0):
        if not blocks:
            return [base]
        block = blocks[0]
        result = []
        for over_image in block.image.build(always_list=True):
            over_image.load()
            over_image_width, over_image_height = over_image.size
            if top + over_image_height > self.height():
                top, left = 0, 0
                result.append(base)
                _base = super(MergeableMangaFormat, self)._build()
            else:
                _base = base.copy()
            bands = over_image.split()
            if len(bands) == 4:
                alpha = bands[3]
                _base.paste(over_image, (left, top), mask=alpha)
            else:
                _base.paste(over_image, (lef, top))
            result += self._build_with_blocks(_base, blocks[1:], top = top + over_image_height, left = left)
        return result

    def _build_blocks(self):
        if not self.config.has_key("blocks"):
            return self._default_blocks()

        blocks = []
        for block in self.config["blocks"]:
            if isinstance(block, str):
                blocks.append(self.Block(name=os.path.join(self.name, block)))
            elif isinstance(block, dict):
                if block.has_key("name") and block["name"]:
                   block["name"] = os.path.join(self.name, block["name"])
                blocks.append(self.Block(**block))
            else:
                raise TypeError, "block must be a dict"
        return blocks
    
    def page_name(self, format_string, page_number, **kwargs):
        format_string = format_string.replace('$N', str(page_number))
        return format_string

    def save(self, name=None):
        pages = self.build()
        for i, page in enumerate(pages):
            pname = self.page_name(name or self.outfile(), i)
            page.save(pname)

    class Block(object):
        def __init__(self, name, width=None, height=None):
            self.image = OpenMergeableMangaFormat(name)
            self.name = name
            self.width = width
            self.height = height

class NewMergeableMangaFormat(sif.NewFile, MergeableMangaFormat):
    pass

class OpenMergeableMangaFormat(sif.OpenFile, MergeableMangaFormat):
    pass