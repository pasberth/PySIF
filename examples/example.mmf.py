import os
import sys

SRC_ROOT = os.path.join(os.path.dirname(__file__), '../src')
sys.path[0:0] = [SRC_ROOT]

import mmf

a = mmf.open('examples/example.mmf')
a.save()
