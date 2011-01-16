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
import gtk, pango
from lib import *
from libu import *
from support.checkupdate import *

def __study_linux():
    study_url_items = [ 
        (True, gtk.STOCK_HELP, _('How to compile a LaTeX file into pdf file ?'), 
         'http://tdt.sjtu.edu.cn/ailurus/?p=329', False),
        (True, gtk.STOCK_HELP, _('Check Linux device driver'),
         'http://kmuto.jp/debian/hcl/', False),
         ]

    def __get_menu(items):
        ret = []
        for item in items:
            if item == None: 
                ret.append( gtk.SeparatorMenuItem() )
                continue 
            if item[4]==False or (item[4] and Config.is_Chinese_locale()):
                if item[0]: menu_item = image_stock_menuitem(item[1], item[2])
                else: menu_item = image_file_menuitem(item[2], item[1], 16)
                menu_item.url = item[3]
                menu_item.connect('activate', lambda w: open_web_page(w.url))
                ret.append( menu_item )
        return ret
    
    ret = __get_menu(study_url_items)
    study_show_tip = image_file_menuitem(_('Tip of the day'), D+'sora_icons/m_tip_of_the_day.png', 16)
    def show_day_tip(*w):
        from support.tipoftheday import TipOfTheDay
        TipOfTheDay()
    study_show_tip.connect('activate', show_day_tip)
    ret.insert(0, study_show_tip)
    return ret

def set_proxy_server():
    proxy_string_entry = gtk.Entry()
    try:    proxy_string_entry.set_text(get_proxy_string())
    except: proxy_string_entry.set_text('')
    proxy_table = gtk.Table()
    proxy_table.set_row_spacings(5)
    proxy_table.set_col_spacings(5)
    proxy_table.attach(gtk.Label(_('Proxy string:')), 0, 1, 0, 1, gtk.FILL, gtk.FILL)
    proxy_table.attach(proxy_string_entry, 1, 2, 0, 1)
    label_example = gtk.Label()
    label_example.set_markup('<small>%s</small>'%(_('Example:') + ' http://USERNAME:PASSWORD@inproxy.sjtu.edu.cn:PORTNUMBER/'))
    label_example.set_selectable(True)
    proxy_table.attach(label_example, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
    
    use_proxy = gtk.CheckButton(_('Use a proxy server'))
    def toggled(w):
        Config.set_use_proxy(w.get_active())
        proxy_table.set_sensitive(w.get_active())
        try:
            if w.get_active(): enable_urllib2_proxy()
            else:              disable_urllib2_proxy()
        except:
            print_traceback()
    use_proxy.connect('toggled', toggled)
    use_proxy.set_active(Config.get_use_proxy())
    use_proxy.toggled() # raise "toggled" signal

    dialog = gtk.Dialog(
        _('Set proxy server'), 
        None, gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR, 
        (gtk.STOCK_OK, gtk.RESPONSE_OK) )
    dialog.set_border_width(10)
    dialog.vbox.set_spacing(10)
    dialog.vbox.pack_start(use_proxy, False)
    dialog.vbox.pack_start(proxy_table, False)
    dialog.vbox.show_all()
    dialog.run()
    set_proxy_string(proxy_string_entry.get_text())
    dialog.destroy()

def __preferences():
    menu_query_before_exit = gtk.CheckMenuItem(_('Query before exit'))
    menu_query_before_exit.set_active(Config.get_query_before_exit())
    menu_query_before_exit.connect('toggled', 
            lambda w: Config.set_query_before_exit(w.get_active()))

    set_proxy = gtk.MenuItem(_('Proxy server'))
    set_proxy.connect('activate', lambda w: set_proxy_server())

    return [ set_proxy, menu_query_before_exit ]

def right_label(text):
    font = pango.FontDescription('Georgia')
    ret = gtk.Label(text)
    ret.modify_font(font)
    ret.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#667766"))
    ret.set_alignment(1, 0)
    ret.set_justify(gtk.JUSTIFY_RIGHT)
    return ret

def left_label(text):
    font = pango.FontDescription('Georgia')
    ret = gtk.Label(text)
    ret.modify_font(font)
    ret.set_alignment(0, 0.5)
    ret.set_justify(gtk.JUSTIFY_LEFT)
    ret.set_selectable(True)
    box = gtk.HBox()
    box.pack_start(ret, True, True, 6)
    return box

def url_button(url):
    import gtk, pango
    def func(w, url): open_web_page(url)
    def enter(w, e): 
        try: w.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        except AttributeError: pass
    def leave(w, e): 
        try: w.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
        except AttributeError: pass
    label = gtk.Label()
    label.set_markup("<span color='blue'><u>%s</u></span>"%url)
    font = pango.FontDescription('Georgia')
    label.modify_font(font)
    button = gtk.Button()
    button.connect('clicked', func, url)
    button.connect('enter-notify-event', enter)
    button.connect('leave-notify-event', leave)
    button.set_relief(gtk.RELIEF_NONE)
    button.add(label)
    align = gtk.Alignment(0, 0.5)
    align.add(button)
    return align

def show_contribution_to_ailurus():
    titlelabel = gtk.Label()
    titlelabel.set_markup(_('Contributing to <i>Ailurus</i>'))
    titlelabel.modify_font(pango.FontDescription('Georgia 20'))
    
    table = gtk.Table()
    
    table.set_border_width(15)
    table.set_col_spacings(20)
    table.set_row_spacings(15)
    
    table.attach(titlelabel, 0, 2, 0, 1, gtk.FILL, gtk.FILL)
    
    table.attach(right_label(_('Project homepage:')), 0, 1, 1, 2, gtk.FILL, gtk.FILL)
    table.attach(url_button('http://ailurus.googlecode.com/'), 1, 2, 1, 2, gtk.FILL, gtk.FILL)
    
    table.attach(right_label(_('Project news:')), 0, 1, 2, 3, gtk.FILL, gtk.FILL)
    table.attach(url_button('http://tdt.sjtu.edu.cn/ailurus/'), 1, 2, 2, 3, gtk.FILL, gtk.FILL)
    
    table.attach(right_label(_('Code repository:')), 0, 1, 3, 4, gtk.FILL, gtk.FILL)
    table.attach(url_button('http://github.com/homerxing/Ailurus'), 1, 2, 3, 4, gtk.FILL, gtk.FILL)
    
    table.attach(right_label(_('Bug Tracker:')), 0, 1, 4, 5, gtk.FILL, gtk.FILL)
    table.attach(url_button('http://code.google.com/p/ailurus/issues/list'), 1, 2, 4, 5, gtk.FILL, gtk.FILL)
    
    table.attach(right_label(_('How to submit' '\n' 'patches:')), 0, 1, 5, 6, gtk.FILL, gtk.FILL)
    text = left_label(_('Send me patches on github. No mailing list (yet?) but feel \n'
                      'free to email me about possible features or whatever: \n'
                      'homer.xing@gmail.com'))
    text2 = left_label(_('How to use github? Please read:'))
    box = gtk.VBox(False, 0)
    box.pack_start(text, False)
    box.pack_start(gtk.Label(), False)
    box.pack_start(text2, False)
    box.pack_start(url_button('http://wiki.github.com/homerxing/Ailurus/join-ailurus-development'))
    table.attach(box, 1, 2, 5, 6, gtk.FILL, gtk.FILL)
    
    table.attach(right_label(_('Maintainer of this' '\n' 'metadata page:')), 0, 1, 6, 7, gtk.FILL, gtk.FILL)
    table.attach(left_label('Homer Xing'), 1, 2, 6, 7, gtk.FILL, gtk.FILL)
    
    table.attach(right_label(_('Last modified:')), 0, 1, 7, 8, gtk.FILL, gtk.FILL)
    table.attach(left_label('2010-4-17'), 1, 2, 7, 8, gtk.FILL, gtk.FILL)
    
    dialog = gtk.Dialog(title = _('Contributing to Ailurus'),
                        flags = gtk.DIALOG_NO_SEPARATOR, 
                        buttons = (gtk.STOCK_OK, gtk.RESPONSE_OK))
    dialog.vbox.pack_start(table)
    dialog.vbox.show_all()
    dialog.run()
    dialog.destroy()

def refresh_static_store(store):
    store.clear()
    for key, value in TimeStat.result.items():
        store.append([key, '%.3f s' % value])

def copy_text_to_clipboard(store):
    assert isinstance(store, gtk.ListStore)

    import StringIO
    text = StringIO.StringIO()
    for row in store:
        key = row[0]
        value = row[1]
        print >>text, key
        print >>text, '\t', value
    copy_to_clipboard(text.getvalue())

def show_statistics():
    store = gtk.ListStore(str, str)
    refresh_static_store(store)
    render_1 = gtk.CellRendererText()
    render_2 = gtk.CellRendererText()
    column = gtk.TreeViewColumn()
    column.set_title(_('name'))
    column.pack_start(render_1, False)
    column.add_attribute(render_1, 'text', 0)
    column.set_sort_column_id(0)
    column.set_sort_order(gtk.SORT_ASCENDING)
    column2 = gtk.TreeViewColumn()
    column2.set_title(_('value'))
    column2.pack_start(render_2)
    column2.add_attribute(render_2, 'text', 1)
    column2.set_sort_column_id(1)
    view = gtk.TreeView(gtk.TreeModelSort(store))
    view.append_column(column)
    view.append_column(column2)
    view.set_rules_hint(True)
    button_refresh = gtk.Button(stock=gtk.STOCK_REFRESH)
    button_close = gtk.Button(stock=gtk.STOCK_CLOSE)
    button_copy = gtk.Button(_('Copy text to clipboard'))
    button_box = gtk.HBox(False)
    button_box.pack_end(button_close, False)
    button_box.pack_end(button_refresh, False)
    button_box.pack_end(button_copy, False)
    vbox = gtk.VBox(False, 5)
    vbox.pack_start(view)
    vbox.pack_start(button_box, False)
    vbox.set_border_width(3)
    window = gtk.Window()
    window.set_title( _('Statistical data') )
    window.set_position(gtk.WIN_POS_CENTER)
    window.add(vbox)
    window.show_all()
    button_copy.connect('clicked', lambda w: copy_text_to_clipboard(store))
    button_refresh.connect('clicked', lambda w: refresh_static_store(store))
    button_close.connect('clicked', lambda w: window.destroy())

def __others():
    help_contribute = gtk.MenuItem(_('Contributing to Ailurus'))
    help_contribute.connect('activate', lambda w: show_contribution_to_ailurus())
    
    help_blog = image_stock_menuitem(gtk.STOCK_HOME, _('Ailurus blog'))
    help_blog.connect('activate', 
        lambda w: open_web_page('http://tdt.sjtu.edu.cn/ailurus/' ) )
    
    help_update = image_file_menuitem(_('Check for updates'), D+'suyun_icons/m_check_update.png', 16) 
    def callback(*w):
        while gtk.events_pending(): gtk.main_iteration()
        import thread
        thread.start_new_thread(check_update, ())
    help_update.connect('activate', callback)

    help_propose_suggestion = image_file_menuitem(_('Propose suggestion'), D+'umut_icons/m_propose_suggestion.png', 16)
    def propose_suggestion(*w):
        from support.gae import ProposeSuggestionWindow
        ProposeSuggestionWindow()
    help_propose_suggestion.connect('activate', propose_suggestion)

    help_report_bug = image_file_menuitem(_('Report bugs'), D+'umut_icons/bug.png', 16)
    help_report_bug.connect('activate', 
        lambda w: report_bug() )
    
    help_translate = image_stock_menuitem(gtk.STOCK_CONVERT, _('Translate this application'))
    help_translate.connect('activate', 
        lambda w: open_web_page('https://translations.launchpad.net/ailurus/trunk' ) )
    
    special_thank = gtk.MenuItem( _('Special thanks') )
    special_thank.connect('activate', lambda *w: show_special_thank_dialog())
    
    about = gtk.MenuItem( _('About') )
    about.connect('activate', lambda *w: show_about_dialog())
    
#    changelog = gtk.MenuItem( _('Read changelog') )
#    changelog.connect('activate', lambda *w: show_changelog())
    
    statistics = gtk.MenuItem( _('Statistical data') )
    statistics.connect('activate', lambda *w: show_statistics())
    
    return [ 
#             changelog, 
             help_contribute, help_blog, help_update, 
             help_propose_suggestion, 
             help_report_bug, help_translate, special_thank, about, statistics, ]
   
def get_study_linux_menu():
    return __study_linux()

def get_preferences_menu():
    return __preferences()

def get_others_menu():
    return __others()
