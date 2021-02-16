
import os
import sys

orig_dir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.join(orig_dir, '../../')))

import pogmake


def test_pogfile_simple():
