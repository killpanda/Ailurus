#!/usr/bin/env python
#append names of files in "unfree/" to po/POTFILES.in
import os, sys, glob

paths = glob.glob('unfree/*.py')
assert paths
paths = [line+'\n' for line in paths]

with open('po/POTFILES.in') as f:
    lines = f.readlines()

for path in paths:
    if not path in lines:
        lines.append(path)

with open('po/POTFILES.in', 'w') as f:
    f.writelines(lines)
