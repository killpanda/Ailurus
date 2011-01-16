#!/usr/bin/env python
#
# Copyright 2010 Homer Xing <homer.xing@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import sys, os
code_path = os.path.dirname(os.path.abspath(__file__))+'/../ailurus/'
sys.path.insert(0, code_path)
from download_icons import icons_pack_version as VERSION
icons_path = os.path.dirname(os.path.abspath(__file__))+'/../ailurus/icons/appicons/'
pack_path = '/tmp/appicons_v%s.tar.gz' % VERSION
assert os.path.exists(icons_path), icons_path
os.chdir(icons_path)
assert os.system('tar czf ' + pack_path + ' *') == 0
print pack_path