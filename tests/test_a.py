import sif
from PIL import Image
from utils import assertRoughlyEqual
from utils import expand_path_fixture
from nose.tools import eq_

def build_pasberth_rb_icon():
    pri = sif.open(expand_path_fixture("pasberth_rb_icon/pri.sif"))
    return pri.build()

def test_is_pasberth_rb_icon_01():
    imgs = build_pasberth_rb_icon()
    icon01 = Image.open(expand_path_fixture("pasberth_rb_icon/img/01.png"))
    assertRoughlyEqual(imgs[0].image, icon01)

def test_pasberth_rb_icon_01_size():
    imgs = build_pasberth_rb_icon()
    icon01 = Image.open(expand_path_fixture("pasberth_rb_icon/img/01.png"))
    eq_(imgs[0].image.size, icon01.size)

def test_is_pasberth_rb_icon_02():
    imgs = build_pasberth_rb_icon()
    icon02 = Image.open(expand_path_fixture("pasberth_rb_icon/img/02.png"))
    assertRoughlyEqual(imgs[1].image, icon02)

def test_is_pasberth_rb_icon_03():
    imgs = build_pasberth_rb_icon()
    icon03 = Image.open(expand_path_fixture("pasberth_rb_icon/img/03.png"))
    assertRoughlyEqual(imgs[2].image, icon03)
