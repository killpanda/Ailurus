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
from libsetting import *

class desktop_icon_setting(Set):
    title = _('Desktop icons')
    category = ['desktop', 'icon']
    @classmethod
    def f(cls):
        box = gtk.VBox(False, 5)
        o = GConfCheckButton(_('Show desktop content') + ' ' + _('(take effect at the next time GNOME starts up)'),
                             '/apps/nautilus/preferences/show_desktop')
        box.pack_start(o, False)
    
        o = GConfCheckButton(_('Display "Mounted volume" icon'), '/apps/nautilus/desktop/volumes_visible',
                 _('Put icons linking to mounted volumes on the desktop.'))
        box.pack_start(o, False)
        
        o = GConfCheckButton(_('Display "Computer" icon'), '/apps/nautilus/desktop/computer_icon_visible',
                 _('Put an icon linking to the computer location on the desktop.'))
        box.pack_start(o, False)
        
        o = GConfCheckButton(_('Display "Home folder" icon'), '/apps/nautilus/desktop/home_icon_visible',
                 _('Put an icon linking to the home folder on the desktop.'))
        box.pack_start(o, False)    
            
        o = GConfCheckButton(_('Display "Network server" icon'), '/apps/nautilus/desktop/network_icon_visible',
                 _('Put an icon linking to the Network Servers view on the desktop.'))
        box.pack_start(o, False)
        
        o = GConfCheckButton(_('Display "Trash" icon'),'/apps/nautilus/desktop/trash_icon_visible',
                 _('Put an icon linking to the trash on the desktop.'))
        box.pack_start(o, False)
        
        box.pack_start(label_left_align(_('In order to change the name of "Computer", "Home folder", "Network server" or "Trash" icon,\n'
                                   'please select the icon, then press F2.')), False)
        
        return box

class start_here_icon_setting(Set):
    @classmethod
    def f(cls):
        def apply(imagechooser, old_image):
            scale_image(old_image, '/tmp/start-here.png', 24, 24)
            
            import os
            local_icons_dir = os.path.expanduser('~/.icons')
            for root, dirs, files in os.walk('/usr/share/icons/'):
                for file_name in files:
                    if 'start-here' in file_name and '24' in root:
                        usr_path = os.path.join(root, file_name)
                        local_path = usr_path.replace('/usr/share/icons', local_icons_dir)
                        local_dir = os.path.dirname(local_path)
                        if not os.path.exists(local_dir): run('mkdir -p "%s"' % local_dir)
                        run('cp /tmp/start-here.png "%s"' % local_path)
    
        def get_start_here_icon_path():
            import os , gconf
            g = gconf.client_get_default();
            local_dir = os.path.expanduser('~/.icons')
            theme_name = g.get_string('/desktop/gnome/interface/icon_theme')
            for root, dirs, files in os.walk('/usr/share/icons/' + theme_name):
                for file_name in files:
                    if 'start-here' in file_name and '24' in root:
                        usr_path = os.path.join(root, file_name)
                        local_path = usr_path.replace('/usr/share/icons', local_dir)
                        if os.path.exists(local_path): return local_path
                        elif os.path.exists(usr_path): return usr_path
            return ''
    
        path = get_start_here_icon_path()
        label = gtk.Label(_('The "start-here" icon is %s') % path)
        label.set_alignment(0, 0)
        i = ImageChooser('/usr/share/pixmaps/', 24, 24)
        try:    i.display_image(path)
        except: i.display_image(None) # show blank
        i.connect('changed', apply)
        box = gtk.VBox(False, 0)
        box.pack_start(label, False)
        box.pack_start(left_align(i), False)
        return box
    
    title = _('Change "start-here" icon') + ' ' + _('(take effect at the next time GNOME starts up)')
    category = 'icon'

class login_icon_setting(Set):
    @classmethod
    def f(cls):
        def apply(w, image):
            run('cp %s $HOME/.face' % image)
    
        label = gtk.Label(_('The login icon is %s') % os.path.expanduser('~/.face'))
        label.set_alignment(0, 0)
        i = ImageChooser('/usr/share/pixmaps/', 96, 96, )
        try:    i.display_image(os.path.expanduser('~/.face'))
        except: i.display_image(None) # show blank
        i.connect('changed',apply)
        box = gtk.VBox(False, 0)
        box.pack_start(label, False)
        box.pack_start(left_align(i), False)
        return box
    
    title = _('Change login icon') + ' ' + _('(take effect at the next time GNOME starts up)')
    category = 'icon'
    
class menu_icon_setting(Set):
    @classmethod
    def f(cls):
        vbox = gtk.VBox()
        o = GConfCheckButton(_('Show icons of menu entries'), 
                 '/desktop/gnome/interface/menus_have_icons',
                 _('Whether menus may display an icon next to a menu entry.'))
        vbox.pack_start(o, False)
        return vbox
    
    title = _('Menu entry icons setting')
    category = ['menu', 'icon']

class button_icon_setting(Set):
    @classmethod
    def f(cls):
        vbox = gtk.VBox()
        o = GConfCheckButton(_('Show icon in buttons'), 
                 '/desktop/gnome/interface/buttons_have_icons',
                 _('Whether buttons may display an icon next to text.'))
        vbox.pack_start(o, False)
        return vbox
    
    title = _('Button icons setting')
    category = 'icon'

class disable_terminal_beep(Set):
    @classmethod
    def f(cls):
        box = gtk.VBox(False, 5)
        o = GConfCheckButton(_('Disable terminal bell'), 
                 '/apps/gnome-terminal/profiles/Default/silent_bell',
                 _("If it is set to true, gnome terminal will not generate beep sound when error happens.") )
        box.pack_start(o, False)
        return box
    
    title = _('Terminal beep sound setting')
    category = 'sound'

class more_nautilus_settings(Set):
    @classmethod
    def f(cls):
        table = gtk.Table()
        o = GConfCheckButton(_('Automatically mount CD and flash disks'), 
                 '/apps/nautilus/preferences/media_automount', 
                 _('If set to true, then Nautilus will automatically mount media such as CD and flash disks.'))
        table.attach(o, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
        m = GConfCheckButton(_('Show more permissions setting in file property dialog'),
                    '/apps/nautilus/preferences/show_advanced_permissions' )
        table.attach(m, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        return table
    
    title = _('More Nautilus settings')
    category = 'nautilus'

class font_size_setting(Set):
    @classmethod
    def f(cls):
        def change_font(w, isincrease):
            import gconf
            g = gconf.client_get_default()
            gconf_font_keys = [
              '/apps/nautilus/preferences/desktop_font',
              '/desktop/gnome/interface/document_font_name',
              '/desktop/gnome/interface/font_name',
              '/desktop/gnome/interface/monospace_font_name',
              '/apps/metacity/general/titlebar_font', ]
            for key in gconf_font_keys:
                value = g.get_string(key)
                l = value.rsplit(' ',1)
                size = int(float(l[-1]))
                if isincrease: size += 1
                else: size -= 1
                l[-1] = str(size)
                value = ' '.join(l)
                g.set_string(key, value)
    
        button_increase = image_stock_button(gtk.STOCK_ZOOM_IN, _('Larger font') )
        button_increase.connect('clicked', change_font, True)
        button_increase.set_tooltip_text(
                              _('Change these GConf keys:\n') +
                              '/apps/nautilus/preferences/desktop_font\n'
                              '/desktop/gnome/interface/document_font_name\n'
                              '/desktop/gnome/interface/font_name\n'
                              '/desktop/gnome/interface/monospace_font_name\n'
                              '/apps/metacity/general/titlebar_font')
        button_decrease = image_stock_button(gtk.STOCK_ZOOM_OUT, _('Smaller font') )
        button_decrease.connect('clicked', change_font, False)
        button_decrease.set_tooltip_text(
                              _('Change these GConf keys:\n') +
                              '/apps/nautilus/preferences/desktop_font\n'
                              '/desktop/gnome/interface/document_font_name\n'
                              '/desktop/gnome/interface/font_name\n'
                              '/desktop/gnome/interface/monospace_font_name\n'
                              '/apps/metacity/general/titlebar_font')
        hbox = gtk.HBox(False, 10)
        hbox.pack_start(button_increase, False, False)
        hbox.pack_start(button_decrease, False, False)
        hbox.show_all()
        return hbox
    
    title = _('One-click changing font size')
    category = 'font'

class layout_of_window_titlebar_buttons(Set):
    @classmethod
    def f(cls):
        def gconf_client():
            import gconf
            return gconf.client_get_default()
        
        def radio_button_clicked(radio_button, widget_on_right, widget_on_right2=None):
            widget_on_right.set_sensitive(radio_button.get_active())
            if widget_on_right2: widget_on_right2.set_sensitive(radio_button.get_active())
    
        pre_defined = ['menu:minimize,maximize,close', 'maximize,minimize,close:', 'close,minimize,maximize:']
        
        c = gconf_client()
        layout = c.get_string('/apps/metacity/general/button_layout')
        if layout is None: layout = 'menu:minimize,maximize,close' # default value
        
        label = gtk.Label(_('GConf key: ') + '/apps/metacity/general/button_layout\n'
                               + _("It can be used in Metacity only."))
        label.set_alignment(0, 0)
        r1 = gtk.RadioButton(label=_('Pre-defined:'))
        r2 = gtk.RadioButton(group=r1, label=_('Custom:'))
        o1 = GConfComboBox('/apps/metacity/general/button_layout', 
                          [_('GNOME classic'), _('Ubuntu Lucid beta'), _('MAC OS X')],
                          pre_defined,)
        o2 = gtk.Entry()
        o2.set_text(layout)
        label2 = gtk.Label('Arrangement of buttons on the titlebar.\n'
                           'The value should be a string, such as "menu:minimize,maximize,close";\n'
                           'the colon separates the left corner of the window from the right corner,\n'
                           'and the button names are comma-separated.\n'
                           'Duplicate buttons are not allowed.\n'
                           'Unknown button names are silently ignored.')
        label2.set_selectable(True)
        label2.set_alignment(0, 0)
        def o1_changed(new_value):
            o2.set_text(new_value)
        o1.callback = o1_changed
        r1.connect('clicked', radio_button_clicked, o1)
        r2.connect('clicked', radio_button_clicked, o2, label2)
    
        table = gtk.Table()
        table.attach(label, 0, 2, 0, 1, gtk.FILL, gtk.FILL)
        table.attach(r1, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        table.attach(o1, 1, 2, 1, 2, gtk.FILL|gtk.EXPAND, gtk.FILL)
        table.attach(r2, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
        table.attach(o2, 1, 2, 2, 3, gtk.FILL|gtk.EXPAND, gtk.FILL)
        table.attach(label2, 1, 2, 3, 4, gtk.FILL, gtk.FILL)
        
        if layout in pre_defined:
            r1.set_active(True); o2.set_sensitive(False); label2.set_sensitive(False)
        else:
            r2.set_active(True); o1.set_sensitive(False)
        
        return table
    
    title = _('The layout of window title-bar buttons')
    category = 'window'

class window_behaviour_setting(Set):
    @classmethod
    def f(cls):
        label_double = gtk.Label(_('double-clicked by mouse left button:'))
        label_double.set_tooltip_text(_('The effects of double-clicking on the title bar.')+_('\nGConf key: ')+'/apps/metacity/general/action_double_click_titlebar')
        label_right = gtk.Label(_('clicked by mouse right button:'))
        label_right.set_tooltip_text(_('The effects of right-clicking on the title bar.')+_('\nGConf key: ')+'/apps/metacity/general/action_right_click_titlebar')
        label_middle = gtk.Label(_('clicked by mouse wheel:'))
        label_middle.set_tooltip_text(_('The effects of clicking on the title bar by mouse wheel.')+_('\nGConf key: ')+'/apps/metacity/general/action_middle_click_titlebar')
        table = gtk.Table()
        table.set_col_spacings(5)
        table.attach(label_double, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
        table.attach(
                GConfComboBox(
                  '/apps/metacity/general/action_double_click_titlebar',
                  [_('maximize'),        _('minimize'), _('roll up'),    _('put behind others'), _('maximize horizontally'),             _('maximize vertically') ],
                  ['toggle_maximize', 'minimize', 'toggle_shade', 'lower',                        'toggle_maximize_horizontally',   'toggle_maximize_vertically'],
                  _('The effects of double-clicking on the title bar.')
                  ),
                  1, 2, 0, 1, gtk.FILL, gtk.FILL)
        table.attach(label_right, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        table.attach(
            GConfComboBox(
                  '/apps/metacity/general/action_right_click_titlebar',
                  [_('show menu'), _('maximize'),             _('minimize'), _('roll up'),           _('put behind others'), _('maximize horizontally'),             _('maximize vertically')],
                  ['menu',             'toggle_maximize',        'minimize', 'toggle_shade',         'lower',                        'toggle_maximize_horizontally',   'toggle_maximize_vertically'],
                  _('The effects of right-clicking on the title bar.')
                  ),
                  1, 2, 1, 2, gtk.FILL, gtk.FILL)
        table.attach(label_middle, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
        table.attach(
            GConfComboBox(
                  '/apps/metacity/general/action_middle_click_titlebar',
                  [_('show menu'), _('maximize'),             _('minimize'), _('roll up'),           _('put behind others'), _('maximize horizontally'),             _('maximize vertically')],
                  ['menu',             'toggle_maximize',        'minimize', 'toggle_shade',         'lower',                        'toggle_maximize_horizontally',   'toggle_maximize_vertically'],
                  _('The effects of clicking on the title bar by mouse wheel.')
                  ),
                  1, 2, 2, 3, gtk.FILL, gtk.FILL)
        return table
    
    title = _('Window effect after that window title bar is ...')
    category = 'window'

class textbox_context_menu_setting(Set):
    @classmethod
    def f(cls):
        table = gtk.Table()
        table.set_col_spacings(10)
        o = GConfCheckButton(_('Show "Input method" entry'), '/desktop/gnome/interface/show_input_method_menu',
                 _('This option affects GEdit and all GTK text-boxes.'))
        table.attach(o, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
        o = GConfCheckButton(_('Show "Insert Unicode control character" entry'), '/desktop/gnome/interface/show_unicode_menu',
                 _('This option affects GEdit and all GTK text-boxes.'))
        table.attach(o, 1, 2, 0, 1, gtk.FILL, gtk.FILL)
        return table
    
    title = _('Text-boxes context menu')
    category = 'menu'

class restriction_on_current_user(Set):
    @classmethod
    def f(cls):
        table = gtk.Table()
        table.set_col_spacings(10)
        table.attach(
               label_left_align(_('These settings restrict current user only. They do not affect other users.')),
               0, 2, 0, 1, gtk.FILL, gtk.FILL)
        o = GConfCheckButton(_('Disable Alt+F2 (Launch application)'),
               '/desktop/gnome/lockdown/disable_command_line',
               _('Prevent current user from pressing Alt+F2 to launch applications.') )
        table.attach(o, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        o = GConfCheckButton(_('Disable Ctrl+Alt+L (Lock screen)'),
               '/desktop/gnome/lockdown/disable_lock_screen',
               _('Prevent current user from pressing Ctrl+Alt+L to lock screen.') )
        table.attach(o, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
        o = GConfCheckButton(_('Disable "print" entry in all menus.'),
               '/desktop/gnome/lockdown/disable_printing',
               _('Prevent current user from printing any documents.'))
        table.attach(o, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
        o = GConfCheckButton(_('Disable "print setup" entry in all menus.'),
               '/desktop/gnome/lockdown/disable_print_setup',
               _('Prevent current user from modifying print settings.'))
        table.attach(o, 1, 2, 2, 3, gtk.FILL, gtk.FILL)
        o = GConfCheckButton(_('Disable "save as" entry in all menus.'),
               '/desktop/gnome/lockdown/disable_save_to_disk',
               _('Prevent current user from saving files by "Save as ..." dialog') )
        table.attach(o, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
        o = GConfCheckButton(_('Forbid running multiple GNOME session.'),
               '/desktop/gnome/lockdown/disable_user_switching',
               _('Prevent current user from switching to another account, unless she has logged out from GNOME before switching.') )
        table.attach(o, 1, 2, 3, 4, gtk.FILL, gtk.FILL)
        return table
    
    title = _('Restriction on current user')
    category = 'restriction'

class nautilus_thumbnail_setting(Set):
    @classmethod
    def f(cls):
        table = gtk.Table()
        table.set_col_spacings(10)
        
        import os
        text = label_left_align( _('The thumbnail cache directory is "%s/.thumbnails".')%os.environ['HOME'] )
        table.attach(text, 0, 2, 0, 1, gtk.FILL, gtk.FILL)
    
        label = label_left_align(_('Size of each thumbnail (in pixels):'))
        key = '/apps/nautilus/icon_view/thumbnail_size'
        label.set_tooltip_text(_('GConf key: %s')%key)
        table.attach(label, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        
        o = GConfNumericEntry(key, 16, 96)
        table.attach(o, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
        
        label = label_left_align(_('Maximum size of thumbnail cache (in MBytes):'))
        key = '/desktop/gnome/thumbnail_cache/maximum_size'
        label.set_tooltip_text(_('GConf key: %s')%key)
        table.attach(label, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
        
        o = GConfNumericEntry(key, 0, 2048)
        table.attach(o, 1, 2, 2, 3, gtk.FILL, gtk.FILL)
        
        label = label_left_align(_('Maximum time each thumbnail remains in cache (in days):'))
        key = '/desktop/gnome/thumbnail_cache/maximum_age'
        label.set_tooltip_text(_('GConf key: %s')%key)
        table.attach(label, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
        
        o = GConfNumericEntry(key, 0, 30)
        table.attach(o, 1, 2, 3, 4, gtk.FILL, gtk.FILL)
        
        o = gtk.Button(_('Clean thumbnail image cache') + ' (%s)' % _('command: rm -rf $HOME/.thumbnails/*'))
        def clean(*w):
            os.system('rm -rf $HOME/.thumbnails/*')
            notify(_('Nautilus thumbnail image cache is clean'), ' ')
        o.connect('clicked', clean)
        table.attach(o, 0, 2, 4, 5, gtk.FILL, gtk.FILL)
        
        return table
    
    title = _('Nautilus thumbnail settings')
    category = 'nautilus'

class gnome_session_setting(Set):
    @classmethod
    def f(cls):
        box = gtk.VBox(False, 5)
        o = GConfCheckButton(_('Prompt you before you log out from GNOME.'),
                '/apps/gnome-session/options/logout_prompt',
                _('If its value is false, GNOME session will terminate immediately if you click the menu "System"->"Log out".') )
        box.pack_start(o, False)
        o = GConfCheckButton(_('Allow connection from remote hosts.'),
                '/apps/gnome-session/options/allow_tcp_connections')
        box.pack_start(o, False)
        return box
    
    title = _('GNOME session')
    category = 'session'

class backlight(Set):
    @classmethod
    def f(cls):
        table = gtk.Table()
        table.set_col_spacings(10)
        table.set_row_spacings(5)
        label = gtk.Label(_('LCD brightness when on AC power:'))
        label.set_alignment(0, 0.5)
        label.set_tooltip_text( _('GConf Key: ') + '/apps/gnome-power-manager/backlight/brightness_ac' )
        o = GConfHScale( '/apps/gnome-power-manager/backlight/brightness_ac', 0, 100 )
        table.attach(label, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
        table.attach(o, 1, 2, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL)
        label = gtk.Label(_('LCD dimming amount when on battery:'))
        label.set_alignment(0, 0.5)
        label.set_tooltip_text( _('GConf Key: ') + '/apps/gnome-power-manager/backlight/brightness_dim_battery' )
        o = GConfHScale( '/apps/gnome-power-manager/backlight/brightness_dim_battery', 0, 100 )
        table.attach(label, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        table.attach(o, 1, 2, 1, 2, gtk.FILL|gtk.EXPAND, gtk.FILL)
        return table
    
    title = _('Backlight') + ' ' + _('(valid only for laptops)')
    category = 'power'

class advance_setting(Set):
    @classmethod
    def f(cls):
        box = gtk.VBox(False, 5)
        
        o = GConfCheckButton(_('Display content of your home folder on desktop') + ' ' + _('(take effect at the next time GNOME starts up)'),
                    '/apps/nautilus/preferences/desktop_is_home_dir')
        box.pack_start(o, False)
        
    
        def clicked(button, path):
            if button.get_active():
                os.system('mkdir -p $HOME/.local/share/applications/')
                with open(path, 'w') as f:
                    f.write('[Desktop Entry]\n'
                            'Name=Gnome Control Center\n'
                            'Exec=gnome-control-center\n'
                            'Icon=gnome-control-center\n'
                            'Terminal=false\n'
                            'Type=Application\n'
                            'Categories=System;')
            else:
                os.unlink(path)
    
        path = os.path.expanduser('~/.local/share/applications/gnome-control-center.desktop')
        button = gtk.CheckButton(_('Display "GNOME control center" entry in "System" menu') + ' ' + _('(take effect at the next time GNOME starts up)'))
        button.set_tooltip_text(_('Create a file $HOME/.local/share/applications/gnome-control-center.desktop'))
        button.set_active(os.path.exists(path))
        button.connect('clicked', clicked, path)
        box.pack_start(button, False)
    
        table = gtk.Table()
        table.set_col_spacings(10)    
    
        o = label_left_align(_('Change default file manager to:'))
        table.attach(o, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
        o = GConfTextEntry('/desktop/gnome/session/required_components/filemanager')
        table.attach(o, 1, 2, 2, 3, gtk.FILL, gtk.FILL )
        
        o = label_left_align(_('Change default panel program to:') )
        table.attach(o, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
        o = GConfTextEntry('/desktop/gnome/session/required_components/panel')
        table.attach(o, 1, 2, 3, 4, gtk.FILL, gtk.FILL)
        
        o = label_left_align(_('Change default window manager to:') )
        table.attach(o, 0, 1, 4, 5, gtk.FILL, gtk.FILL)
        o = GConfTextEntry('/desktop/gnome/session/required_components/windowmanager')
        table.attach(o, 1, 2, 4, 5, gtk.FILL, gtk.FILL)
    
        box.pack_start(table, False)

        return box
    
    title = _('Advance settings')
    category = 'desktop'

class login_window_setting(Set):
    @classmethod
    def f(cls):
        box = gtk.VBox(False, 5)
        o = GConfCheckButton(_('Do not list username. You must enter username manually.\n'
                               'To display a username list might be not secure.'),
                             '/apps/gdm/simple-greeter/disable_user_list')
        box.pack_start(o, False)
        o = GConfCheckButton(_('Do not display "restart" button'), '/apps/gdm/simple-greeter/disable_restart_buttons')
        box.pack_start(o, False)
        return box
    
    title = _('Login window settings')
    category = 'login_window'

class login_window_background(Set):
    'the method is on http://blog.roodo.com/rocksaying/archives/12316205.html'
    @classmethod
    def visible(cls):
        if (UBUNTU or UBUNTU_DERIV) and VERSION >= 'karmic': return True
        return False # do not support on Fedora because there is no sudo.
    @classmethod
    def f(cls):
        box = gtk.VBox(False, 5)
    
        def apply(w, image):
            try:
                run_as_root('sudo -u gdm gconftool-2 --set --type string /desktop/gnome/background/picture_filename "%s"' % image)
            except:
                w.display_image(Config.get_login_window_background())
                raise
            else:
                Config.set_login_window_background(image)
    
        i = ImageChooser('/usr/share/backgrounds/', 160, 120,
                         _('The login window background is the gconf value "/desktop/gnome/background/picture_filename" of user "gdm".'))
        i.display_image(Config.get_login_window_background())
        i.connect('changed',apply)
        box = gtk.VBox(False, 0)
        box.pack_start(left_align(i))
        return box
    
    title = _('Change login window background')
    category = 'login_window'

class login_sound(Set):
    @classmethod
    def visible(cls):
        if (UBUNTU or UBUNTU_DERIV) and VERSION >= 'karmic': return True
        return False # do not support on Fedora because there is no sudo.
    @classmethod
    def f(cls):
        enable_sound = gtk.Button(_('Enable GNOME login sound'))
        enable_sound.set_tooltip_text(_('Command:') + ' sudo -u gdm gconftool-2 --set /desktop/gnome/sound/event_sounds --type bool true')
        enable_sound.connect('clicked', lambda *w: run_as_root('sudo -u gdm gconftool-2 --set /desktop/gnome/sound/event_sounds --type bool true'))
    
        disable_sound = gtk.Button(_('Disable GNOME login sound'))
        disable_sound.set_tooltip_text(_('Command:') + ' sudo -u gdm gconftool-2 --set /desktop/gnome/sound/event_sounds --type bool false')
        disable_sound.connect('clicked', lambda *w: run_as_root('sudo -u gdm gconftool-2 --set /desktop/gnome/sound/event_sounds --type bool false'))
        
        box = gtk.HBox(False, 10)
        box.pack_start(enable_sound, False)
        box.pack_start(disable_sound, False)

        return box
    
    title = _('Change GNOME login sound')
    category = ['login_window', 'sound']

class shortcut_setting(Set):
    @classmethod
    def f(cls):
        l1 = gtk.Label(_('Command line'))
        l2 = gtk.Label(_('Shortcut key'))
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(l1, False, False, 60)
        hbox.pack_start(gtk.Label(), True)
        hbox.pack_start(l2, False, False, 60)
        table = gtk.Table()
        table.set_col_spacings(5)
        table.attach(hbox, 0, 2, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL)
        for number in range(1, 13):
            o = label_left_align(_('%2d:' % number))
            table.attach(o, 0, 1, number, number+1, gtk.FILL, gtk.FILL)
            o = GConfShortcutKeyEntry('command_%d' % number)
            table.attach(o, 1, 2, number, number+1, gtk.FILL|gtk.EXPAND, gtk.FILL)
        return table
    
    title = _('Shortcut key')
    category = 'shortcut'

class compression_strategy(Set):
    @classmethod
    def f(cls):
        label = gtk.Label(_('Compression strategy of file-roller:'))
        label.set_tooltip_text(_('GConf key: ') + '/apps/file-roller/general/compression_level')
        combo = GConfComboBox(
                  '/apps/file-roller/general/compression_level',
                  [_('Very high speed'), _('High speed'), _('Balanced'), _('High compression rate') ],
                  ['very_fast',          'fast',          'normal',      'maximum'])
        hbox = gtk.HBox(False, 10)
        hbox.pack_start(label, False)
        hbox.pack_start(combo, False)
        return hbox
    
    title = _('Compression strategy')
    category = 'compression'

class gedit_setting(Set):
    @classmethod
    def f(cls):
        table = gtk.Table()
        table.set_col_spacings(10)
        
        key = '/apps/gedit-2/preferences/editor/undo/max_undo_actions'
        label = gtk.Label(_('Maximum number of undos:'))
        label.set_tooltip_text(_('GConf key: ') + key)
        label.set_alignment(0, 0.5)
        entry = GConfNumericEntry(key, 0, 200)
        table.attach(label, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
        table.attach(entry, 1, 2, 0, 1, gtk.FILL, gtk.FILL)
        
        key = '/apps/gedit-2/preferences/ui/recents/max_recents'
        label = gtk.Label(_('Maximum number of recent files:'))
        label.set_tooltip_text(_('GConf key: ') + key)
        label.set_alignment(0, 0.5)
        entry = GConfNumericEntry(key, 0, 20)
        table.attach(label, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        table.attach(entry, 1, 2, 1, 2, gtk.FILL, gtk.FILL)

        return table
    
    title = _('GEdit settings')
    category = 'gedit'

class screen_saver(Set):
    @classmethod
    def f(cls):
        box = gtk.VBox()
        o = GConfCheckButton(_('Activate screen saver when computer is idle for long time'),
                             '/apps/gnome-screensaver/idle_activation_enabled')
        box.pack_start(o, False)
        o = GConfCheckButton(_('Lock screen when screen saver is activated'),
                             '/apps/gnome-screensaver/lock_enabled')
        box.pack_start(o, False)
        o = GConfCheckButton(_('Lock screen after hibernating'), '/apps/gnome-power-manager/lock/hibernate')
        box.pack_start(o, False)
        o = GConfCheckButton(_('Lock screen after suspending'), '/apps/gnome-power-manager/lock/suspend')
        box.pack_start(o, False)
        return box
    
    title = _('Screensaver')
    category = 'screensaver'