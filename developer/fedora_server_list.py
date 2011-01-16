#!/usr/bin/env python
#
# Copyright 2010 Homer Xing <homer.xing@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import os, sys, re, urllib2

output_path = os.path.dirname(os.path.abspath(__file__))+'/../ailurus/support/fedora_server_list'
output_file = open(output_path, 'w')

class Parser:
    def __init__(self):
        self.country = None
        self.org = None
        self.url = None
        self.begin_fedora_linux = False
    
    def reset(self):
        self.country = self.org = self.url = None
        self.begin_fedora_linux = False
    
    def begin_new_repos(self):
        if self.country and self.org and self.url:
            print >>output_file, self.country
            print >>output_file, self.org
            print >>output_file, self.url
        self.reset()
    
    def begin_country(self, line):
        assert self.country == None
        match = re.match(r'<td>([A-Z][A-Z])</td>', line)
        self.country = match.group(1)
    
    def start_fedora_linux(self):
        assert self.begin_fedora_linux == False
        self.begin_fedora_linux = True
    
    def begin_url(self, line):
        if self.begin_fedora_linux == False: return
        if self.url: return
        match = re.match(r'<td><span><a href="([^"]+)">([^<]+)</a></span></td>', line)
        self.url = match.group(1)
    
    def begin_org(self, line):
        if self.org: return
        match = re.match(r'<td><a href="[^"]+">([^<]+)</a></td>', line)
        self.org = match.group(1)
    
    def cope(self, line):
        if '</tr><tr class="odd">' == line or '</tr><tr class="even">' == line:
            self.begin_new_repos()
        if re.match(r'<td>[A-Z][A-Z]</td>', line):
            self.begin_country(line)
        if '<td>Fedora Linux</td>' in line:
            self.start_fedora_linux()
        if re.match(r'<td><span><a href="[^"]+">[^<]+</a></span></td>', line):
            self.begin_url(line)
        if re.match(r'<td><a href="[^"]+">[^<]+</a></td>', line):
            self.begin_org(line)

parser = Parser()
f = urllib2.urlopen('http://mirrors.fedoraproject.org/publiclist/Fedora/')
for line in f:
    parser.cope(line.strip())
f.close()
