#!/usr/bin/env python

import os, sys, glob
ailurus_path = os.path.dirname(os.path.abspath(__file__)) + '/../ailurus'
sys.path.insert(0, ailurus_path)
appicon_path = ailurus_path + '/icons/appicons/'
from loader import AppObjs
import common.apps
import fedora.apps
import gnome.apps
import ubuntu.apps

names = []
for module in [common.apps, fedora.apps, gnome.apps, ubuntu.apps]:
    names += AppObjs.all_installer_names_in_module(module)
names += AppObjs.all_installer_names_in_text_file()
names = list(set(names))

print "The following software item needs icon!"
for name in names:
    path, use_default_icon = AppObjs.get_icon_path(name)
    if use_default_icon:
        print name
print

print 'The following icon is excessive!'
for path in glob.glob(appicon_path + '/*.png'):
    filename = os.path.basename(path)
    if filename in ['python.png', 'gtk.png']: continue
    basename = os.path.splitext(filename)[0]
    if not basename in names:
        print filename