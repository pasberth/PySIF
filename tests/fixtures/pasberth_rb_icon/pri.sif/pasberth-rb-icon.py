import os
import sys

SRC_ROOT = os.path.join(os.path.dirname(__file__), './src')
sys.path[0:0] = [SRC_ROOT]

import sif

a = sif.open('pasberth-rb-icon.sif')
a.save()
