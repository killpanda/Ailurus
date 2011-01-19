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

class Colorful_BASH_prompt_symbols(C):
    __doc__ = _('Use colorful Bash prompt symbols')
    detail = (_('Add this line into $HOME/.bashrc:') + '\n' + 
              r"PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '")
    bashrc = os.path.expanduser('~/.bashrc')
    line = r"PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '"
    def exists(self):
        if DEEPIN: # Deepin Linux has already adopted colorful BASH prompt symbols
            return False
        return not file_contain(self.bashrc, self.line)
    def cure(self):
        file_append(self.bashrc, self.line)
        notify( _('The color of bash prompt symbols is changed.'), _('It will take effect at the next time you log in.') )

#class Fix_error_in_49_sansserif_conf(C):
#    __doc__ = _('Fix errors in 49-sansserif.conf. Otherwise, some character in Flash would be displayed as blank diamond.')
#    detail = _('Change "sans-serif" to "sans serif".')
#    type = C.MUST_FIX
#    def exists(self):
#        return False # some users found side effect
#        try:
#            with open('/etc/fonts/conf.d/49-sansserif.conf') as f:
#                return '>sans-serif<' in f.read()
#        except IOError: # File does not exist
#            return False
#    def cure(self):
#        with TempOwn('/etc/fonts/conf.d/49-sansserif.conf'):
#            with open('/etc/fonts/conf.d/49-sansserif.conf') as f:
#                content = f.read()
#            content = content.replace('>sans-serif<', '>sans serif<')
#            with open('/etc/fonts/conf.d/49-sansserif.conf', 'w') as f:
#                f.write(content)
#
#class Recover_49_sansserif_conf(C):
#    __doc__ = _('Recover 49-sansserif.conf. Change "sans serif" back to "sans-serif".')
#    detail = _('Ailurus tried to fix Flash font bug. But some users found that font in other applications is also affected.\n'
#               'This operation aims at recovering font configuration file.')
#    def exists(self):
#        try:
#            with open('/etc/fonts/conf.d/49-sansserif.conf') as f:
#                return '>sans serif<' in f.read()
#        except IOError: # File does not exist
#            return False
#    def cure(self):
#        with TempOwn('/etc/fonts/conf.d/49-sansserif.conf'):
#            with open('/etc/fonts/conf.d/49-sansserif.conf') as f:
#                content = f.read()
#            content = content.replace('>sans serif<', '>sans-serif<')
#            with open('/etc/fonts/conf.d/49-sansserif.conf', 'w') as f:
#                f.write(content)

class Add_user_to_vboxusers_group(C):
    __doc__ = _('Add yourself to "vboxusers" group. Otherwise, USB devices cannot be used in VirtualBox.')
    detail = _('Command:') + ' gpasswd -a $USER vboxusers'
    type = C.MUST_FIX
    def exists(self):
        username = os.environ['USER']
        with open('/etc/group') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('vboxusers:'):
                return not username in line
    def cure(self):
        command = os.path.expandvars('gpasswd -a $USER vboxusers')
        run_as_root(command)

class Fix_error_in_fontconfig_properties(C):
    __doc__ = _('Fix errors in Java font configuration. Otherwise, some unicode characters cannot be displayed.')
    detail = _('Change wqy-zenhei.ttf to wqy-zenhei.ttc. Change uming.ttf to uming.ttc.')
    type = C.MUST_FIX
    file = '/etc/java-6-openjdk/fontconfig.properties'
    def exists(self):
        try:
            with open(self.file) as f:
                content = f.read()
            return '/wqy-zenhei.ttf' in content or '/uming.ttf' in content
        except IOError:
            return False
    def cure(self):
        with TempOwn(self.file):
            with open(self.file) as f:
                content = f.read()
            content = content.replace('/wqy-zenhei.ttf', '/wqy-zenhei.ttc')
            content = content.replace('/uming.ttf', '/uming.ttc')
            with open(self.file, 'w') as f:
                f.write(content)

# Not need. Because Java font bug has been fixed in Ubuntu Lucid.
#class Fix_error_in_netbeans_shortcut(C):
#    __doc__ = _('Fix errors in Netbeans shortcut. Otherwise, some unicode characters cannot be displayed.')
#    detail = _("""Add "export _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=on'" """)
#    type = C.MUST_FIX
#    file = '/usr/share/applications/netbeans.desktop'
#    def exists(self):
#        try:
#            with open(self.file) as f:
#                content = f.read()
#            return '\nExec=/usr/bin/netbeans\n' in content
#        except IOError:
#            return False
#    def cure(self):
#        with TempOwn(self.file):
#            with open(self.file) as f:
#                lines = f.readlines()
#            for i, line in enumerate(lines):
#                if line.startswith('Exec='):
#                    lines[i] = """Exec=sh -c "_JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=on' /usr/bin/netbeans" \n"""
#            with open(self.file, 'w') as f:
#                f.writelines(lines)

class Google_chrome_is_upgradable(C):
    __doc__ = _('Google Chrome can be upgraded.')
    detail = _('You are using Google Chrome beta version, but stable version is released.')
    def exists(self):
        return APT.installed('google-chrome-beta')
    def cure(self):
        APT.remove('google-chrome-beta')
        open_web_page('http://www.google.com/chrome/')

# FIXME: After Chinese language support successfully installed, language-pack-zh will be automatically removed.
# Then this item always appears.
#class Install_full_language_support(C):
#    __doc__ = _('Install full language support and input method')
#    def exists(self):
#        lang = Config.get_locale().split('_')[0]
#        list = [
#                'language-pack-' + lang,
#                'language-support-fonts-' + lang,
#                'language-support-input-' + lang,
#                'language-support-translations-' + lang,
#                'language-support-' + lang,
#                'language-support-writing-' + lang,
#                ]
#        if GNOME: list.append('language-pack-gnome-' + lang)
#        if KDE:   list.append('language-pack-kde-' + lang)
#        pkgs = [p for p in list if APT.exist(p) and not APT.installed(p)]
#        self.pkgs = pkgs
#        self.detail = _('Command:') + ' apt-get install ' + ' '.join(self.pkgs)
#        return bool(pkgs)
#    def cure(self):
#        if self.pkgs:
#            APT.install(*self.pkgs)

class Install_GCompris_voice(C):
    __doc__ = _('Install voice data for GCompris')
    def exists(self):
        if not APT.installed('gcompris'): return False
        lang = Config.get_locale().split('_')[0]
        voice = 'gcompris-sound-' + lang
        self.pkg = voice
        self.detail = _('Command:') + ' apt-get install ' + self.pkg
        return APT.exist(voice) and not APT.installed(voice)
    def cure(self):
        APT.install(self.pkg)

class Install_Childsplay_voice(C):
    __doc__ = _('Install voice data for Childsplay')
    def exists(self):
        if not APT.installed('childsplay'): return False
        lang = Config.get_locale().split('_')[0]
        voice = 'childsplay-alphabet-sounds-' + lang
        self.pkg = voice
        self.detail = _('Command:') + ' apt-get install ' + self.pkg
        return APT.exist(voice) and not APT.installed(voice)
    def cure(self):
        APT.install(self.pkg)

#class Sources_list_is_using_wrong_code_name(C):
#    __doc__ = _('/etc/apt/sources.list or /etc/apt/sources.list.d/ contains wrong code name.')
#    def exists(self):
#        lines = [APTSource2.remove_comment(line) for line in APTSource2.all_lines()]
#        self.right_code_name = right_code_name = VERSION
#        self.wrong_code_names = wrong_code_names = set(Config.get_all_Ubuntu_versions())
#        wrong_code_names.discard(right_code_name)
#        wrong = False
#        for line in lines:
#            for c in wrong_code_names:
#                if c in line:
#                    wrong = True
#        self.detail = _('Correct code name is %s. Get code name by "lsb_release -cs".') % right_code_name
#        return wrong
#    def cure(self):
#        for file in APTSource2.all_conf_files():
#            with TempOwn(file):
#                with open(file) as f:
#                    content = f.read()
#                for c in self.wrong_code_names:
#                    content = content.replace(c, VERSION)
#                with open(file, 'w') as f:
#                    f.write(content)

class Remove_ubuntu_docs_package(C):
    __doc__ = _('Remove ubuntu-docs package. Free 270M disk space.')
    detail = _('Command:') + ' apt-get remove ubuntu-docs'
    def exists(self):
        return APT.installed('ubuntu-docs')
    def cure(self):
        APT.remove('ubuntu-docs')