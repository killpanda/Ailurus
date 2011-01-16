#!/usr/bin/env python
#remove names of files in "unfree/" from po/POTFILES.in
import os, sys, glob

paths = glob.glob('unfree/*.py')
assert paths
paths = [line+'\n' for line in paths]

with open('po/POTFILES.in') as f:
    lines = f.readlines()

for path in paths:
    if path in lines:
        lines.remove(path)
        assert path not in lines

with open('po/POTFILES.in', 'w') as f:
    f.writelines(lines)
