#!/usr/bin/env python
#
# Copyright 2010 Homer Xing <homer.xing@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import sys, os, urllib2, re

latest_mtj_version = '1.0.1'

def version_string_to_tuple(string):
    return tuple(map(int, string.split('.')))

f = urllib2.urlopen('http://www.eclipse.org/dsdp/mtj/')
content = f.read()
f.close()

strings = re.findall('>MTJ [0-9.]+<', content)
for string in strings:
    version = re.match('>MTJ ([0-9.]+)<', string).group(1)
    if version_string_to_tuple(version)>version_string_to_tuple(latest_mtj_version):
        print 'Version %s is released!' % version
        print 'http://www.eclipse.org/dsdp/mtj/'
        sys.exit(1)

xml = 'http://www.eclipse.org/downloads/download.php?file=/dsdp/mtj/downloads/drops/R-1.0.1-200909181641/dsdp-mtj-SDK-1.0.1.zip&format=xml'
f = urllib2.urlopen(xml)
content = f.read()
f.close()

path = os.path.dirname(os.path.abspath(__file__))+'/../ailurus/support/MTJ_urls'
f = open(path, 'w')

url_list = re.findall(r'url="[^"]+"', content)
for string in url_list:
    match = re.match('url="([^"]+)"', string)
    url = match.group(1)
    print >>f, url

print 'Update', path