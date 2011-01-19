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
import gtk
import sys, os
from lib import *
from libu import *

def __study_linux():
    study_url_items = [ 
        # text, web page url, Chinese only?
        (_('Ubuntu/Kubuntu configuration guide'),
         'http://ubuntuguide.org/wiki/', False),
        (_('Ubuntu skills'), 
         'http://wiki.ubuntu.org.cn/UbuntuSkills', True),
        (_('Obtain "Full Circle" magazine'), 
         'http://fullcirclemagazine.org/', False),
        (_('Obtain "Ubuntu pocket guide" book'), 
         'http://www.ubuntupocketguide.com/', False),
        (_('Find more third-party repositories on http://repogen.simplylinux.ch/'), 
         'http://repogen.simplylinux.ch/', False),
         ]

    def __get_menu(items):
        ret = []
        for item in items:
            if item[2]==False or (item[2] and Config.is_Chinese_locale()):
                menu_item = image_stock_menuitem(gtk.STOCK_HELP, item[0])
                menu_item.url = item[1]
                menu_item.connect('activate', lambda w: open_web_page(w.url))
                ret.append( menu_item )
        return ret
    
    return __get_menu(study_url_items)

def get_study_linux_menu():
    return __study_linux()
