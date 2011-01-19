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

def get_non_launchpad_keyfile_path(class_name):
    return A + '/publickey/ubuntu_' + class_name

class _repo(I):
    this_is_a_repository = True
    category = 'repository'
    def __init__(self):
        assert isinstance(self.web_page, str)
        assert isinstance(self.apt_file, str)
        assert isinstance(self.apt_conf, list)
        for i,a in enumerate(self.apt_conf):
            is_string_not_empty(a)
            if a.endswith('\n'): raise ValueError(a)
        assert isinstance(self.apt_content, str)
        
        if hasattr(self, 'key_url'):
            assert isinstance(self.key_url, str)
            if self.key_url:
                assert ( self.key_url.startswith('ftp://') or
                         self.key_url.startswith('http://') or
                         self.key_url.startswith('https://') )
        
        assert isinstance(self.key_id, str)
        
        self.download_url = self.web_page
        self.how_to_install = '\n'.join(self.apt_conf)
    def installed(self):
        return APTSource2.all_lines_contain_all_of(self.apt_conf)
    def install(self):
        APTSource2.add_lines_to_file(self.apt_conf, self.apt_file)
        if hasattr(self, 'key_url') and self.key_url:
            path = get_non_launchpad_keyfile_path(self.__class__.__name__)
            run_as_root('apt-key add "%s"' % path)
    def remove(self):
        APTSource2.remove_snips_from_all_files(self.apt_conf)
        if self.key_id:
            run_as_root('apt-key del '+self.key_id, ignore_error=True)

def get_owner_and_name(ppa):
    assert not ppa.startswith("ppa:")
    ppa_owner = ppa.split("/")[0]
    try:
        ppa_name = ppa.split("/")[1]
    except IndexError, e:
        ppa_name = "ppa"
    return (ppa_owner, ppa_name)

def get_deb_line(ppa_owner, ppa_name, distro_codename):
    return "deb http://ppa.launchpad.net/%s/%s/ubuntu %s main" % (
        ppa_owner, ppa_name, distro_codename)

def get_repos_file_name(ppa_owner, ppa_name, distro_codename):
    return "%s-%s-%s.list" % (ppa_owner, ppa_name, distro_codename)

def get_signing_key(ppa_owner, ppa_name):
    import urllib2, re
    lp_url = ('https://launchpad.net/api/beta/~%s/+archive/%s' % (
        ppa_owner, ppa_name))
    try:
        req = urllib2.Request(lp_url)
        req.add_header("Accept","application/json")
        lp_page = urllib2.urlopen(req).read()
        signing_key_fingerprint = re.findall(
            '\"signing_key_fingerprint\": \"(\w*)\"', lp_page)[0]
        return signing_key_fingerprint
    except urllib2.URLError, e:
        print_traceback()
        return None

def add_signing_key(signing_key_fingerprint):
    path = get_signing_key_path(signing_key_fingerprint)
    run_as_root("apt-key add '%s'" % path)

def del_signing_key(signing_key_fingerprint):
    run_as_root("apt-key del " + signing_key_fingerprint)

def get_signing_key_path(signing_key_fingerprint):
    assert isinstance(signing_key_fingerprint, str) and signing_key_fingerprint
    return A + '/publickey/launchpad_' + signing_key_fingerprint

class _launchpad(I):
    this_is_a_repository = True
    category = 'repository'
    def __init__(self):
        assert isinstance(self.ppa, str)
        if hasattr(self, 'content'): assert isinstance(self.content, str)
        self.ppa_owner, self.ppa_name = get_owner_and_name(self.ppa)
        self.deb_config = get_deb_line(self.ppa_owner, self.ppa_name, VERSION)
        self.repos_file_name = '/etc/apt/sources.list.d/' + get_repos_file_name(self.ppa_owner, self.ppa_name, VERSION)
        self.download_url = 'http://launchpad.net/~%s/+archive/%s' % (self.ppa_owner, self.ppa_name)
        if VERSION <= 'jaunty':
            self.how_to_install = self.deb_config
        else: # >= 'karmic'
            self.how_to_install = 'add-apt-repository ppa:%s' % self.ppa
    def install(self):
        APTSource2.add_lines_to_file([self.deb_config], self.repos_file_name)
        signing_key = get_signing_key(self.ppa_owner, self.ppa_name)
        if signing_key: add_signing_key(signing_key)
    def installed(self):
        return APTSource2.all_lines_contain(self.deb_config)
    def remove(self):
        APTSource2.remove_snips_from_all_files([self.deb_config])
        signing_key = get_signing_key(self.ppa_owner, self.ppa_name)
        if signing_key: del_signing_key(signing_key)

# Hide it in Lucid. Since Firefox is 3.6.3 in Lucid.
class Repo_Firefox_3_6(_launchpad):
    __doc__ = _('Firefox 3.6 (stable)')
    license = TRI_LICENSE(MPL, GPL, LGPL)
    ppa = 'mozillateam/firefox-stable'
    content = 'firefox'
    def visible(self):
        return VERSION in ['hardy', 'intrepid', 'jaunty', 'karmic']

class Repo_PlayOnLinux(_repo):
    __doc__ = _('PlayOnLinux (stable)')
    license = LGPL
    def __init__(self):
        self.detail = _('PlayOnLinux is a front-end for wine. '
            'It helps to install Windows Games and softwares on Linux.')
        self.apt_content = 'playonlinux'
        self.web_page = 'http://www.playonlinux.com/en/download.html'
        self.apt_file = '/etc/apt/sources.list.d/playonlinux.list'
        self.apt_conf = [ 'deb http://deb.playonlinux.com/ '+VERSION+' main' ]
        self.key_url = '' #no key
        self.key_id = '' #no key
        _repo.__init__(self)

class Repo_WINE(_launchpad):
    __doc__ = _('WINE (beta version)')
    license = LGPL + ' http://wiki.winehq.org/Licensing'
    detail = _('This repository contains the latest version of Wine. '
            'Wine is for running Windows applications on Linux.')
    ppa = 'ubuntu-wine'
    content = ''

class Repo_Ailurus(_launchpad):
    __doc__ = _('Ailurus (stable)')
    license = GPL
    ppa = 'ailurus'
    content = 'ailurus'

class Repo_AWN_Development(_launchpad):
    __doc__ = _('AWN (beta version)')
    license = GPL
    detail = _('AWN is a MacOS X like panel for GNOME. '
            'This repository provides the latest version of AWN.')
    content = 'avant-window-navigator-trunk'
    ppa = 'awn-testing'

class Repo_Blueman(_launchpad):
    __doc__ = _('Blueman (stable)')
    license = GPL
    detail = _('Blueman is a graphical blue-tooth manager.')
    content = 'blueman'
    ppa = 'blueman'

class Repo_Christine(_launchpad):
    __doc__ = _('Christine (stable)')
    license = GPL
    detail = _('Christine is a small media player.')
    content = 'christine'
    ppa = 'markuz'

class Repo_Chromium_Daily(_launchpad):
    __doc__ = _('Chromium (beta version)')
    license = BSD
    detail = _('Chromium is the open source version of Google Chrome.')
    content = 'chromium-browser'
    ppa = 'chromium-daily'

class Repo_GTG(_launchpad):
    __doc__ = _('Getting things GNOME (stable)')
    license = GPL
    detail = _('"Getting things GNOME" is a simple, powerful and flexible organization tool.')
    content = 'gtg'
    ppa = 'gtg'

class Repo_GNOMEColors(_launchpad):
    __doc__ = _('GNOME colors (stable)')
    license = GPL
    detail = _('This repository contains some themes.')
    content = 'gnome-colors'
    DE = 'gnome'
    ppa = 'gnome-colors-packagers'

class Repo_GlobalMenu(_launchpad):
    __doc__ = _('GNOME Global Menu (stable)')
    license = GPL
    detail = _('GNOME Global Menu is the globally-shared menu bar of all applications.')
    content = 'gnome-globalmenu'
    DE = 'gnome'
    ppa = 'globalmenu-team'

class Repo_Medibuntu(_repo):
    __doc__ = _('Medibuntu (stable)')
    license = GPL
    detail = _('This is a repository providing packages which cannot be included into the Ubuntu distribution for legal reasons. '
            'There are many packages in this repository. The list of packages is in http://packages.medibuntu.org/')
    apt_content = ''
    web_page = 'http://packages.medibuntu.org/'
    apt_file = '/etc/apt/sources.list.d/medibuntu.list'
    apt_conf = [ 'deb http://packages.medibuntu.org/ '+VERSION+' free non-free' ]
    key_url = 'http://packages.medibuntu.org/medibuntu-key.gpg'
    key_id = '0C5A2783'

class Repo_Moovida(_launchpad):
    __doc__ = _('Moovida (stable)')
    license = GPL
    detail = _('Moovida is a cross platform media player.')
    content = 'moovida'
    ppa = 'moovida-packagers'
    
class Repo_X_Server_Updates(_launchpad):
    __doc__ = _('X server updates (stable)')
    license = GPL
    detail = _('This repository provides latest versions of X.org drivers, libraries.')
    content = ( 'fglrx-installer xfree86-driver-synaptics xserver-xorg-input-vmmouse xserver-xorg-video-ati ' +
                             'xserver-xorg-video-intel xserver-xorg-video-nv' )
    ppa = 'ubuntu-x-swat/x-updates'
        
class Repo_WebkitGTK(_launchpad):
    __doc__ = _('WebkitGTK (stable)')
    license = LGPL
    detail = _('WebkitGTK is the port of Webkit to the GTK+ platform.')
    content = 'webkit pywebkitgtk'
    ppa = 'webkit-team'
    
class Repo_XBMC(_launchpad):
    __doc__ = _('XBMC (stable)')
    license = GPL
    detail = _('XBMC is an open source software media player and entertainment hub for digital media.')
    content = 'xbmc'
    ppa = 'team-xbmc'

class Repo_IBus_Jaunty(_launchpad):
    __doc__ = _('IBus (stable)')
    license = GPL
    content = 'ibus ibus-table ibus-pinyin'
    ppa = 'ibus-dev/ibus-1.2-jaunty'
    def visible(self):
        return VERSION == 'jaunty'

class Repo_IBus_Intrepid(_launchpad):
    __doc__ = _('IBus (stable)')
    license = GPL
    content = 'ibus ibus-table ibus-pinyin'
    ppa = 'ibus-dev/ibus-1.2-intrepid'
    def visible(self):
        return VERSION == 'intrepid'

class Repo_IBus_Karmic(_launchpad):
    __doc__ = _('IBus (stable)')
    license = GPL
    content = 'ibus ibus-table ibus-pinyin'
    ppa = 'ibus-dev/ibus-1.2-karmic'
    def visible(self):
        return VERSION == 'karmic'

class Repo_Canonical_Partner(_repo):
    __doc__ = _('Partners of Canonical')
    detail = _('This repository provides many packages from partners of Canonical.')
    apt_content = 'acroread uex symphony accountz-baz'
    web_page = 'http://archive.canonical.com/ubuntu/dists/'
    apt_file = '/etc/apt/sources.list.d/partners-of-canonical.list'
    apt_conf = [ 'deb http://archive.canonical.com/ubuntu '+VERSION+' partner ' ]
    key_url = ''
    key_id = ''

class Repo_RSSOwl(_repo):
    __doc__ = _('RSSOwl (stable)')
    license = EPL
    detail = _('RSSOwl is an RSS reader.')
    apt_content = 'rssowl'
    web_page = 'http://packages.rssowl.org/README'
    apt_file = '/etc/apt/sources.list.d/rssowl.list'
    apt_conf = [ 'deb http://packages.rssowl.org/ubuntu '+VERSION+' main' ]
    key_url = 'http://packages.rssowl.org/project/rene.moser.pubkey'
    key_id = 'E53168C7'

class Repo_Gmchess(_launchpad):
    __doc__ = _('Gmchess (stable)')
    license = GPL
    Chinese = True
    detail = _('This is a Chinese chess game.')
    content = 'gmchess'
    ppa = 'gmchess'

class Repo_Exaile(_launchpad):
    __doc__ = _('Exaile (beta version)')
    license = GPL
    detail = _('A music manager and player for GTK+ written in Python.')
    content = 'exaile'
    ppa = 'exaile-devel'

class Repo_Audacious(_launchpad):
    __doc__ = _('Audacious (beta version)')
    license = GPL
    detail = _('An advanced audio player.It focused on audio quality and supporting a wide range of audio codecs.')
    content = 'audacious audacious-plugins'
    ppa = 'dupondje'

# Disable Repo_Tor, because the packages are provided in Ubuntu Lucid and Fedora 12/13
#class Repo_Tor(_repo):
#    __doc__ = _('Tor (stable)')
#    license = BSD
#    def __init__(self):
#        self.detail = _('An open network that helps you defend against a form of network surveillance that threatens personal freedom and privacy, '
#        'confidential business activities and relationships, and state security known as traffic analysis.')
#        self.apt_content = 'tor privoxy vidalia'
#        self.web_page = 'http://deb.torproject.org/'
#        self.apt_file = '/etc/apt/sources.list.d/tor.list'
#        self.apt_conf = [ 'deb http://deb.torproject.org/torproject.org '+VERSION+' main' ]
#        self.key_url = ''
#        self.key_id = '886DDD89'
#        _repo.__init__(self)

class Repo_RedNoteBook(_repo):
    __doc__ = _('RedNoteBook (stable)')
    license = GPL
    detail = _('This is a desktop diary application.')
    apt_content = 'rednotebook'
    web_page = 'http://robin.powdarrmonkey.net/ubuntu/'
    apt_file = '/etc/apt/sources.list.d/rednotebook.list'
    apt_conf = [ 'deb http://robin.powdarrmonkey.net/ubuntu '+VERSION+'/' ]
    key_url = 'http://robin.powdarrmonkey.net/ubuntu/repository.key'
    key_id = 'FF95D333'

class Repo_Pidgin_Develop(_launchpad):
    __doc__ = _('Pidgin (beta version)')
    license = GPL
    detail = _('A free chat client used by millions. Connect easily to MSN, Google Talk, Yahoo, AIM and other chat networks all at once.')
    content = 'pidgin'
    ppa = 'pidgin-developers'

class Repo_OSD_Lyrics(_launchpad):
    __doc__ = _('OSD-Lyrics (stable)')
    license = GPL
    detail = _('It displays lyrics. It supports many media players.')
    content = 'osdlyrics'
    ppa = 'osd-lyrics'

class Repo_Acire(_launchpad):
    __doc__ = _('Acire (stable)')
    license = GPL
    content = 'acire'
    ppa = 'acire-team/acire-releases'

class Repo_ElementaryArtwork(_launchpad):
    __doc__ = _('Elementary Theme')
    ppa = 'elementaryart'

class Repo_Docky(_launchpad):
    'Docky'
    ppa = 'docky-core'

class Repo_CairoDock(_launchpad):
    'Cairo Dock'
    ppa = 'cairo-dock-team/weekly'