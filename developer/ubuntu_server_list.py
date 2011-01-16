#!/usr/bin/env python
#
# Copyright 2010 Homer Xing <homer.xing@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import os, sys, urllib2
output_path = os.path.dirname(os.path.abspath(__file__))+'/../ailurus/support/ubuntu_server_list'
output_file = open(output_path, 'w')

class Analysis:
    def __init__(self):
        self.name = None
        self.location = None
        self.httpurl = None
        self.ftpurl = None
        self.rsyncurl = None
        self.server = None
    def set_location(self, location):
        changes = {'Korea, Republic of':'Republic of Korea',
                   'Moldova, Republic of':'Republic of Moldova'}
        if location in changes: location = changes[location]
        self.location = location

    def set_name(self, name):
        self.name = name.replace('\'', r'\'')
        
    def set_url(self, protocol, url):
        # set URL
        if protocol == 'http':
            assert url.startswith('http')
            self.httpurl = url
        elif protocol == 'ftp':
            assert url.startswith('ftp')
            self.ftpurl = url
        elif protocol == 'rsync':
            assert url.startswith('rsync')
            self.rsyncurl = url
        else:
            return
        
        # set server
        if self.server == None:
            import re
            match = re.match(r'^[a-z]+://([^/]+)/.*$', url)
            assert match, url
            self.server = match.group(1)
    
    def end_one_mirror(self):
        url = self.httpurl or self.ftpurl or self.rsyncurl

        assert self.name
        assert self.location
        assert url
        assert self.server
        
        print >>output_file, self.name
        print >>output_file, self.location
        print >>output_file, url
        print >>output_file, self.server

        self.name = self.httpurl = self.ftpurl = self.rsyncurl = self.server = None
    
    def analysis(self, line):
        import re
        match = re.search(r'<th colspan="2" style="text-align: left">([^<]+)</th>', line)
        if match:
            self.set_location(match.group(1))
            return
        
        match = re.search(r'<a href="/ubuntu/\+mirror/[^"]+">([^<]+)</a>', line)
        if match:
            self.set_name(match.group(1))
            return 

        match = re.search(r'<a href="([^"]+)">([^<]+)</a>', line)
        if match:
            protocol = match.group(2)
            url = match.group(1)
            self.set_url(protocol, url)
            return
    
        match = re.search('<span class="[^"]+">[^<]+</span>', line)
        if match:
            self.end_one_mirror()
            return

if __name__ == '__main__':
    obj = Analysis()
    f = urllib2.urlopen('https://launchpad.net/ubuntu/+archivemirrors')
    for line in f:
        obj.analysis(line)
