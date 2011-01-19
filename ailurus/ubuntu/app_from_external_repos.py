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

class Acire(_apt_install):
    __doc__ = _('Acire: A Python code fragment manager')
    license = GPL
    category = 'saber'
    ppa = 'acire-team/acire-releases'
    pkgs = 'acire'
    def visible(self):
        return VERSION not in ['hardy', 'intrepid', 'jaunty']

class Audacious(_apt_install):
    __doc__ = _('Audacious: Audio player')
    license = GPL
    category = 'player'
    ppa = 'dupondje'
    pkgs = 'audacious audacious-plugins'
    
class Blueman(_apt_install):
    __doc__ = _('Blueman: Graphical blue-tooth manager')
    license = GPL
    category = 'others'
    ppa = 'blueman'
    pkgs = 'blueman'
    
class Christine(_apt_install):
    __doc__ = _('Christine: Media player')
    license = GPL
    category = 'player'
    ppa = 'markuz'
    pkgs = 'christine'
    
class Chromium(_apt_install):
    __doc__ = _('Chromium: Web browser')
    license = BSD
    category = 'browser'
    ppa = 'chromium-daily'
    pkgs = 'chromium-browser'
    
#class ComicVODPlayer_new(I):
#    __doc__ = _('Mplayer with "vod" protocol support')
#    detail = _('Install mplayer and comicview. Mplayer supports "vod" protocol. "vod" protocol is used in some online video sites such as SJTU comic.')
#    category = 'player'
#    Chinese = True
#    license = GPL
#    ppa = 'homer-xing/mplayer-vod'
#    def __init__(self):
#        self.comicview = ComicView()
#    def install(self):
#        if not self.comicview.installed():
#            self.comicview.install()
#        # Remove current mplayer. Then install a newer version.
#        to_remove = [ p for p in APT.get_installed_pkgs_set() if p.startswith('mplayer') ]
#        APT.remove(*to_remove)
#        APT.install('mplayer', 'mplayer-gui')
#        # Remove repository
#        Repo_Mplayer_VOD().remove()
#    def installed(self):
#        return self.comicview.installed() and APT.installed('mplayer')
#    def remove(self):
#        APT.remove('mplayer')
#    def visible(self):
#        return APT.installed('firefox')

#class ComicView(_ff_extension):
#    __doc__ = 'ComicView: Enjoy video on comic.sjtu.edu.cn'
#    license = GPL
#    Chinese = True
#    desc = ''
#    download_url = 'http://ailurus.googlecode.com/files/comicview-0.2.8.xpi'
#    name = u'Comic Viewer'
#    R = R(['http://ailurus.googlecode.com/files/comicview-0.2.8.xpi'])
#    def visible(self):
#        return False

class Exaile(_apt_install):
    __doc__ = _('Exaile: Audio player')
    license = GPL
    category = 'player'
    ppa = 'exaile-devel'
    pkgs = 'exaile'

class Firefox_3_6(_apt_install):
    __doc__ = _('Firefox 3.6')
    license = TRI_LICENSE(MPL, GPL, LGPL)
    category = 'browser'
    ppa = 'mozillateam/firefox-stable'
    pkgs = 'firefox'
    def visible(self): # Hide it in Lucid. Since Firefox is 3.6.3 in Lucid.
        return VERSION in ['hardy', 'intrepid', 'jaunty', 'karmic']

class Getting_things_gnome(_apt_install):
    __doc__ = _('Getting Things Gnome: GTD tool')
    license = GPL
    category = 'business'
    logo = 'gtg.png'
    ppa = 'gtg'
    pkgs = 'gtg'

class Gmchess(_apt_install):
    __doc__ = _('Gmchess: Chinese chess game')
    license = GPL
    category = 'game'
    ppa = 'gmchess'
    pkgs = 'gmchess'

class Gnome_color(_apt_install):
    __doc__ = _('GNOME colors themes')
    license = GPL
    category = 'theme'
    ppa = 'gnome-colors-packagers'
    pkgs = 'gnome-colors'
    DE = 'gnome'
    def visible(self):
        return VERSION != 'lucid'

class Gnome_global_menu(_apt_install):
    __doc__ = _('Global Menu: A globally shared menu bar')
    license = GPL
    category = 'others'
    ppa = 'globalmenu-team'
    pkgs = 'gnome-globalmenu'
    DE = 'gnome'
    def visible(self):
        return VERSION != 'maverick'

class Gnome_global_menu_for_maverick(_apt_install):
    __doc__ = _('Global Menu: A globally shared menu bar')
    license = GPL
    category = 'others'
    ppa = 'nilarimogard/webupd8'
    pkgs = 'gnome-globalmenu'
    DE = 'gnome'
    def visible(self):
        return VERSION == 'maverick'

class Moovida(_apt_install):
    __doc__ = _('Moovida: Media player')
    license = GPL
    category = 'player'
    ppa = 'moovida-packagers'
    pkgs = 'moovida'

class OSD_Lyrics(_apt_install):
    __doc__ = _('OSD-Lyrics: Display lyrics')
    category = 'others'
    license = GPL
    ppa = 'osd-lyrics'
    pkgs = 'osdlyrics'

# Yeah, we can install playonlinux now!
class PlayOnLinux(_apt_install):
    __doc__ = _('PlayOnLinux: A graphical front-end for wine')
    license = LGPL
    category = 'simulator'
    deb = 'deb http://deb.playonlinux.com/ %s main' % VERSION
    pkgs = 'playonlinux'

class RSSOwl(_apt_install):
    __doc__ = _('RSSOwl: RSS feed reader')
    license = EPL
    category = 'rss'
    deb = 'deb http://packages.rssowl.org/ubuntu %s main' % VERSION
    pkgs = 'rssowl'

class RedNoteBook(_apt_install):
    __doc__ = _('RedNoteBook: A desktop diary application')
    license = GPL
    category = 'business'
    deb = 'deb http://robin.powdarrmonkey.net/ubuntu %s/' % VERSION
    pkgs = 'rednotebook'
    def visible(self):
        return VERSION != 'lucid'

class XBMC(_apt_install):
    __doc__ = _('XBMC: Home entertainment system')
    category = 'player'
    license = GPL
    ppa = 'team-xbmc'
    pkgs = 'xbmc xbmc-standalone'

class ElementaryTheme(_apt_install):
    __doc__ = _('Elementary: Beautiful theme which looks like Mac OS X')
    category = 'theme'
    ppa = 'elementaryart'
    pkgs = 'elementary-icon-theme elementary-theme elementary-wallpapers'

class Docky(_apt_install):
    'Docky'
    detail = _('Simple GNOME dock')
    category = 'panel'
    ppa = 'docky-core'
    pkgs = 'docky'

class CairoDock(_apt_install):
    'Cairo-Dock'
    detail = _('A dock, a taskbar, and many applets')
    category = 'panel'
    ppa = 'cairo-dock-team/weekly'
    pkgs = 'cairo-dock cairo-dock-plug-ins'

# It is not available in Launchpad :(
#class Songbird(_apt_install):
#    __doc__ = _('Songbird: Open source substitution of iTunes')
#    detail = _('Music player which integrates with online content via plugins. '
#               'Site contains project news, download, add-ons directory, help, and how to contribute.')
#    category = 'player'
#    ppa = 'songbird-daily'
#    pkgs = 'songbird'

class DeaDBeeF(_apt_install):
    'DeaDBeef'
    detail = _('Till now the only music player that can correctly play files from .cue sheets')
    category = 'player'
    ppa = 'alexey-smirnov/deadbeef'
    pkgs = 'deadbeef'

class Mobloquer(_apt_install):
    'Mobloquer'
    detail = _('Protect your privacy. Block internet traffic based on IP address ranges.')
    category = 'internet'
    ppa = 'jre-phoenix'
    pkgs = 'moblock mobloquer'

class Backintime(_apt_install):
    __doc__ = 'Back In Time'
    detail = _('Incremental backup tool supporting schedule')
    category = 'security'
    ppa = 'bit-team/testing'
    pkgs = 'backintime-gnome'

class Handbrake(_apt_install):
    'Handbrake'
    detail = _('Convert video into other forms so they can be viewed on portable devices')
    category = 'media_editor'
    ppa = 'stebbins/handbrake-snapshots'
    pkgs = 'handbrake-gtk'

class OpenFetion(_apt_install):
    'Openfetion'
    detail = _('''An client for China Mobile's "Fetion" service''')
    licese = GPL
    category = 'chat'
    ppa = 'happyaron/ppa'
    pkgs = 'openfetion'
    Chinese = True
