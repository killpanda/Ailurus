#!/usr/bin/env python
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
import gtk, os, sys
from lib import *
from libu import *
from loader import *

def detect_proxy_env():
    if 'http_proxy' in os.environ and Config.get_use_proxy() == False:
        proxy_string = os.environ['http_proxy']
        message = _('You have set an environment variable <i>http_proxy=%s</i>.\n'
                    'Would you like to let Ailurus use a proxy server?') % proxy_string
        dialog = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION,
                                   buttons=gtk.BUTTONS_YES_NO)
        dialog.set_markup(message)
        ret = dialog.run()
        dialog.destroy()
        if ret == gtk.RESPONSE_YES:
            try:
                set_proxy_string(proxy_string)
                Config.set_use_proxy(True)
            except:
                print_traceback()
            else:
                dialog = gtk.MessageDialog(type=gtk.MESSAGE_INFO,
                                           buttons=gtk.BUTTONS_OK,
                                           message_format=_('Successfully adopted a proxy server'))
                dialog.run()
                dialog.destroy()
        else:
            os.unsetenv('http_proxy')

def detect_running_instances():
    string = get_output('pgrep -u $USER ailurus', True)
    if string!='':
        notify(_('Warning!'), 
           _('Another instance of Ailurus is running. '
              'It is not recommended to run multiple instance concurrently.') )

def change_task_name():
    import ctypes
    libc = ctypes.CDLL('libc.so.6')
    libc.prctl(15, 'ailurus', 0, 0, 0)

def set_default_window_icon():
    gtk.window_set_default_icon_from_file(D+'suyun_icons/default.png')

def with_same_content(file1, file2):
    import os
    if not os.path.exists(file1) or not os.path.exists(file2):
        return False
    with open(file1) as f:
        content1 = f.read()
    with open(file2) as f:
        content2 = f.read()
    return content1 == content2

def check_required_packages():
    debian_missing = []
    ubuntu_missing = []
    fedora_missing = []
    archlinux_missing = []

    try: import pynotify
    except: 
        debian_missing.append('python-notify')
        ubuntu_missing.append('python-notify')
        fedora_missing.append('notify-python')
        archlinux_missing.append('python-notify')
    try: import vte
    except: 
        debian_missing.append('python-vte')
        ubuntu_missing.append('python-vte')
        fedora_missing.append('vte')
        archlinux_missing.append('vte')
    try: import apt
    except: 
        debian_missing.append('python-apt')
        ubuntu_missing.append('python-apt')
    try: import rpm
    except: 
        fedora_missing.append('rpm-python')
    try: import dbus
    except: 
        debian_missing.append('python-dbus')
        ubuntu_missing.append('python-dbus')
        fedora_missing.append('dbus-python')
        archlinux_missing.append('dbus-python')
    try: import gnomekeyring
    except:
        debian_missing.append('python-gnomekeyring')
        ubuntu_missing.append('python-gnomekeyring')
        fedora_missing.append('gnome-python2-gnomekeyring')
        archlinux_missing.append('python-gnomekeyring') # I am not sure. python-gnomekeyring is on AUR. get nothing from pacman -Ss python*keyring 
    if not os.path.exists('/usr/bin/unzip'):
        debian_missing.append('unzip')
        ubuntu_missing.append('unzip')
        fedora_missing.append('unzip')
        archlinux_missing.append('unzip')
    if not os.path.exists('/usr/bin/wget'):
        debian_missing.append('wget')
        ubuntu_missing.append('wget')
        fedora_missing.append('wget')
        archlinux_missing.append('wget')
    if not os.path.exists('/usr/bin/gdebi-gtk'):
        debian_missing.append('gdebi')
        ubuntu_missing.append('gdebi')
        
    try: # detect policykit version 0.9.x
        import dbus
        obj = dbus.SystemBus().get_object('org.freedesktop.PolicyKit', '/')
        obj = dbus.Interface(obj, 'org.freedesktop.PolicyKit')
        has_policykit_0 = True
    except ImportError:
        has_policykit_0 = True # We cannot detect PolicyKit if we haven't dbus.
    except:
        has_policykit_0 = False
    try: # detect policykit version 1.x
        import dbus
        obj = dbus.SystemBus().get_object('org.freedesktop.PolicyKit1', '/org/freedesktop/PolicyKit1/Authority')
        obj = dbus.Interface(obj, 'org.freedesktop.PolicyKit1.Authority')
        has_policykit_1 = True
    except ImportError:
        has_policykit_1 = True # We cannot detect PolicyKit if we haven't dbus.
    except:
        has_policykit_1 = False
    if not has_policykit_0 and not has_policykit_1:
        debian_missing.append('policykit-1-gnome (or polkit-kde-1)')
        ubuntu_missing.append('policykit-gnome (or policykit-kde or policykit-1-gnome)') # FIXME: It is not good to list all these packages. Should be more precise.
        # FIXME: policykit-1-kde does not exist in Ubuntu.
        fedora_missing.append('polkit-gnome (or polkit-kde)')
        archlinux_missing.append('polkit-gnome (or polkit-kde)')

    error = (
             (DEBIAN and debian_missing)
             or ((UBUNTU or UBUNTU_DERIV) and ubuntu_missing)
             or (FEDORA and fedora_missing)
             or (ARCHLINUX and archlinux_missing)
            )
    if error:
        import StringIO
        message = StringIO.StringIO()
        print >>message, _('Necessary packages are not installed. Ailurus cannot work.')
        print >>message, ''
        print >>message, _('Please install these packages:')
        print >>message, ''
        if DEBIAN:
            print >>message, '<span color="blue">', ', '.join(debian_missing), '</span>'
        elif UBUNTU or UBUNTU_DERIV:
            print >>message, '<span color="blue">', ', '.join(ubuntu_missing), '</span>'
        elif FEDORA:
            print >>message, '<span color="blue">', ', '.join(fedora_missing), '</span>'
        elif ARCHLINUX:
            print >>message, '<span color="blue">', ', '.join(archlinux_missing), '</span>'
        dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
        dialog.set_title('Ailurus ' + AILURUS_VERSION)
        dialog.set_markup(message.getvalue())
        dialog.run()
        dialog.destroy()

def check_home_dir_permission():
    try: Config.check_permission()
    except: pass
    else: return

    import StringIO
    msg = StringIO.StringIO()
    print >>msg, _('Your home folder is not owned by yourself.\n'
                   'Please run the following command to fix the error.')
    user = os.environ['USER']
    home = os.environ['HOME']
    command = 'sudo chown -R %s:%s %s' % (user, user, home)
    print >>msg, '<span color="blue">%s</span>' % command,
    
    dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
    dialog.set_title(_('Fatal error'))
    dialog.set_markup(msg.getvalue())
    dialog.run()
    dialog.destroy()

def check_dbus_daemon_status():
    if not with_same_content('/etc/dbus-1/system.d/cn.ailurus.conf', '/usr/share/ailurus/support/cn.ailurus.conf'):
        correct_conf_files = False
    elif not with_same_content('/usr/share/dbus-1/system-services/cn.ailurus.service', '/usr/share/ailurus/support/cn.ailurus.service'):
        correct_conf_files = False
    else:
        correct_conf_files = True

    try:
        running_version = get_dbus_daemon_version()
    except:
        print_traceback()
        running_version = 0
    from daemon import version as current_version
    same_version = (current_version == running_version)
    
    daemon_current = A+'/daemon.py'
    daemon_installed = '<None>'
    try:
        import ailurus
    except:
        same_daemon = False
    else:
        daemon_installed = os.path.dirname(os.path.abspath(ailurus.__file__))+'/daemon.py'
        same_daemon = with_same_content(daemon_current, daemon_installed)
    
    if correct_conf_files and same_version and same_daemon: return
    def show_text_dialog(msg, icon=gtk.MESSAGE_ERROR):
        dialog = gtk.MessageDialog(type=icon, buttons=gtk.BUTTONS_OK)
        dialog.set_title('Ailurus')
        dialog.set_markup(msg)
        dialog.run()
        dialog.destroy()
    import StringIO
    message = StringIO.StringIO()
    print >>message, _('Error happened. You cannot install any software by Ailurus. :(')
    print >>message, ''
    if not correct_conf_files:
        print >>message, _('System configuration file should be updated.')
        print >>message, _('Please run these commands using <b>su</b> or <b>sudo</b>:')
        print >>message, ''
        print >>message, '<span color="blue">', 'cp /usr/share/ailurus/support/cn.ailurus.conf /etc/dbus-1/system.d/cn.ailurus.conf', '</span>'
        print >>message, '<span color="blue">', 'cp /usr/share/ailurus/support/cn.ailurus.service /usr/share/dbus-1/system-services/cn.ailurus.service', '</span>'
        print >>message, ''
        show_text_dialog(message.getvalue())
    elif not same_daemon:
        print >>message, _('Please re-install Ailurus.')
        print >>message, _('Because file contents are different:')
        print >>message, '<span color="blue">', daemon_current, '</span>'
        print >>message, '<span color="blue">', daemon_installed, '</span>'
        show_text_dialog(message.getvalue())
    elif not same_version:
        print >>message, _('We need to restart Ailurus daemon.')
        print >>message, _('Old version is %s.') % running_version, _('New version is %s') % current_version
        print >>message, ''
        print >>message, _('Press this button to restart daemon. Require authentication.')
        show_text_dialog(message.getvalue())
        try:
            restart_dbus_daemon()
            show_text_dialog(_('Ailurus daemon successfully restarted. Ailurus will work fine.'), icon=gtk.MESSAGE_INFO)
        except:
            show_text_dialog(_("Cannot restart Ailurus daemon. Please restart your computer."))
            print_traceback()

def wait_firefox_to_create_profile():
    if os.path.exists('/usr/bin/firefox'):
        propath = os.path.expanduser('~/.mozilla/firefox/profiles.ini')
        if not os.path.exists(propath):
            KillWhenExit.add('firefox -no-remote')
            import time
            start = time.time()
            while not os.path.exists(propath) and time.time() - start < 6:
                time.sleep(0.1)

sys.excepthook = exception_happened

class toolitem(gtk.ToolItem):
    def __load_image(self):
        pixbuf = get_pixbuf(self.icon, self.image_size, self.image_size)
        image = gtk.image_new_from_pixbuf(pixbuf)
        child = self.align_image.get_child()
        if child:
            self.align_image.remove(child)
        self.align_image.add(image)
        self.align_image.set_size_request(3*self.image_size/2, -1)
        self.align_image.show_all()
    
    def refresh(self, size):
        if self.image_size != size:
            self.image_size = size
            self.__load_image()
            self.__change_font_size()
    
    def __change_font_size(self):
        import pango
        if self.image_size <= 25:
            font_size = 4
        elif 25 < self.image_size <= 30:
            font_size = 5
        elif 30 < self.image_size <= 40:
            font_size = 6
        else:
            font_size = 8
        self.text.modify_font(pango.FontDescription('Sans %s' % font_size))
        
    def __init__(self, icon, text, signal_name, callback, *callback_args):
        gtk.ToolItem.__init__(self)
        
        is_string_not_empty(icon)
        is_string_not_empty(text)
        is_string_not_empty(signal_name)
        assert callable(callback)
        
        self.image_size = 40;
        self.icon = icon
        self.align_image = align_image = gtk.Alignment(0.5, 0.5)
        self.__load_image()
        self.text = text = gtk.Label(text)
        import pango
        text.modify_font(pango.FontDescription('Sans 9'))
        text.set_alignment(0.5, 0.5)
        text.set_justify(gtk.JUSTIFY_CENTER)
        vbox = vbox = gtk.VBox(False, 5)
        vbox.pack_end(text)
        vbox.pack_end(align_image)
        button = gtk.Button()
        button.add(vbox)
        button.set_relief(gtk.RELIEF_NONE)
        button.connect(signal_name, callback, *callback_args)
        self.add(button)

class PaneLoader:
    def __init__(self, main_view, pane_class, content_function = None):
        import gobject
        assert isinstance(pane_class, gobject.GObjectMeta)
        assert callable(content_function) or content_function is None
        self.main_view = main_view
        self.pane_class = pane_class
        self.content_function = content_function
        self.pane_object = None
    def get_pane(self):
        if self.pane_object is None:
            if self.content_function: arg = [self.content_function()] # has argument
            else: arg = [] # no argument
            with TimeStat(self.pane_class.__name__):
                self.pane_object = self.pane_class(self.main_view, *arg)
        return self.pane_object
    def need_to_load(self):
        return self.pane_object is None

def create_menu_from(menuitems):
    assert isinstance(menuitems, list)
    menu = gtk.Menu()
    for item in menuitems:
        menu.append(item)
    menu.show_all()
    return menu

class DefaultPaneMenuItem(gtk.CheckMenuItem):
    def __init__(self, text, value, group):
        'text is displayed. value is saved in Config. group consists of all menu items'
        assert isinstance(text, str)
        assert isinstance(value, str)
        assert isinstance(group, list)
        for obj in group:
            assert isinstance(obj, gtk.CheckMenuItem)
        self.text = text.replace('\n', '')
        self.value = value
        self.group = group
        gtk.CheckMenuItem.__init__(self, self.text)
        self.set_draw_as_radio(True)
        self.set_active(Config.get_default_pane() == value)
        self.connect('toggled', lambda w: self.toggled())
    def toggled(self):
        if self.get_active():
            Config.set_default_pane(self.value)
            for obj in self.group:
                if obj != self:
                    obj.set_active(False)
        self.set_active(Config.get_default_pane() == self.value)

class MainView:
    def create_default_pane_menu(self):
        'Create a menu, to select default pane.'
        menuitems = []
        reversed_order = self.ordered_key[:]
        reversed_order.reverse()
        for key in reversed_order:
            pane = self.contents[key]
            assert hasattr(pane, 'pane_class') # pane is a PaneLoader object
            assert hasattr(pane.pane_class, 'text')
            item = DefaultPaneMenuItem(pane.pane_class.text, pane.pane_class.__name__, menuitems)
            menuitems.append(item)
        return create_menu_from(menuitems)
    
    def add_quit_button(self):
        item_quit = toolitem(D+'sora_icons/m_quit.png', _('Quit'), 'clicked', self.terminate_program)
        self.toolbar.insert(item_quit, 0)

    def add_study_button_preference_button_other_button(self):
        item = toolitem(D+'sora_icons/m_others.png', _('Others'), 'button_release_event', 
                        self.__show_popupmenu_on_toolbaritem, create_menu_from(load_others_menuitems()))
        self.toolbar.insert(item, 0)
        self.menu_preference = create_menu_from(load_preferences_menuitems())
        default_pane_item = gtk.MenuItem(_('Default pane'))
        default_pane_item.set_submenu(self.create_default_pane_menu())
        self.menu_preference.append(default_pane_item)
        self.menu_preference.show_all()
        item = toolitem(D+'sora_icons/m_preference.png', _('Preferences'), 'button_release_event', 
                        self.__show_popupmenu_on_toolbaritem, self.menu_preference)
        self.toolbar.insert(item, 0)
        item = toolitem(D+'sora_icons/m_study_linux.png', _('Study\nLinux'), 'button_release_event', 
                        self.__show_popupmenu_on_toolbaritem, create_menu_from(load_study_linux_menuitems()))
        self.toolbar.insert(item, 0)

    def add_pane_buttons_in_toolbar(self):
        for key in self.ordered_key:
            pane_loader = self.contents[key]
            icon = pane_loader.pane_class.icon
            text = pane_loader.pane_class.text
            item = toolitem(icon, text, 'clicked', self.activate_pane, key)
            self.toolbar.insert(item, 0)
        
        self.activate_pane(None, Config.get_default_pane())

    def get_item_icon_size(self):
        return min( int(self.last_x / 20), 48)

    def __refresh_toolbar(self):
        icon_size = self.get_item_icon_size()
        for i in range(0, self.toolbar.get_n_items()):
            item = self.toolbar.get_nth_item(i)
            item.refresh(icon_size)

    def __show_popupmenu_on_toolbaritem(self, widget, event, menu):
        if event.type == gtk.gdk.BUTTON_RELEASE and event.button == 1:
            def func(menu):
                (x, y) = self.window.get_position()
                rectangle = widget.get_allocation()
                x += rectangle.x
                y += rectangle.y + rectangle.height + 20
                return (x, y, True)
            menu.popup(None, None, func, event.button, event.time)
            return True
        return False
    
    def activate_pane(self, widget, name):
        assert isinstance(name, str)
        self.current_pane = name
        for child in self.toggle_area.get_children():
            self.toggle_area.remove(child)
        pane_loader = self.contents[name]
        if pane_loader.need_to_load():
            import pango
            label = gtk.Label(_('Please wait a few seconds'))
            label.modify_font(pango.FontDescription('Sans 20'))
            self.toggle_area.add(label)
            self.toggle_area.show_all()
            while gtk.events_pending(): gtk.main_iteration()
            pane = pane_loader.get_pane() # load pane
            for child in self.toggle_area.get_children():
                self.toggle_area.remove(child)
            if hasattr(pane, 'get_preference_menuitems'): # insert preference_menuitems
                for item in pane.get_preference_menuitems():
                    self.menu_preference.append(item)
                self.menu_preference.show_all()
        self.toggle_area.add(pane_loader.get_pane())
        self.toggle_area.show_all()

    def lock(self):
        self.stop_delete_event = True
        self.toolbar.set_sensitive(False)
    
    def unlock(self):
        self.stop_delete_event = False
        self.toolbar.set_sensitive(True)

    def query_whether_exit(self):
        dialog = gtk.MessageDialog(self.window, 
                gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                _('Are you sure to exit?'))
        check_button = gtk.CheckButton(_('Do not ask me again.'))
        check_button.set_active(not Config.get_query_before_exit())
        dialog.vbox.pack_start(check_button)
        dialog.vbox.show_all()
        ret = dialog.run()
        dialog.destroy()
        Config.set_query_before_exit(not check_button.get_active())
        if ret == gtk.RESPONSE_NO:
            return True
        else:
            return False

    def terminate_program(self, *w):
        if Config.get_query_before_exit() and self.query_whether_exit():
            return True
        
        if self.stop_delete_event:
            return True
        
        from support.windowpos import WindowPos
        WindowPos.save(self.window,'main')

        gtk.main_quit()
        sys.exit()

    def register(self, pane_class, content_function = None):
        import gobject
        key = pane_class.__name__
        self.contents[key] = PaneLoader(self, pane_class, content_function)
        self.ordered_key.append(key)

    def __init__(self):
        self.window = None # MainView window
        self.stop_delete_event = False
        self.contents = {}
        self.ordered_key = [] # contains keys in self.contents, in calling order of self.register
        self.menu_preference = None # "Preference" menu
        
        self.toggle_area = gtk.VBox()
        self.toggle_area.set_border_width(5)
        
        vbox = gtk.VBox(False, 0)
        
        self.toolbar = gtk.Toolbar()
        self.toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        self.toolbar.set_style(gtk.TOOLBAR_BOTH)
        vbox.pack_start(self.toolbar, False)
        vbox.pack_start(gtk.HSeparator(), False)
        vbox.pack_start(self.toggle_area, True, True)
        
        self.window = window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Ailurus')
        self.last_x = self.window.get_size()[0]
        def configure_event(window, event, toolbar):
            if self.last_x != self.window.get_size()[0]:
                self.last_x = self.window.get_size()[0]
                self.__refresh_toolbar()
        self.window.connect('configure_event', configure_event, self.toolbar)
        window.connect("delete_event", self.terminate_program)
        window.add(vbox)

        from support.windowpos import WindowPos
        WindowPos.load(window,'main')
        
        from system_setting_pane import SystemSettingPane
        from clean_up_pane import CleanUpPane
        from info_pane import InfoPane
        from install_remove_pane import InstallRemovePane
        from computer_doctor_pane import ComputerDoctorPane
        if UBUNTU or UBUNTU_DERIV:
            from ubuntu.repos_config_pane import ReposConfigPane
        if FEDORA:
            from fedora.repos_edit_pane import FedoraReposEditPane

        self.register(ComputerDoctorPane, load_cure_objs)
        self.register(CleanUpPane)
        if BACKEND:
            from snapshot_pane import SnapshotPane
            self.register(SnapshotPane)
        if UBUNTU or UBUNTU_DERIV:
            self.register(ReposConfigPane)
        if FEDORA:
            self.register(FedoraReposEditPane)
        self.register(InstallRemovePane)
        self.register(SystemSettingPane, load_setting)
        self.register(InfoPane, load_info)
        
        self.add_quit_button()
        self.add_study_button_preference_button_other_button()
        self.add_pane_buttons_in_toolbar()
        self.window.show_all()
        
        if Config.is_long_enough_since_last_check_update():
            Config.set_last_check_update_time_to_now()
            from support.checkupdate import check_update
            import thread
            thread.start_new_thread(check_update, (True, )) # "True" means "silent"

def show_agreement():
    message = ('Ailurus CANNOT install w32codecs/w64codecs, libdvdcss2 or close source software.\n'
        '\n'
        '<span color="red">Please NOTE that <b>downloading and installing w32codecs/w64codecs '
        'and libdvdcss2 violates the Digital Millennium Copyright Act(DMCA) and other laws regarding '
        'anti-piracy/copyright violation in the United States of America</b>.</span>\n'
        '\n'
        'Under NO circumstances, will the Ailurus developers be responsible for your actions which includes, '
        'but not limited to, downloading and installing these codecs or close source software.')
    label = gtk.Label(_('Do you agree?'))
    dialog = gtk.MessageDialog(buttons=gtk.BUTTONS_YES_NO, type=gtk.MESSAGE_WARNING)
    dialog.set_markup(message)
    dialog.set_title(_('Warning'))
    dialog.vbox.pack_start(label, False)
    dialog.vbox.show_all()
    ret = dialog.run()
    dialog.destroy()
    if ret == gtk.RESPONSE_YES:
        Config.set_show_agreement(False)
    if ret != gtk.RESPONSE_YES:
        sys.exit()

if Config.get_show_agreement():
    show_agreement()

with TimeStat(_('start up')):
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    change_task_name()
    set_default_window_icon()
    detect_proxy_env()
    check_home_dir_permission()
    check_required_packages()
    check_dbus_daemon_status()
    
    while gtk.events_pending(): gtk.main_iteration()
    main_view = MainView()

gtk.gdk.threads_init()
gtk.gdk.threads_enter()
gtk.main()
gtk.gdk.threads_leave()
sys.exit()
