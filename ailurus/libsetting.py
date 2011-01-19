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
import gtk, pango
from lib import *
from libu import *

class GConfCheckButton(gtk.CheckButton):
    def __toggled(self, w):
        value = self.get_active()
        import gconf
        g = gconf.client_get_default()
        g.set_bool(self.key, value)
    def __init__(self, text, key, tooltip = None):
        gtk.CheckButton.__init__(self)
        self.key = key
        self.set_label(text)
        if not tooltip: tooltip = _('GConf key: ')+key
        else: tooltip += _('\nGConf key: ')+key
        self.set_tooltip_markup(tooltip)
        import gconf
        g = gconf.client_get_default()
        self.set_active( g.get_bool(key) )
        self.connect('toggled', self.__toggled)

class GConfComboBox(gtk.HBox):
    def __init__(self, key, values_shown, values_gconf, tooltip = None, callback = None):
        gtk.HBox.__init__(self, False, 10)
        
        self.key = key
        self.values_gconf = values_gconf
        self.callback = callback
        if self.callback: assert callable(self.callback)
        
        combo = gtk.combo_box_new_text()
        if not tooltip: tooltip = _('GConf key: ')+key
        else: tooltip += _('\nGConf key: ')+key
        combo.set_tooltip_text(tooltip)
        for s in values_shown:
            combo.append_text(s)
        import gconf
        g = gconf.client_get_default()
        value = g.get_string(key)
        for i, s in enumerate(values_gconf):
            if s==value:
                combo.set_active(i)
                break
        combo.connect('changed', self.__option_changed)
        combo.connect('scroll-event', lambda *w:True)
        self.pack_start(combo, False, False)
    def __option_changed(self, combo):
        value = self.values_gconf[ combo.get_active() ]
        import gconf
        g = gconf.client_get_default()
        g.set_string(self.key, value)
        if self.callback: self.callback(value)

class GConfTextEntry(gtk.HBox):
    def __value_changed(self, *w): 
        self.button.set_sensitive(True)
        
    def __button_clicked(self, *w):
        value = self.entry.get_text()
        import gconf
        g = gconf.client_get_default()
        g.set_string(self.key, value)
        self.button.set_sensitive(False)
    
    def __init__(self, key):
        self.key = key
        self.entry = gtk.Entry()    
        import gconf
        g = gconf.client_get_default()
        value = g.get_string(key)
        if value: self.entry.set_text(value) 
        
        self.button = gtk.Button(stock=gtk.STOCK_APPLY)
        self.button.set_sensitive(False)
        self.entry.connect('changed', self.__value_changed)
        self.button.connect('clicked', self.__button_clicked)
        
        tooltip_text = _('GConf key: ') + key
        self.entry.set_tooltip_text(tooltip_text)
        self.button.set_tooltip_text(tooltip_text)
        
        gtk.HBox.__init__(self, False, 5)
        self.pack_start(self.entry, False)
        self.pack_start(self.button, False)

class GConfShortcutKeyEntry(gtk.HBox):
    def grab_key(self, *w):
        import support.keygrabber
        window = support.keygrabber.GrabberWindow ()
        window.main ()
        self.shortcut_entry.set_text(window.shortcut)

    def __entry_value_changed(self, *w):
        import gconf
        g = gconf.client_get_default()
        g.set_string('/apps/metacity/keybinding_commands/' + self.number, self.command_entry.get_text())
        g.set_string('/apps/metacity/global_keybindings/run_' + self.number, self.shortcut_entry.get_text())

    def __clear_entry_content(self, *w):        
        self.command_entry.set_text('')
        self.shortcut_entry.set_text('disabled')
        
    def __init__(self, number):
        is_string_not_empty(number)
        gtk.HBox.__init__(self, False)
        
        import gconf
        g = gconf.client_get_default()

        self.number = number
        self.command_entry = gtk.Entry()
        self.command_entry.set_tooltip_text(_('GConf key: ') + '/apps/metacity/keybinding_commands/' + self.number)
        value = g.get_string('/apps/metacity/keybinding_commands/'+number)
        if value: self.command_entry.set_text(value)
        self.command_entry.connect('changed', self.__entry_value_changed)

        self.shortcut_entry = gtk.Entry()
        self.shortcut_entry.set_tooltip_text(_('GConf key: ') + '/apps/metacity/global_keybindings/run_' + self.number)
        self.shortcut_entry.connect('grab-focus', self.grab_key)
        value = g.get_string('/apps/metacity/global_keybindings/run_'+number)
        if value: self.shortcut_entry.set_text(value)
        self.shortcut_entry.connect('changed', self.__entry_value_changed)
        
        self.clear_entry_content_button = gtk.Button(stock = gtk.STOCK_CLEAR)
        self.clear_entry_content_button.connect('clicked', self.__clear_entry_content)

        self.pack_start(self.command_entry, True)
        self.pack_start(self.shortcut_entry, False)
        self.pack_start(self.clear_entry_content_button, False)

class ImageChooser(gtk.Button):
    import gobject
    __gsignals__ = {'changed':( gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,) ) }
    
    def image_filter(self):
        filter = gtk.FileFilter()
        filter.set_name(_("Images"))
        for type, pattern in [('image/png', '*.png'),
                              ('image/jpeg', '*.jpg'),
                              ('image/gif', '*.gif'),
                              ('image/x-xpixmap', '*.xpm'),
                              ('image/x-svg', '*.svg'),]:
            filter.add_mime_type(type)  
            filter.add_pattern(pattern)
        return filter
    
    def choose_image(self):
        chooser = gtk.FileChooserDialog(_('Choose an image'), None, gtk.FILE_CHOOSER_ACTION_OPEN,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                 gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.set_current_folder(self.default_dir)
        chooser.set_select_multiple(False)
        chooser.add_filter(self.image_filter())
        if chooser.run() == gtk.RESPONSE_OK:
            image_path = chooser.get_filename()
            self.display_image(image_path)
            self.emit('changed', image_path)
        chooser.destroy()
    
    def display_image(self, image_path):
        'If image_path is none, then show blank.'
        child = self.get_child()
        if child: self.remove(child)
        
        if image_path and os.path.exists(image_path):
            self.pixbuf = gtk.gdk.pixbuf_new_from_file(image_path).scale_simple(self.width, self.height, gtk.gdk.INTERP_HYPER)
        else:
            self.pixbuf = blank_pixbuf(self.width, self.height)
        self.add(gtk.image_new_from_pixbuf(self.pixbuf))
        self.show_all()
    def display_pixbuf(self, pixbuf):
        'If image_path is none, then show blank.'
        child = self.get_child()
        if child: self.remove(child)
        
        if pixbuf:
            self.pixbuf = pixbuf.scale_simple(self.width, self.height, gtk.gdk.INTERP_HYPER)
        else:
            self.pixbuf = blank_pixbuf(self.width, self.height)
        self.add(gtk.image_new_from_pixbuf(self.pixbuf))
        self.show_all()
    def __init__(self, default_dir, width, height, tooltip=None):
        assert isinstance(default_dir, str) and default_dir
        assert isinstance(width, int)
        assert isinstance(height, int)
        if tooltip: assert isinstance(tooltip, str)
        self.default_dir = default_dir
        self.width = width
        self.height = height
        gtk.Button.__init__(self)
        if tooltip: self.set_tooltip_text(tooltip)
        self.connect('clicked', lambda *w: self.choose_image())

class GConfNumericEntry(gtk.HBox):
    def __value_changed(self, *w):
        self.button_apply.set_sensitive(True)
    def __apply(self, *w):
        value = self.spin.get_value_as_int()
        import gconf
        g = gconf.client_get_default()
        g.set_int(self.key, value)
        self.button_apply.set_sensitive(False)
    def __init__(self, key, min, max, tooltip=''):
        self.key = key
        
        if tooltip: tooltip+='\n'
        tooltip += _('GConf key: ')+key
        tooltip += _('\nMinimum value: %(min)s. Maximum value: %(max)s.')%{'min':min, 'max':max}
        
        self.spin = spin = gtk.SpinButton()
        spin.set_size_request(100, -1)
        spin.set_range(min, max)
        spin.set_increments(1, 1)
        spin.set_update_policy(gtk.UPDATE_ALWAYS)
        spin.set_numeric(True)
        spin.set_tooltip_text(tooltip)
        spin.set_wrap(False)
        spin.set_snap_to_ticks(True)
        import gconf
        g = gconf.client_get_default()
        value = g.get_int(key)
        spin.set_value(value)
        spin.connect('value-changed', self.__value_changed)
        spin.connect('scroll-event', lambda *w:True)

        self.button_apply = button_apply = gtk.Button( _('Apply') )
        button_apply.set_sensitive(False)
        button_apply.connect('clicked', self.__apply)
        
        gtk.HBox.__init__(self, False, 5)
        self.pack_start(spin, False)
        self.pack_start(button_apply, False)

class GConfHScale(gtk.HScale):
    def __init__(self, gconf_key, min, max, tooltip = ''):
        self.gconf_key = gconf_key
        
        if tooltip: tooltip += '\n'
        tooltip += _('GConf key: ') + gconf_key
        
        gtk.HScale.__init__(self)
        self.set_value_pos(gtk.POS_RIGHT)
        self.set_digits(0)
        self.set_range(min, max)
        import gconf
        g = gconf.client_get_default()
        value = g.get_int(self.gconf_key)
        self.set_value(value)
        self.connect("value-changed", self.__value_changed)
        if tooltip: self.set_tooltip_text(tooltip)
        
    def __value_changed(self, *w):
        new_value = int( self.get_value() )
        import gconf
        g = gconf.client_get_default()
        g.set_int(self.gconf_key, new_value)

class Set:
    array = (
              (D+'sora_icons/s_nautilus.png', _('Nautilus'), 'nautilus', ), 
              (D+'sora_icons/s_desktop.png', _('Desktop'), 'desktop', ), 
              (D+'umut_icons/s_window.png', _('Window effect'), 'window', ), 
              (D+'umut_icons/s_menu.png', _('Menu'), 'menu', ), 
              (D+'umut_icons/s_icon.png', _('Icon'), 'icon', ), 
              (D+'umut_icons/s_font.png', _('Font'), 'font', ), 
              (D+'umut_icons/s_session.png', _('GNOME Session'), 'session', ), 
              (D+'umut_icons/s_panel.png', _('GNOME Panel'), 'panel', ),
              (D+'umut_icons/s_memory.png', _('Memory'), 'memory', ), 
              (D+'umut_icons/s_terminal.png', _('Terminal'), 'terminal', ),
              (D+'umut_icons/s_sound.png', _('Sound'), 'sound', ), 
              (D+'umut_icons/s_power.png', _('Power management'), 'power', ),
              (D+'umut_icons/s_update.png', _('Update'), 'update', ),
              (D+'umut_icons/s_restriction.png', _('Restriction'), 'restriction', ),
              (D+'umut_icons/s_shortcutkey.png', _('Shortcut key'), 'shortcut', ),
              (D+'sora_icons/s_firefox.png', _('Configure Firefox'), 'firefox', ),
              (D+'umut_icons/s_login_window.png', _('Login window'), 'login_window', ),
              (D+'umut_icons/s_compression.png', _('Compression'), 'compression', ),
              (D+'umut_icons/s_gedit.png', _('GEdit'), 'gedit', ),
              (D+'umut_icons/s_screensaver.png', _('Screensaver'), 'screensaver', ),
    )
    valid_categories = [item[2] for item in array]
    category = None # string or list_of_string
    title = None # string
    content = None # gtk.Container
    @classmethod
    def category_list(cls):
        if isinstance(cls.category, str):
            return [cls.category]
        else:
            return cls.category
    @classmethod
    def f(cls): # must override, return gtk.Container
        raise NotImplementedError
    @classmethod
    def get_content(cls):
        if cls.content is None:
            cls.content = gtk.VBox(False, 5)
            cls.content.set_border_width(5)
            cls.content.pack_start(title_label(cls.title), False)
            cls.content.pack_start(cls.f(), False)
        return cls.content
    @classmethod
    def check(cls):
        assert cls.category
        if isinstance(cls.category, str):
            assert cls.category in cls.valid_categories
        elif isinstance(cls.category, list):
            for c in cls.category:
                assert c in cls.valid_categories
        else:
            raise TypeError
    @classmethod
    def contain(cls, another_category):
        if isinstance(cls.category, str):
            return cls.category == another_category
        return another_category in cls.category
    @classmethod
    def visible(cls):
        return True
    
class Setting(gtk.VBox):
    def __title(self, text):
        label = gtk.Label()
        label.set_markup('<b>%s</b>'%text)
        return left_align(label)

    def __init__(self, box, title, category):
        assert isinstance(box, gtk.Container)
        assert isinstance(title, (str, unicode) )
        assert isinstance(category, list)
        assert category != []
        for i in category: 
            assert isinstance(i, str)

        gtk.VBox.__init__(self, False, 0)
        self.set_border_width(5)
        self.pack_start( self.__title(title), False )
        self.pack_start( box, False)
        box.set_border_width(5)
        
        self.category = category

class FirefoxPrefText(gtk.Label):
    def __init__(self, text, key, tips = ''):
        assert isinstance(text, (str, unicode)) and text
        assert isinstance(key, str) and key
        new_text = '%s <small>(<span color="#8A00C2">%s</span>)</small>' % (text, key)
        if tips: new_text += '\n' + '<small><span color="#0072B2">%s</span></small>' % tips
        gtk.Label.__init__(self)
        self.set_markup(new_text)
        self.set_ellipsize(pango.ELLIPSIZE_END)
        self.set_alignment(0, 0.5)
        self.set_selectable(True)

class FirefoxBooleanPref(gtk.HBox):
    def __init__(self, key, default=None):
        assert isinstance(key, str) and key
        if default is not None: assert isinstance(default, bool)
        self.key, self.default = key, default
        self.combo = combo = gtk.combo_box_new_text()
        combo.append_text(_('Yes'))
        combo.append_text(_('No'))
        combo.connect('scroll-event', lambda *w: True)
        gtk.HBox.__init__(self, False, 5)
        self.pack_start(combo, False)
        self.m_get_value()
        combo.connect('changed', lambda *w: self.m_set_value())
    def m_get_value(self):
        try:
            value = bool(firefox.get_pref(self.key))
        except:
            if self.default is not None:
                self.combo.set_active({True:0, False:1}[self.default])
        else:
            self.combo.set_active({True:0, False:1}[value])
    def m_set_value(self):
        index = self.combo.get_active()
        if index == -1: firefox.remove_pref(self.key)
        else: firefox.set_pref(self.key, {0:True, 1:False}[index])
    def set_value(self, new_value):
        assert isinstance(new_value, bool)
        self.combo.set_active({True:0, False:1}[new_value])

class FirefoxComboPref(gtk.HBox):
    def __init__(self, key, texts, values, default=None): # "text" is displayed. "value" is stored in pref.js
        assert isinstance(key, str) and key
        assert isinstance(texts, list) and texts
        assert isinstance(values, list) and values
        assert len(texts) == len(values)
        if default: assert default in values
        self.key, self.texts, self.values, self.default = key, texts, values, default
        self.combo = combo = gtk.combo_box_new_text()
        combo.connect('scroll-event', lambda *w: True)
        for text in self.texts:
            combo.append_text(text)
        gtk.HBox.__init__(self, False, 5)
        self.pack_start(combo, False)
        combo.connect('changed', lambda *w: self.m_set_value())
        self.m_get_value()
    def m_get_value(self):
        try:    value = firefox.get_pref(self.key)
        except:
            if self.default:
                for i in range(len(self.values)):
                    if self.values[i] == self.default:
                        self.combo.set_active(i)
        else:
            for i in range(len(self.values)):
                if self.values[i] == value:
                    self.combo.set_active(i)
    def m_set_value(self):
        i = self.combo.get_active()
        firefox.set_pref(self.key, self.values[i])
    def set_value(self, new_value):
        assert new_value in self.values
        for i in range(len(self.values)):
            if self.values[i] == new_value:
                self.combo.set_active(i)

class FirefoxNumericPref(gtk.Entry):
    def __init__(self, key, default):
        'default is displayed if the preference is not set'
        assert isinstance(key, str) and key
        assert isinstance(default, (int, long))
        self.key = key
        self.default_value = str(default)
        gtk.Entry.__init__(self)
        self.set_width_chars(7)
        self.connect('changed', lambda w: self.m_set_value())
        self.m_get_value()
    def m_get_value(self):
        try:
            value = int(firefox.get_pref(self.key))
        except:
            self.set_text(self.default_value)
        else:
            self.set_text(str(value))
    def m_set_value(self):
        try:
            value = int(self.get_text())
        except:
            pass
        else:
            firefox.set_pref(self.key, value)
    def set_value(self, new_value):
        assert isinstance(new_value, (int, long))
        self.set_text(str(new_value))
        
class FirefoxNumericPref2(gtk.SpinButton): # do not use this class, because min & max is hard to determine
    def __init__(self, key, min, max, default):
        'default_value is displayed if the preference is not set'
        assert isinstance(key, str) and key
        assert isinstance(min, (int, long))
        assert isinstance(max, (int, long))
        assert isinstance(default, (int, long)) and min<=default<=max
        step = max(1, (max-min)/100)
        self.key = key
        self.default_value = default
        gtk.SpinButton.__init__(self)
        self.set_range(min, max)
        self.set_increments(step, step)
        self.set_update_policy(gtk.UPDATE_IF_VALID)
        self.set_numeric(True)
        self.set_wrap(False)
        self.set_snap_to_ticks(True) # if True invalid values should be corrected.
        self.m_get_value()
        self.connect('value-changed', lambda w: self.m_set_value())
    def m_get_value(self):
        try:
            value = int(firefox.get_pref(self.key))
        except:
            self.set_value(self.default_value)
        else:
            self.set_value(value)
    def m_set_value(self):
        value = self.get_value_as_int()
        firefox.set_pref(self.key, value)        

if __name__ == '__main__':
    content_interrupt_parsing_t = FirefoxPrefText(_('whether interrupt parsing a page to respond to UI events?') , 'content.interrupt.parsing')
    content_interrupt_parsing = FirefoxBooleanPref('content.interrupt.parsing')
    content_max_tokenizing_time_t = FirefoxPrefText(_('maximum number of microseconds between two page rendering'), 'content.max.tokenizing.time')
    content_max_tokenizing_time = FirefoxNumericPref('content.max.tokenizing.time', 100000)
    content_maxtextrun_t = FirefoxPrefText(_('maximum number of bytes to split a long text node'), 'content.maxtextrun')
    content_maxtextrun = FirefoxNumericPref('content.maxtextrun', 1024)
    
    table = gtk.Table()
    row = 0
    def add(t, w):
        global table, row
        table.attach(t, 0, 1, row, row+1, gtk.FILL|gtk.EXPAND, gtk.FILL)
        table.attach(w, 1, 2, row, row+1, gtk.FILL, gtk.FILL)
        row += 1
    add(content_interrupt_parsing_t, content_interrupt_parsing)
    add(content_max_tokenizing_time_t, content_max_tokenizing_time)
    add(content_maxtextrun_t, content_maxtextrun)
    window = gtk.Window()
    window.set_position(gtk.WIN_POS_CENTER)
    window.connect('delete-event', gtk.main_quit)
    window.add(table)
    window.show_all()
    window.set_size_request(300, -1)
    gtk.main()
    print firefox.get_pref('content.interrupt.parsing')
    print firefox.get_pref('content.maxtextrun')