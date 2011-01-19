#coding: utf-8
#
# Ailurus - a simple application installer and GNOME tweaker
#
# Copyright (C) 2009-2010, Ailurus developers and Ailurus contributors
# Copyright (C) 2007-2010, Trusted Digital Technology Laboratory, Shanghai Jiao Tong University, China.
#
# Ailurus is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ailurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ailurus; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

from __future__ import with_statement
import sys, os
from lib import *
from libapp import *
from apps_eclipse import *
#from app_tasksel import * # Shall we provide tasksel GUI? Its loading time is almost the same as dump_deb
from app_from_external_repos import *
from third_party_repos import *

class WorldofPadman_Ubuntu(I):
    __doc__ = _('World of Padman: Funny shooter game')
    detail = _('Ailurus will install the game, and apply the latest patch.')
    download_url = 'ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/'
    license = GPL + ' http://sourceforge.net/projects/wop-engine/'
    category = 'game'
    def install(self):
        file1 = R(urls.worldofpadman).download()
        run_as_root('bash ' + file1)
        file2 = R(urls.worldofpadman_patch).download()
        run_as_root('bash ' + file2)
    def installed(self):
        import os
        return os.path.exists('/usr/local/games/WoP')
    def remove(self):
        run_as_root('rm /usr/local/games/WoP -rf')
        run_as_root('rm /usr/local/bin/wop')

class PBC(I): # support x86_64 only.
    __doc__ = _('PBC (Pairing-Based Cryptography) library')
    detail = _('Install Pairing-Based Cryptography library, powered by Stanford University.')
    download_url = 'http://crypto.stanford.edu/pbc/'
    category = 'library'
    license = GPL
    def install(self):
        fdev = R(urls.pbcdev64).download()
        f = R(urls.pbc64).download()
        APT.install_local(f, fdev)
    def installed(self):
        return APT.installed('libpbc0') and APT.installed('libpbc-dev')
    def remove(self):
        APT.remove('libpbc0', 'libpbc-dev')
    def visible(self):
        return not is32()
    
class GNOMEArtNextGen(I):
    __doc__ = _('GNOMEArtNG: Choose 100+ GNOME themes')
    detail = _('It is able to customize the backgrounds, application look, window borders, icons, GNOME splash and GDM window. '
       'More than 100 themes can be installed, which are downloaded from http://art.gnome.org . '
       'The official site of GNOMEArtNG is http://developer.berlios.de/projects/gnomeartng/')
    category = 'theme'
    license = GPL
    DE = 'gnome'
    def install(self):
        if VERSION == 'hardy':
            file = R(urls.gnomeartng_hardy).download()
        elif VERSION == 'intrepid':
            file = R(urls.gnomeartng_intrepid).download()
        elif VERSION == 'jaunty':
            file = R(urls.gnomeartng_jaunty).download()
        elif VERSION == 'karmic':
            file = R('http://ailurus.googlecode.com/files/gnomeartng-0.7.0-karmic.deb').download()
        else:
            raise Exception('GNOMEArtNextGen', VERSION)
        APT.install_local(file)
        try: # Do not raise error, when this file cannot be downloaded.
            thumb = R('http://download.berlios.de/gnomeartng/thumbs.tar.gz').download()
        except:
            return
        import os
        path = os.path.expanduser('~/.gnome2/gnome-art-ng/')
        if not os.path.exists(path): run('mkdir '+path)
        with Chdir(path):
            run('tar xf '+thumb)
    def installed(self):
        return APT.installed('gnomeartng')
    def remove(self):
        APT.remove('gnomeartng')
        run('rm -rf $HOME/.gnome2/gnome-art-ng/')
    def visible(self):
        return VERSION in ['hardy', 'intrepid', 'jaunty', 'karmic']

class DisableGetty(I):
    __doc__ = _('Deactivate Getty ( Ctrl+Alt+F2 ... F6 ), Ctrl+Alt+F1 is still activated')
    detail = _('Speed up Linux start up process. Free 2.5 MBytes memory. ')
    def visible(self):
        return os.path.exists('/etc/event.d/tty1')
    def installed(self):
        with Chdir('/etc/event.d/'):
            for i in range(2,7):
                file_name = 'tty%s' % i
                if os.path.exists(file_name):
                    with open(file_name) as f:
                        for line in f:
                            if line.startswith('exec'): return False
        return True
    def install(self):
        with Chdir('/etc/event.d/'):
            for i in range(2,7):
                file_name = 'tty%s'%i
                if os.path.exists(file_name):
                    with TempOwn(file_name):
                        with open(file_name) as f:
                            contents = f.readlines()
                        for j, line in enumerate(contents):
                            if line.startswith('exec'):
                                contents[j]='#' + line
                        with open(file_name, 'w') as f:
                            f.writelines(contents)
    def remove(self):
        with Chdir('/etc/event.d/'):
            for i in range(2,7):
                file_name = 'tty%s'%i
                if os.path.exists(file_name):
                    with TempOwn(file_name):
                        with open(file_name) as f:
                            contents = f.readlines()
                        for j, line in enumerate(contents):
                            if line.startswith('#exec'):
                                contents[j]='exec /sbin/getty 38400 tty%s\n' % i
                        with open(file_name, 'w') as f:
                            f.writelines(contents)

class DisableGettyKarmic(I):
    __doc__ = _('Deactivate Getty ( Ctrl+Alt+F2 ... F6 ), Ctrl+Alt+F1 is still activated')
    detail = _('Speed up Linux start up process. Free 2.5 MBytes memory. ')
    def visible(self):
        return os.path.exists('/etc/init/tty1.conf')
    def installed(self):
        with Chdir('/etc/init/'):
            for i in range(2,7):
                file_name = 'tty%s.conf' % i
                if os.path.exists(file_name):
                    with open(file_name) as f:
                        for line in f:
                            if line.startswith('exec'): return False
        return True
    def install(self):
        with Chdir('/etc/init/'):
            for i in range(2,7):
                filename = 'tty%s.conf'%i
                with TempOwn(filename):
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line.startswith('exec'):
                            contents[j]='#' + line
                    with open(filename, 'w') as f:
                        f.writelines(contents)
    def remove(self):
        with Chdir('/etc/init/'):
            for i in range(2,7):
                filename = 'tty%s.conf'%i
                with TempOwn(filename):
                    with open(filename) as f:
                        contents = f.readlines()
                    for j, line in enumerate(contents):
                        if line.startswith('#exec'):
                            contents[j]='exec /sbin/getty -8 38400 tty%s\n'%i
                    with open(filename, 'w') as f:
                        f.writelines(contents)

class OpenJUMP(_apt_install): # OpenJUMP is not in Fedora :(
    __doc__ = _('OpenJUMP: A geographic information system')
    license = GPL
    category = 'geography'
    pkgs = 'openjump'

class Remastersys(_apt_install):
    __doc__ = _('Remastersys: Backup your system to a live CD')
    download_url = 'http://sourceforge.net/projects/remastersys/'
    category = 'others'
    pkgs = 'remastersys'
    def visible(self):
        return VERSION >= 'karmic'
    def install(self):
        f = R(urls.remastersys).download()
        APT.install_local(f)

class Radioget(I):
    __doc__ = _('SHA-DA network radio: Listen to and watch radio and TV programs in China')
    dowload_url = 'http://radioget.googlecode.com/'
    category = 'internet'
    license = GPL
    Chinese = True
    def visible(self):
        return is32()
    def install(self):
        f = R('http://radioget.googlecode.com/files/radioget-0.2.4-i386.deb').download()
        APT.install_local(f)
    def installed(self):
        return APT.installed('radioget')
    def remove(self):
        APT.remove('radioget')  
    