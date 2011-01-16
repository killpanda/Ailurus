#!/usr/bin/env python
#
# Copyright 2010 Homer Xing <homer.xing@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import os, sys, re
pattern1 = re.compile(r'em:name="(.+)"')
pattern2 = re.compile(r'<em:name>(.+)</em:name>')
def get_name(string):
    match = pattern1.search(string)
    if match:
        return match.group(1)
    match = pattern2.search(string)
    if match:
        return match.group(1)
    raise Exception
ailurus_path = os.path.dirname(os.path.abspath(__file__))+'/../ailurus/'
sys.path.insert(0, ailurus_path)
from lib import *
from libapp import *
from loader import *
app_objs = load_app_objs()
objs = [obj for obj in app_objs if isinstance(obj, _ff_extension)]
objs = [obj for obj in objs if obj.__class__.__name__ in ('FFFirefoxSync', 'FFFlashgot')]
for obj in objs:
    try:
        assert isinstance(obj, _ff_extension)
        f = obj.R.download()
        run('rm /tmp/T -rf')
        run('mkdir /tmp/T')
        with Chdir('/tmp/T'):
            run('unzip -qo '+f)
            rdf = open('install.rdf')
            content = rdf.read()
            name = get_name(content)
            assert name == obj.name, name
    except:
        print obj
        print_traceback()
