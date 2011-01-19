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

class Generic_Genome_Browser(I):
    __doc__ = _('Generic Genome Browser')
    detail = _('Generic Genome Browser is a combination of database and interactive web page '
               'for manipulating and displaying annotations on genomes.\n'
               '<span color="red">Due to the limitation of the authors\' programming ability, '
               '"Generic Genome Browser" cannot be detected or removed by Ailurus.</span>')
    license = AL
    category='biology'
    def install(self):
        if FEDORA:
            for package in ['perl-libwww-perl', 'perl-CPAN']:
                if not RPM.installed(package): RPM.install(package)
        
        f = R('http://gmod.svn.sourceforge.net/viewvc/gmod/Generic-Genome-Browser/trunk/bin/gbrowse_netinstall.pl').download()
        run_as_root_in_terminal('perl ' + f)
    def installed(self):
        return False
    def remove(self):
        raise NotImplementedError

class Bioclipse(_path_lists):
    __doc__ = _('Bioclipse: an awesome Chemical and Biological Informatics application')
    download_url = 'http://sourceforge.net/projects/bioclipse/'
    category = 'biology'
    license = ('Eclipse Public License (EPL) + exception, '
               'see http://www.bioclipse.net/license-0')
    def __init__(self):
        self.shortcut = '/usr/share/applications/bioclipse.desktop'
        self.path = '/opt/bioclipse'
        self.paths = [ self.shortcut, self.path ]
    def install(self):
        if is32():
            f = R(urls.bioclipse32).download()
        else:
            f = R(urls.bioclipse64).download()
        with Chdir('/tmp'):
            run('tar xf "%s"' %f)
            import os
            if not os.path.exists('/opt'): run_as_root('mkdir /opt')
            run_as_root('rm /opt/bioclipse -rf')
            import glob
            path = [path for path in glob.glob('Bioclipse.*') if os.path.isdir(path)]
            run_as_root('cp %s /opt/bioclipse -r' % path[0])
            run_as_root('chown $USER:$USER /opt/bioclipse -R')
            
            create_file(self.shortcut,'''[Desktop Entry]
Name=Bioclipse
Exec=/opt/bioclipse/bioclipse
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Development
Icon=/opt/bioclipse/icon.xpm 
''')
            
            file_append('/opt/bioclipse/bioclipse.ini', '-Dorg.eclipse.swt.browser.XULRunnerPath=/usr/lib/xulrunner/')

class Electric(_path_lists):
    __doc__ = _('Electric: A software for IC design which supports VHDL and Verilog')
    category = 'electronics'
    license = GPL
    download_url = 'http://www.staticfreesoft.com/'
    shortcut = '/usr/share/applications/electric.desktop'
    file = '/opt/electricBinary.jar'
    paths = [shortcut, file]
    def install(self):
        f = R(urls.electric).download()
        if not os.path.exists('/opt'):
            run_as_root('mkdir /opt')
        run_as_root('cp %s %s' % (f, self.file))
        create_file(self.shortcut, '''[Desktop Entry]
Name=Electric
Exec=java -jar %s
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Science;Engineering;'''%self.file)

class RouteConverter(_path_lists):
    'RouteConverter'
    detail = _('Convert GPS log between different formats')
    license = GPL
    download_url = 'http://www.routeconverter.de/en'
    category = 'geography'
    shortcut = '/usr/share/applications/RouteConverter.desktop'
    file = '/opt/RouteConverterLinux.jar'
    paths = [shortcut, file]
    def install(self):
        if is32(): url = urls.routeconverter32
        else: url = urls.routeconverter64
        f = R(url).download()
        if not os.path.exists('/opt'):
            run_as_root('mkdir /opt')
        run_as_root('cp %s %s' % (f, self.file))
        create_file(self.shortcut, '''[Desktop Entry]
Name=RouteConverter
Exec=java -jar %s
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application'''%self.file)

class MyTourbook(_path_lists):
    'MyTourbook'
    detail = _('visualize and analyze tours which are recorded by a GPS device')
    license = GPL
    download_url = 'http://mytourbook.sourceforge.net'
    category = 'geography'
    shortcut = '/usr/share/applications/MyTourbook.desktop'
    file = '/opt/mytourbook'
    paths = [shortcut, file]
    def install(self):
        if is32(): url = urls.mytourbook32
        else: url = urls.mytourbook64
        f = R(url).download()
        if not os.path.exists('/opt'):
            run_as_root('mkdir /opt')
        with Chdir('/opt'):
            run_as_root('unzip -qo "%s"' % f)
        create_file(self.shortcut, '''[Desktop Entry]
Name=MyTourbook
Exec=/opt/mytourbook/mytourbook
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Icon=/opt/mytourbook/icon.xpm''')

class GeoGebra(_path_lists):
    'GeoGebra'
    detail = _('Learning algebra and geometry')
    category = 'math'
    download_url = 'http://www.geogebra.org/cms/'
    shortcut = '/usr/share/applications/GeoGebra.desktop'
    file = '/opt/geogebra'
    paths = [shortcut, file]
    def install(self):
        if is32(): url = urls.geogebra32
        else: url = urls.geogebra64
        f = R(url).download()
        if not os.path.exists('/opt'):
            run_as_root('mkdir /opt')
        with Chdir('/opt'):
            run_as_root('tar xf "%s"' % f)
        create_file(self.shortcut, '''[Desktop Entry]
Name=GeoGebra
Exec=/opt/geogebra/geogebra.sh
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Icon=/opt/geogebra/icon.png''')

def get_sweethome_version():
    if is32(): url = urls.sweethome32
    else:       url = urls.sweethome64
    import re
    match = re.search('SweetHome3D-([0-9.]+)-linux', url)
    return match.group(1)

class SweetHome3D(_path_lists):
    __doc__ = _('SweetHome3D: open source interior design application')
    download_url = 'http://www.sweethome3d.com/'
    category = 'design'
    shortcut = '/usr/share/applications/SweetHome3D.desktop'
    path = '/opt/SweetHome3D-%s' % get_sweethome_version()
    paths = [shortcut, path]
    def install(self):
        if is32(): url = urls.sweethome32
        else:       url = urls.sweethome64
        f = R(url).download()
        run_as_root('mkdir /opt', ignore_error=True)
        with Chdir('/opt'):
            run_as_root('tar xf ' + f)
        create_file(self.shortcut, '[Desktop Entry]\n'
                                   'Name=SweetHome3D\n'
                                   'Exec=' + self.path + '/SweetHome3D\n'
                                   'Encoding=UTF-8\n'
                                   'StartupNotify=true\n'
                                   'Terminal=false\n'
                                   'Type=Application\n'
                                   'Categories=Graphics;\n')

# Do not install it via Launchpad, because the packages there is 1.6. It is old, since 1.8 has been released. 
# Songbird cannot be downloaded from http://developer.songbirdnest.com/builds/trunk/latest/ now :(
#class Songbird(I):
#    __doc__ = _('Songbird: Open source substitution of iTunes')
#    detail = (_('Music player which integrates with online content via plugins. '
#               'Site contains project news, download, add-ons directory, help, and how to contribute.') + '\n' + 
#              _('Launch it by this command:') + ' LD_BIND_NOW=1 ./songbird')
#    download_url = 'http://developer.songbirdnest.com/builds/trunk/latest/' 
#    category = 'player'
#    license = GPL
#    def install(self):
#        open_web_page('http://developer.songbirdnest.com/builds/trunk/latest/')
#    def installed(self):
#        return False
#    def remove(self):
#        pass

class TsingHuaTeXTemplate(_download_one_file):
    __doc__ = _('LaTeX Thesis Templates by Tsing Hua University, China')
    import os
    detail = _('These templates include undergraduate dissertation template, master thesis template and PhD thesis template. '
       'They are developed by Tsing Hua University, China. Official website is http://thuthesis.sourceforge.net/\n'
       'After installation, a file "thuthesis.tgz" is placed in the folder "%s".')%os.environ['HOME']
    category = 'latex'
    Chinese = True
    license = 'GPL'
    def __init__(self):
        self.R = R(urls.tsinghuatex)
        import os
        self.file = os.path.expandvars('$HOME/thuthesis.tgz')

class FFAdblock(_ff_extension):
    __doc__ = _('Adblock+: Block 99% advertisement')
    license = MPL
    detail = _('It is able to block 99% ads and banners.')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/1865'
    name = u'Adblock Plus'
    R = R(latest(1865), filename='adblock_plus.xpi')

class FFAutoProxy(_ff_extension):
    __doc__ = _('AutoProxy: Proxy management via a third party list')
    Chinese = True
    license = MPL
    detail = ''
    download_url = 'https://addons.mozilla.org/zh-CN/firefox/addon/11009'
    name = u'AutoProxy'
    R = R(latest(11009), filename='autoproxy.xpi')

class FFChromifox(_ff_extension): 
    __doc__ = _('Chromifox: Chrome theme')
    license = TRI_LICENSE(MPL, GPL, LGPL)
    detail = _('A coat of Chrome for Firefox')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/8782'
    name = u'Chromifox Basic'
    R = R(latest(8782), filename='chromifox_basic.jar')

class FFCleanHide(_ff_extension):
    __doc__ = _('CleanHide: Delete hidden text in web page')
    license = GPL
    detail = _('If you find that some web page use hidden text and you cannot copy text easily, try this!')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/3648'
    name = u'CleanHide'
    R = R(latest(3648), filename='cleanhide.xpi')

class FFDownloadStatusBar(_ff_extension): 
    __doc__ = _('DownloadStatusBar: Keep track of downloads in a tiny statusbar.')
    license = MPL
    detail = ''
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/26'
    name = u'Download Statusbar'
    R = R(latest(26), filename='download_statusbar.xpi')

class FFDownThemAll(_ff_extension):
    __doc__ = _('DownThemAll: A reliable multithread downloader')
    license = GPL
    detail = _('It is able to download all images on web-pages.')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/201'
    name = u'DownThemAll!'
    R = R(latest(201), filename='downthemall.xpi')

class FFEasyDragToGo(_ff_extension):
    __doc__ = _('EasyDragToGo: Open new tabs by dragging text, links and pictures')
    license = MPL
    detail = ''
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/6639'
    name = u'Easy DragToGo'
    R = R(latest(6639), filename='easy_dragtogo.xpi')

class FFEaseLink(_ff_extension):
    __doc__ = _('Ease Link: Decode Thunder, QQ, Flashget, Rayfile, Namipan links')
    detail = _('Get normal HTML hyperlink from hyperlink dedicated to special software')
    license = MPL
    Chinese = True
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/59133'
    name = u'Ease Link'
    R = R(latest(59133), filename='ease_link.xpi')

class FFFireBug(_ff_extension):
    __doc__ = _('FireBug: Real-time edit and debug CSS/HTML/JavaScript in webpage')
    license = BSD
    detail = _('This is a powerful web development tool.')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/1843'
    name = u'Firebug'
    R = R(latest(1843), filename='firebug.xpi')

class FFFireGesture(_ff_extension):
    __doc__ = _('FireGesture: Execute commands and user scripts by mouse gestures')
    license = MPL
    detail = _('It supports five kinds of mouse gestures.')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/6366'
    name = u'FireGestures'
    R = R(latest(6366), filename='firegestures.xpi')

class FFFlashgot(_ff_extension):
    __doc__ = _('Flashgot: A lightweight and reliable download managers')
    license = GPL
    detail = _("It is able to download all the links, movies and audio clips of a page with a single click.")
    download_url = 'https://addons.mozilla.org/zh-CN/firefox/addon/220'
    name = u'FlashGot'
    R = R(latest(220), filename='flashgot.xpi')

class FFFoxyProxy(_ff_extension):
    __doc__ = _('FoxyProxy: One-click switching proxy')
    license = GPL
    detail = ''
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/2464'
    name = u'FoxyProxy Standard'
    R = R(latest(2464), filename='foxyproxy_standard.xpi')

class FFGMarks(_ff_extension):
    __doc__ = _('GMarks: Synchronize bookmarks with Google Bookmarks service')
    detail = ''
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/2888'
    name = u'GMarks'
    R = R(latest(2888), filename='gmarks.xpi')

class FFGreaseMonkey(_ff_extension):
    __doc__ = _('GreaseMonkey: Make change to web pages')
    license = MIT
    detail = _('This is an extension that allow you to install scripts to make changes to web page, such as adding an HTML signature and bypassing image verification.'
              'You can download hundreds of scripts from http://userscripts.org, or '
              'check out http://wiki.greasespot.net/ to get started to write your own scripts. '
              'The book "Dive into Greasemonkey" is worth reading. It can be downloaded freely from http://diveintogreasemonkey.org/ .' )
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/748'
    name = u'Greasemonkey'
    R = R(latest(748), filename='greasemonke.xpi')

class FFFlashblock(_ff_extension):
    __doc__ = _('Flashblock: blocks Flash animation')
    license = DUAL_LICENSE(GPL, MPL)
    detail = _('Never annoyed by Flash animations')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/433/'
    name = u'Flashblock'
    R = R(latest(433), filename='flashblock.xpi')

class FFLiveHTTPHeaders(_ff_extension):
    __doc__ = _('Live HTTP Headers: View HTTP headers in real-time')
    license = GPL
    detail = ''
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/3829'
    name = u'Live HTTP Headers'
    R = R(latest(3829), filename='live_http_headers.xpi')

class FFNoscript(_ff_extension):
    __doc__ = _('NoScript: Allow active content to run only from sites you trust')
    license = GPL
    detail = _('Allow active content to run only from sites you trust, and protect yourself against XSS and Clickjacking attacks.' )
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/722'
    name = u'NoScript'
    R = R(latest(722), filename='noscript.xpi')

class FFSeoQuake(_ff_extension):
    __doc__ = _('SeoQuake: Help you view search engine parameters of your web site')
    license = MPL
    detail = _('It helps you promote your web sites.')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/3036'
    name = u'SeoQuake'
    R = R(latest(3036), filename='seoquake.xpi')

class FFStylish(_ff_extension):
    __doc__ = _('Stylish: Install themes and skins for websites.')
    license = GPL
    detail = ''
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/2108'
    name = u'Stylish'
    R = R(latest(2108), filename='stylish.xpi')

class FFTamperData(_ff_extension):
    __doc__ = _('Tamper Data: View and modify HTTP/HTTPS headers and post request parameters.')
    license = GPL
    detail = ''
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/966'
    name = u'Tamper Data'
    R = R(latest(966), filename='tamper_data.xpi')

class FFUserAgentSwitcher(_ff_extension):
    __doc__ = _('User Agent Switcher: Camousflag Firefox as other kinds of browsers.')
    license = GPL
    detail = _('It tells the remote websites that you are an IE user.')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/59'
    name = u'User Agent Switcher'
    R = R(latest(59), filename='user_agent_switcher.xpi')

class FFViewSourceChart(_ff_extension):
    __doc__ = _('View Source Chart: Show pretty color-coded HTML source code')
    license = GPL
    detail = _("This extension helps you quickly scan and recognize a document's tags.")
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/655'
    name = u'View Source Chart'
    R = R(latest(655), filename='view_source_chart.xpi')

class FFFirefoxSync(_ff_extension):
    __doc__ = _('Firefox Sync: synchronize bookmarks, browsing history and tabs wherever you go.')
    license = MPL
    detail = ''
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/10868'
    name = u'Firefox Sync'
    R = R(latest(10868), filename='firefox_sync.xpi')

class FFWebDeveloper(_ff_extension):
    __doc__ = _('Web Developer: Web page analysis tools')
    license = LGPL
    detail = _('Many developers installed it.')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/60'
    name = u'Web Developer'
    R = R(latest(60), filename='web_developer.xpi')

class FFYetAnotherSmoothScrolling(_ff_extension):
    __doc__ = _('Yet Another Smooth Scrolling: Customize scrolling behavior')
    license = BSD
    detail = ''
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/5846'
    name = u'Yet Another Smooth Scrolling'
    R = R(latest(5846), filename='yet_another_smooth_scrolling.xpi')

class FFYSlow(_ff_extension):
    __doc__ = _("YSlow: web page performance tuning")
    license = MPL
    detail = _("It helps you improve web page performance. It tells you why web page is slow.")
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/5369'
    name = u'YSlow'
    R = R(latest(5369), filename='yslow.xpi')
        
class FFWebMailNotifier(_ff_extension):
    __doc__ = _('WebMail Notifier: check your email accounts and notify unread emails')
    license = MPL
    detail = _('Supports many email server')
    download_url = 'https://addons.mozilla.org/en-US/firefox/addon/4490'
    name = u'WebMail Notifier'
    R = R(latest(4490), filename='webmail_notifier.xpi')
