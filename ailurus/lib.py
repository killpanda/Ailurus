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

def get_ailurus_path():
    import os
    return os.path.dirname(os.path.abspath(__file__))

try:
    A = get_ailurus_path()
except: # raise exception in python console because __file__ is not defined
    import os
    A = os.path.expanduser('~/workspace/Ailurus/ailurus/')
    assert os.path.exists(A), 'Please put ailurus code in $HOME/workspace/Ailurus/'
D = A + '/icons/'

def row(text, value, icon, tooltip = None): # only used in hardwareinfo.py and osinfo.py
    return (text, value, icon, tooltip)

class I:
    this_is_an_installer = True
    this_is_a_repository = False
    category = 'others'
    detail = ''
    how_to_install = ''
    download_url = ''
    cache_installed = showed_in_toggle = None # boolean
    logo_pixbuf = None # gtk.gdk.Pixbuf
    use_default_icon = None # boolean
    installing_error = [] # list
    def self_check(self):
        'check errors in source code'
    def fill(self):
        'fill self.detail, self.how_to_install'
    def install(self):
        raise NotImplementedError
    def installed(self):
        raise NotImplementedError
    def remove(self):
        raise NotImplementedError
    def add_temp_repository(self):
        'Add repository before installing me'
    def clean_temp_repository(self):
        'Remove repository after installing me'
    def clean_installing_error(self):
        self.installing_error = []
    def has_installing_error(self):
        return bool(self.installing_error)
    def add_installing_error(self, error):
        assert isinstance(error, tuple) and len(error) == 3
        import types
        assert isinstance(error[0], types.TypeType)
        assert isinstance(error[1], types.ObjectType)
        assert isinstance(error[2], types.ObjectType)
        self.installing_error.append(error)
    def print_installing_error(self, stream):
        import traceback
        print >>stream, self.__doc__
        for exc in self.installing_error:
            traceback.print_exception(exc[0], exc[1], exc[2], file=stream)
        print >>stream
    def fail_by_download_error(self):
        for error in self.installing_error:
            if error[0] == CannotDownloadError:
                return True
        return False
    def fail_by_user_cancel(self):
        for error in self.installing_error:
            if error[0] == UserCancelInstallation:
                return True
        return False
    def visible(self):
        return True

class C:
    this_is_a_cure = True
    MUST_FIX, SUGGESTION = range(2)
    type = SUGGESTION
    detail = ''
    def exists(self):
        raise NotImplementedError
    def cure(self):
        raise NotImplementedError
    
class Config:
    import os
    config_dir = os.path.expanduser('~/.config/ailurus/')
    @classmethod
    def check_permission(cls):
        cls.make_config_dir()
        f = open(cls.config_dir + 'this_file_can_be_safely_removed', 'w')
        f.close()
    @classmethod
    def make_config_dir(cls):
        import os
        dir = os.path.expanduser('~/.config/ailurus/')
        if not os.path.exists(dir): # make directory
            os.makedirs(dir)
    @classmethod
    def init(cls):
        assert not hasattr(cls, 'inited')
        cls.inited = True
        # create parser object
        import ConfigParser, os
        cls.parser = ConfigParser.RawConfigParser()
        # read configuration file if it exists
        cls.make_config_dir()
        path = cls.config_dir + 'conf'
        if os.path.exists(path):
            cls.parser.read(path)
    @classmethod
    def save(cls):
        cls.make_config_dir()
        try:
            with open(cls.config_dir + 'conf' , 'w') as f:
                cls.parser.write(f)
        except:
            print_traceback()
    @classmethod
    def set_string(cls, key, value):
        assert isinstance(key, str) and key
        assert isinstance(value, (str,unicode))  and value
        cls.parser.set('DEFAULT', key, value)
        cls.save()
    @classmethod
    def get_string(cls, key):
        assert isinstance(key, str) and key
        return cls.parser.get('DEFAULT', key)
    @classmethod
    def set_int(cls, key, value):
        assert isinstance(key, str) and key
        assert isinstance(value, int), type(value)
        cls.parser.set('DEFAULT', key, value)
        cls.save()
    @classmethod
    def get_int(cls, key):
        assert isinstance(key, str) and key
        value = cls.parser.get('DEFAULT', key)
        return int(value)
    @classmethod
    def set_long(cls, key, value):
        assert isinstance(key, str) and key
        assert isinstance(value, long), type(value)
        cls.parser.set('DEFAULT', key, value)
        cls.save()
    @classmethod
    def get_long(cls, key):
        assert isinstance(key, str) and key
        value = cls.parser.get('DEFAULT', key)
        return long(value)
    @classmethod
    def set_bool(cls, key, value):
        assert isinstance(key, str) and key
        assert isinstance(value, bool)
        cls.parser.set('DEFAULT', key, value)
        cls.save()
    @classmethod
    def get_bool(cls, key):
        assert isinstance(key, str) and key
        value = cls.parser.get('DEFAULT', key)
        value = str(value)
        return value=='True' or value=='true'
    @classmethod
    def get_custom_appobj_counter_value(cls):
        try: return cls.get_int('custom_app_count')
        except: return 0
    @classmethod
    def increase_customapp_counter_value(cls):
        value = cls.get_custom_appobj_counter_value()
        value += 1
        cls.set_int('custom_app_count', value)
    @classmethod
    def set_do_query_before_install(cls, value):
        cls.set_bool('do_query_before_install', value)
    @classmethod
    def get_do_query_before_install(cls):
        try: return cls.get_bool('do_query_before_install')
        except: return True
    @classmethod
    def set_login_window_background(cls, value):
        'just a cache. value may be wrong. cache the gconf value "/desktop/gnome/background/picture_filename" of user "gdm".'
        cls.set_string('login_window_background', value)
    @classmethod
    def get_login_window_background(cls):
        try: return cls.get_string('login_window_background')
        except: return None # please do not return ''. 
    @classmethod
    def set_contact(cls, value):
        cls.set_string('contact', value)
    @classmethod
    def get_contact(cls):
        try:
            return cls.get_string('contact')
        except:
            import os
            return os.environ['USER']
    @classmethod
    def set_last_check_update_time_to_now(cls):
        import time
        value = long(time.time()) # the time as a floating point number expressed in seconds since the epoch, in UTC
        cls.set_long('last_check_update_time', value)
    @classmethod
    def get_last_check_update_time(cls):
        try: return cls.get_long('last_check_update_time')
        except: return 0
    @classmethod
    def is_long_enough_since_last_check_update(cls):
        import time
        last_check_time = cls.get_last_check_update_time()
        now = time.time() # the time as a floating point number expressed in seconds since the epoch, in UTC
        one_day = 3600 * 24
        return now - last_check_time > one_day * 14
    @classmethod
    def set_last_synced_data_version(cls, value):
        cls.set_int('last_synced_data_version', value)
    @classmethod
    def get_last_synced_data_version(cls):
        try: return cls.get_int('last_synced_data_version')
        except: return 0
    @classmethod
    def set_use_proxy(cls, value):
        cls.set_bool('use_proxy', value)
    @classmethod
    def get_use_proxy(cls):
        try: return cls.get_bool('use_proxy')
        except: return False
    @classmethod
    def set_proxy_string_id_in_keyring(cls, value):
        cls.set_long('proxy_string_id_in_keyring', value)
    @classmethod
    def get_proxy_string_id_in_keyring(cls):
        # do not wrap it in try..except
        return cls.get_long('proxy_string_id_in_keyring')
    @classmethod
    def set_query_before_exit(cls, value):
        cls.set_bool('query_before_exit', value)
    @classmethod
    def get_query_before_exit(cls):
        try:       return cls.get_bool('query_before_exit')
        except:    return True
    @classmethod
    def wget_set_timeout(cls, timeout):
        assert isinstance(timeout, int) and timeout>0, timeout
        cls.set_int('wget_timeout', timeout)
    @classmethod
    def wget_get_timeout(cls):
        try:       value = cls.get_int('wget_timeout')
        except: value = 20
        return value
    @classmethod
    def wget_set_triesnum(cls, triesnum):
        assert isinstance(triesnum, int) and triesnum>0, triesnum
        cls.set_int('wget_triesnum', triesnum)
    @classmethod
    def wget_get_triesnum(cls):
        try:       value = cls.get_int('wget_triesnum')
        except: value = 3
        return value
    @classmethod
    def set_default_pane(cls, value):
        cls.set_string('default_pane', value)
    @classmethod
    def get_default_pane(cls):
        try: value = cls.get_string('default_pane')
        except: value = 'SystemSettingPane'
        return value
    @classmethod
    def get_locale(cls):
        import locale
        try:
            value = locale.getdefaultlocale()[0]
            if value: return value # language code and encoding may be None if their values cannot be determined.
            else: return 'en_US'
        except ValueError: # may raise exception: "unknown locale"
            print_traceback()
            return 'en_US'
    @classmethod
    def is_Chinese_locale(cls):
        return cls.get_locale().startswith('zh')
    @classmethod
    def is_Poland_locale(cls):
        return cls.get_locale().startswith('pl')
    @classmethod
    def is_Ubuntu(cls):
        import os
        if not os.path.exists('/etc/lsb-release'): 
            return False
        with open('/etc/lsb-release') as f:
            c = f.read()
        return 'Ubuntu' in c
    @classmethod
    def get_Ubuntu_version(cls):
        '''return 'hardy', 'intrepid', 'jaunty', 'karmic', 'lucid' ...'''
        with open('/etc/lsb-release') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('DISTRIB_CODENAME='):
                return line.split('=')[1].strip()
    @classmethod
    def get_all_Ubuntu_versions(cls):
        return ['hardy', 'intrepid', 'jaunty', 'karmic', 'lucid', 'maverick']
    @classmethod
    def is_Mint(cls):
        import os
        if not os.path.exists('/etc/lsb-release'): return False
        with open('/etc/lsb-release') as f:
            c = f.read()
        return 'LinuxMint' in c
    @classmethod
    def get_Mint_version(cls):
        with open('/etc/lsb-release') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('DISTRIB_RELEASE='):
                a = line.split('=')[1].strip()
        return a
    @classmethod
    def is_YLMF(cls):
        import os
        if not os.path.exists('/etc/lsb-release'): 
            return False
        with open('/etc/lsb-release') as f:
            c = f.read()
        return 'Ylmf_OS' in c
    @classmethod
    def get_YLMF_version(cls):
        '''return 'hardy', 'intrepid', 'jaunty', 'karmic' or 'lucid'.'''
        with open('/etc/lsb-release') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('DISTRIB_CODENAME='):
                return line.split('=')[1].strip()
    @classmethod
    def is_Deepin(cls): # Linux Deepin is based on XUbuntu karmic
        import platform
        return platform.dist()[0] == 'Deepin'
    @classmethod
    def get_Deepin_version(cls):
        'return karmic'
        import platform
        return platform.dist()[2]
    @classmethod
    def is_Fedora(cls):
        import os
        return os.path.exists('/etc/fedora-release')
    @classmethod
    def get_Fedora_version(cls):
        with open('/etc/fedora-release') as f:
            c = f.read()
        return c.split()[2].strip()
    @classmethod
    def is_ArchLinux(cls): # There is no get_arch_version, since ArchLinux has no version.
        import os
        return os.path.exists('/etc/arch-release')
    @classmethod
    def is_Debian(cls):
        import platform
        return platform.dist()[0] == 'debian'
    @classmethod
    def get_Debian_version(cls):
        'return "5.*"'
        import platform
        return platform.dist()[1]
    @classmethod
    def is_GNOME(cls):
        if cls.is_XFCE(): return False
        try:
            get_output('pgrep -u $USER gnome-panel')
            return True
        except:
            return False
    @classmethod
    def is_KDE(cls):
        try:
            get_output('pgrep -u $USER kdeinit')
            return True
        except:
            try:
                get_output('pgrep -u $USER kdeinit4')
                return True
            except: pass
        return False
    @classmethod
    def is_XFCE(cls):
        try:  
            get_output('pgrep -u $USER xfce4-session')
            return True
        except: 
            return False

def set_proxy_string(proxy_string):
    import gnomekeyring
    keyring = gnomekeyring.get_default_keyring_sync()
    id = gnomekeyring.item_create_sync(keyring,
                                       gnomekeyring.ITEM_GENERIC_SECRET,
                                       'ailurus proxy string',
                                       {'appname':'ailurus'},
                                       proxy_string,
                                       True, # update_if_exists
                                      )
    Config.set_proxy_string_id_in_keyring(id)

class UserDeniedError(Exception):
    'User has denied keyring authentication'

def get_proxy_string():
    "Return '', non-empty string or raise exception"
    if hasattr(get_proxy_string, 'denied'): # user has denied access before
        raise UserDeniedError
    
    try:    id = Config.get_proxy_string_id_in_keyring()
    except: return '' # not exist
    
    import gnomekeyring
    keyring = gnomekeyring.get_default_keyring_sync()
    try:
        proxy_string = gnomekeyring.item_get_info_sync(keyring, id).get_secret()
        return proxy_string
    except gnomekeyring.DeniedError: # user denied authentication
        get_proxy_string.denied = True
        raise UserDeniedError

def enable_urllib2_proxy():
    string = get_proxy_string()
    assert string
    import urllib2
    proxy_support = urllib2.ProxyHandler({'http':string}) # FIXME: please support https, ftp, rstp
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

def disable_urllib2_proxy():
    import urllib2
    urllib2.install_opener(None)

def install_locale():
    import gettext
    gettext.translation('ailurus', '/usr/share/locale', fallback=True).install(names=['ngettext'])

def is_legal_license(license):
    return license in [GPL, LGPL, EPL, MPL, BSD, MIT, CDDL, APL, AL] 

def DUAL_LICENSE(A, B):
    assert is_legal_license(A) and is_legal_license(B)
    return _('Dual-licensed under %(A)s and %(B)s') % {'A':A, 'B':B}

def TRI_LICENSE(A, B, C):
    assert is_legal_license(A) and is_legal_license(B) and is_legal_license(C)
    return _('Tri-licensed under %(A)s, %(B)s and %(C)s') % {'A':A, 'B':B, 'C':C}

class ResponseTime:
    map = {}
    changed = False
    @classmethod
    def load(cls):
        import os
        try:
            path = Config.config_dir + 'response_time_3'
            if not os.path.exists(path): return
            with open(path) as f:
                lines = f.readlines()
            for i in range(0, len(lines), 2):
                url = lines[i].strip()
                time = float(lines[i+1].strip())
                cls.map[url] = time
        except IOError:
            print_traceback()
    @classmethod
    def save(cls):
        if not cls.changed: return
        try:
            path = Config.config_dir + 'response_time_3'
            with open(path, 'w') as f:
                for key, value in cls.map.items():
                    print >>f, key
                    print >>f, value
        except IOError:
            print_traceback()
    @classmethod
    def get(cls, url):
        is_string_not_empty(url)
        return cls.map[url]
    @classmethod
    def set(cls, url, value):
        is_string_not_empty(url)
        assert isinstance(value, (int,float)) and value > 0
        cls.map[url] = value
        cls.changed = True

class CommandFailError(Exception):
    'Fail to execute a command'

def run(command, ignore_error=False):
    is_string_not_empty(command)
    if not isinstance(ignore_error,  bool): raise TypeError

    if getattr(run, 'terminal', None):
        assert run.terminal.__class__.__name__ == 'Terminal'
        try:
            run.terminal.run(command)
        except CommandFailError:
            if not ignore_error: raise
    else:
        print '\x1b[1;33m', _('Run command:'), command, '\x1b[m'
        import os, subprocess
        env = None
        if Config.get_use_proxy():
            try:
                proxy_string = get_proxy_string()
                assert proxy_string
            except: pass
            else:
                env = os.environ.copy()
                env.update({'http_proxy':proxy_string,
                            'https_proxy':proxy_string,
                            'ftp_proxy':proxy_string,
                            })
        task = subprocess.Popen(command, env=env, shell=True)
        task.wait()
        if task.returncode and ignore_error == False:
            raise CommandFailError(command, task.returncode)

def packed_env_string():
    import os
    env = dict( os.environ )
    env['PWD'] = os.getcwd()
    return repr(env)

def daemon():
    import dbus
    bus = dbus.SystemBus()
    obj = bus.get_object('cn.ailurus', '/')
    return obj

def get_dbus_daemon_version():
    ret = daemon().get_version(dbus_interface='cn.ailurus.Interface')
    return ret    

def restart_dbus_daemon():
    authenticate()
    daemon().exit(dbus_interface='cn.ailurus.Interface')

def get_authentication_method():
    ret = daemon().get_check_permission_method(dbus_interface='cn.ailurus.Interface')
    ret = int(ret)
    return ret

def authenticate():
    if get_authentication_method() == 0:
        import dbus, os
        bus = dbus.SessionBus()
        policykit = bus.get_object('org.freedesktop.PolicyKit.AuthenticationAgent', '/')
        policykit.ObtainAuthorization('cn.ailurus', dbus.UInt32(0), dbus.UInt32(os.getpid()))

def spawn_as_root(command):
    is_string_not_empty(command)
    
    authenticate()
    daemon().spawn(command, packed_env_string(), dbus_interface='cn.ailurus.Interface')

def drop_priviledge():
    daemon().drop_priviledge(dbus_interface='cn.ailurus.Interface')
    
class AccessDeniedError(Exception):
    'User press cancel button in policykit window'

def run_as_root(cmd, ignore_error=False):
    import dbus
    is_string_not_empty(cmd)
    assert isinstance(ignore_error, bool)
    
    print '\x1b[1;33m', _('Run command:'), cmd, '\x1b[m'
    authenticate()
    try:
        daemon().run(cmd, packed_env_string(), timeout=36000, dbus_interface='cn.ailurus.Interface')
    except dbus.exceptions.DBusException, e:
        if e.get_dbus_name() == 'cn.ailurus.AccessDeniedError': raise AccessDeniedError(*e.args)
        elif e.get_dbus_name() == 'cn.ailurus.CommandFailError':
            if not ignore_error: raise CommandFailError(cmd)
        else: raise

def is_string_not_empty(string):
    if type(string)!=str and type(string)!=unicode: raise TypeError(string)
    if string=='': raise ValueError

def get_output(cmd, ignore_error=False):
    is_string_not_empty(cmd)
    assert isinstance(ignore_error, bool)
    
    import commands
    status, output=commands.getstatusoutput(cmd)
    if status and not ignore_error: raise CommandFailError(cmd, output) # help to fix issue 1092
    return output
    
class TempOwn:
    def __init__(self,path):
        is_string_not_empty(path)
        if path[0]=='-':
            raise ValueError
        import os
        dirname = os.path.dirname(os.path.abspath(path))
        if not os.path.exists(dirname):
            run_as_root('mkdir "%s"'%dirname)
        if not os.path.exists(path):
            run_as_root('touch "%s"'%path)
        run_as_root('chown $USER:$USER %s'%path )
        self.path = path
    def __enter__(self):
        return None
    def __exit__(self, type, value, traceback):
        run_as_root('chown root:root %s'%self.path)

def notify(title, content):
    'Show a notification in the right-upper corner.'
    # title must not be empty. 
    # otherwise, this error happens. notify_notification_update: assertion `summary != NULL && *summary != '\0'' failed
    assert isinstance(title, str) and title
    assert isinstance(content, str)
    try:
        import pynotify
        if not hasattr(notify,'ailurus_notify'):
            notify.ailurus_notify = pynotify.Notification(' ',' ')
        icon = D+'suyun_icons/notify-icon.png'
        if title == notify.ailurus_notify.get_property('summary'):
            notify.ailurus_notify = pynotify.Notification(title, content, icon)
            notify.ailurus_notify.set_hint_string("x-canonical-append", "")
        else:
            notify.ailurus_notify.update(title, content, icon)
               
        notify.ailurus_notify.set_timeout(10000)
        notify.ailurus_notify.show()
    except:
        print_traceback()

def is32():
    import os
    return os.uname()[-1] != 'x86_64'

def file_contain(path, *lines):
    'Return True if the file contains all the lines'
    is_string_not_empty(path)
    if not len(lines): raise ValueError
    for line in lines:
        is_string_not_empty(line)
    import os
    if os.path.exists(path):
        with open(path, 'r') as f:
            contents = f.readlines()
        for line in lines:
            if line[-1]!='\n': line+='\n'
            if not line in contents: return False
        return True
    return False

def file_insert(path, *args):
    'Insert lines into file. The format of args is "position, line, position, line..."'
    is_string_not_empty(path)
    if not len(args): raise ValueError
    for i in range(0, len(args), 2):
        if type(args[i])!=int: raise TypeError
        is_string_not_empty(args[i+1])
    
    import os
    if not os.path.exists(path):
        run('touch %s'%path)
    with open(path, "r") as f:
        contents = f.readlines()
    for i in range(0, len(args), 2):
        line = args[i]
        string = args[i+1]
        if string[-1]!='\n': string+='\n'
        contents.insert(line, string)
    with open(path, "w") as f:
        f.writelines(contents)

def file_append(path, *lines):
    is_string_not_empty(path)
    if not len(lines): raise ValueError
    for line in lines:
        is_string_not_empty(line)
    with open(path, 'a') as f:
        for line in lines:
            if line[-1]!='\n': line+='\n'
            f.write(line)

def file_remove(path, *lines):
    is_string_not_empty(path)
    if not len(lines): raise ValueError
    for line in lines:
        is_string_not_empty(line)
    with open(path, "r") as f:
        contents = f.readlines()
    for line in lines:
        if line[-1]!='\n': line+='\n'
        try: 
            contents.remove(line)
        except ValueError: pass
    with open(path, "w") as f:
        f.writelines(contents)

def free_space(path):
    is_string_not_empty(path)
    assert path[0]=='/'
    import os, statvfs
    e = os.statvfs(path)
    return e[statvfs.F_BAVAIL] * e[statvfs.F_BSIZE]

def own_by_user(*paths):
    if not len(paths): raise ValueError
    for path in paths:
        is_string_not_empty(path)
        if path[0]=='-': raise ValueError
    for path in paths:
        import os
        if os.stat(path).st_uid != os.getuid():
            run_as_root('chown $USER:$USER "%s"'%path)

def is_pkg_list(packages):
    if not len(packages): raise ValueError
    for package in packages:
        is_string_not_empty(package)
        if package[0]=='-': raise ValueError
        if ' ' in package: raise ValueError

def run_as_root_in_terminal(command, ignore_error=False):
    import dbus
    is_string_not_empty(command)
    print '\x1b[1;33m', _('Run command:'), command, '\x1b[m'

    string = 'python "%s/support/term.py" %s' % (A, command)

    authenticate()
    try:
        daemon().run(string, packed_env_string(), timeout=36000, dbus_interface='cn.ailurus.Interface')
    except dbus.exceptions.DBusException, e:
        if e.get_dbus_name() == 'cn.ailurus.AccessDeniedError': raise AccessDeniedError(*e.args)
        elif e.get_dbus_name() == 'cn.ailurus.CommandFailError':
            if not ignore_error:
                if os.path.exists('/tmp/ailurus_subprocess_dump'): 
                    dump = open('/tmp/ailurus_subprocess_dump').read()
                    open('/tmp/ailurus_subprocess_dump', 'w').write('')
                else: dump = None
                
                if dump: raise CommandFailError(command, dump)
                else: raise CommandFailError(command)
        else: raise

class RPM:
    fresh_cache = False
    __set1 = set() # __set1 consists of all installed software
    __set2 = set() # __set2 = __set1 + all available software
    @classmethod
    def cache_changed(cls):
        cls.fresh_cache = False
    @classmethod
    def refresh_cache(cls):
        if cls.fresh_cache: return
        cls.fresh_cache = True
        cls.__set1 = set()
        cls.__set2 = set()
        import subprocess, os

        with TimeStat(_('scan installed packages')):
            path = A+'/support/dump_rpm_installed.py'
            task = subprocess.Popen(['python', path],
                stdout=subprocess.PIPE,
                )
            for line in task.stdout:
                cls.__set1.add(line.strip())
            task.wait()
        
        with TimeStat(_('scan available packages')):
            path = A+'/support/dump_rpm_existing_new.py'
            task = subprocess.Popen(['python', path],
                stdout=subprocess.PIPE,
                )
            for line in task.stdout:
                cls.__set2.add(line.strip())
            task.wait()
    @classmethod
    def get_installed_pkgs_set(cls):
        cls.refresh_cache()
        return set(cls.__set1)
    @classmethod
    def get_existing_pkgs_set(cls):
        cls.refresh_cache()
        return set(cls.__set2)
    @classmethod
    def exist(cls, package_name):
        cls.refresh_cache()
        return package_name in cls.__set1 or package_name in cls.__set2
    @classmethod
    def installed(cls, package_name):
        is_pkg_list([package_name])
        cls.refresh_cache()
        return package_name in cls.__set1
    @classmethod
    def install(cls, *package):
        cls.cache_changed()
        run_as_root_in_terminal('yum install %s -y' % ' '.join(package))
    @classmethod
    def install_local(cls, path):
        assert isinstance(path, str)
        import os
        assert os.path.exists(path)
        cls.cache_changed()
        run_as_root_in_terminal('yum localinstall "%s" --nogpgcheck -y' % path)
    @classmethod
    def remove(cls, *package):
        cls.cache_changed()
        run_as_root_in_terminal('yum remove %s -y' % ' '.join(package))
    @classmethod
    def import_key(cls, path):
        assert isinstance(path, str)
        run_as_root_in_terminal('rpm --import %s' % path)

class APTSourceSyntaxError(Exception):
    pass

class APT:
    fresh_cache = False
    apt_get_update_is_called = False
    apt_cache = None # instance of apt.cache.Cache
    @classmethod
    def cache_changed(cls):
        cls.fresh_cache = False
    @classmethod
    def get_pkg_summary(cls, name):
        assert isinstance(name, str) and name
        cls.refresh_cache()
        return cls.apt_cache[name].summary
    @classmethod
    def has_broken_dependency(cls):
        cls.refresh_cache()
        try:
            return bool(cls.apt_cache.broken_count)
        except AttributeError: # ubuntu hardy
            return False # not a good solution
    @classmethod
    def refresh_cache(cls):
        if cls.fresh_cache: return
        with TimeStat(_('scan packages')):
            import apt
            try:
                cls.apt_cache = apt.cache.Cache()
                assert cls.apt_cache != None # TODO: how to cope with this error?
            except SystemError, e: # syntax error in source config
                raise APTSourceSyntaxError(*e.args)
            else:
                cls.fresh_cache = True
    @classmethod
    def get_installed_pkgs_set(cls):
        cls.refresh_cache()
        ret = set()
        for pkg in cls.apt_cache:
            if pkg.isInstalled:
                ret.add(pkg.name)
        return ret
    @classmethod
    def get_existing_pkgs_set(cls):
        cls.refresh_cache()
        ret = set()
        for pkg in cls.apt_cache:
            ret.add(pkg.name)
        return ret
    @classmethod
    def get_autoremovable_pkgs(cls):
        cls.refresh_cache()
        ret = []
        for pkg in cls.apt_cache:
            if hasattr(pkg, 'is_auto_removable'): auto_removable = pkg.is_auto_removable
            elif hasattr(pkg, 'isAutoRemovable'): auto_removable = pkg.isAutoRemovable # deprecated
            elif pkg.isInstalled and pkg._depcache.IsGarbage(pkg._pkg): auto_removable = True
            else: auto_removable = False
            
            if auto_removable:
                if hasattr(pkg, 'versions'): # recommended
                    version = pkg.versions[0]
                    installed_size = version.installed_size
                    summary = version.summary
                else: # deprecated
                    installed_size = pkg.installedSize
                    summary = pkg.summary
                ret.append([pkg.name, long(installed_size), summary.replace('\n', ' ')])
        return ret
    @classmethod
    def installed(cls, package_name):
        cls.refresh_cache()
        if not package_name in cls.apt_cache:
            return False
        p = cls.apt_cache[package_name]
        if hasattr(p, 'is_installed'):
            return p.is_installed # recommended attribute 
        else:
            return p.isInstalled # deprecated attribute
    @classmethod
    def exist(cls, package_name):
        cls.refresh_cache()
        return package_name in cls.apt_cache
    @classmethod
    def install(cls, *packages):
        import dbus
        is_pkg_list(packages)
        cls.apt_get_update()
        cls.cache_changed()
        run_as_root_in_terminal('apt-get install %s' % ' '.join(packages))
#        print '\x1b[1;32m', _('Installing packages:'), ' '.join(packages), '\x1b[m'
#        try:
#            daemon().apt_command('install', ','.join(packages),
#                                 packed_env_string(), timeout=3600, dbus_interface='cn.ailurus.Interface')
#        except dbus.exceptions.DBusException, e:
#            if e.get_dbus_name() == 'cn.ailurus.CannotDownloadError':
#                raise CannotDownloadError(*packages)
    @classmethod
    def remove(cls, *packages):
        is_pkg_list(packages)
        cls.cache_changed()
        run_as_root_in_terminal('apt-get remove %s' % ' '.join(packages))
#        print '\x1b[1;31m', _('Removing packages:'), ' '.join(packages), '\x1b[m'
#        daemon().apt_command('remove', ','.join(packages),
#                             packed_env_string(), timeout=3600, dbus_interface='cn.ailurus.Interface')
    @classmethod
    def neet_to_run_apt_get_update(cls):
        cls.apt_get_update_is_called = False
    @classmethod
    def apt_get_update(cls):
        if cls.apt_get_update_is_called == False:
            run_as_root_in_terminal('apt-get update', ignore_error = True)
#            daemon().apt_command('update', '', packed_env_string(), timeout=3600, dbus_interface='cn.ailurus.Interface')
            cls.apt_get_update_is_called = True
            cls.cache_changed()
    @classmethod
    def install_local(cls, *packages):
        cls.cache_changed()
        for package in packages:
            run_as_root('gdebi-gtk "%s"' % package)
#            run_as_root_in_terminal('dpkg -i "%s"' % package)
#            daemon().apt_command('install_local', package,
#                                 packed_env_string(), timeout=3600, dbus_interface='cn.ailurus.Interface')
    @classmethod
    def is_cache_lockable(cls):
        import dbus
        try:
            daemon().is_apt_cache_lockable(dbus_interface='cn.ailurus.Interface')
        except dbus.exceptions.DBusException, e:
            if e.get_dbus_name() == 'cn.ailurus.CannotLockAptCacheError':
                raise CannotLockAptCacheError(e.get_dbus_message())

class CannotLockAptCacheError(Exception):
    'Cannot lock apt cache'

class PACMAN:
    fresh_cache = False
    pacman_sync_called = False
    __pkgs = set()
    __allpkgs = set()
    @classmethod
    def cache_changed(cls):
        cls.fresh_cache = False
    @classmethod
    def refresh_cache(cls):
        if cls.fresh_cache: return
        cls.fresh_cache = True
        cls.__pkgs = set()
        cls.__allpkgs = set()
        with TimeStat(_('scan installed packages')):
            import subprocess, os
            task = subprocess.Popen(['pacman', '-Q'],
                stdout=subprocess.PIPE,
                )
            for line in task.stdout:
                cls.__pkgs.add(line.split()[0])
            task.wait()
        
        with TimeStat(_('scan available packages')):
            task = subprocess.Popen(['pacman', '-Sl'],
                stdout=subprocess.PIPE,
                )
            for line in task.stdout:
                cls.__allpkgs.add(line.split()[1])
            task.wait()
    @classmethod
    def get_installed_pkgs_set(cls):
        cls.refresh_cache()
        return set(cls.__pkgs)
    @classmethod
    def get_existing_pkgs_set(cls):
        cls.refresh_cache()
        return set(cls.__allpkgs)
    @classmethod
    def installed(cls, package_name):
        cls.refresh_cache()
        return package_name in cls.__pkgs
    @classmethod
    def exist(cls, package_name):
        cls.refresh_cache()
        return package_name in cls.__pkgs or package_name in cls.__allpkgs
    @classmethod
    def install(cls, *packages):
        is_pkg_list(packages)
        if not cls.pacman_sync_called:
            cls.pacman_sync()
        cls.cache_changed()
        run_as_root_in_terminal('pacman -S %s' % ' '.join(packages))
    @classmethod
    def install_local(cls, path):
        assert isinstance(path, str)
        import os
        assert os.path.exists(path)
        cls.cache_changed()
        run_as_root_in_terminal('pacman -U "%s"' % path)
    @classmethod
    def remove(cls, *packages):
        is_pkg_list(packages)
        packages = [p for p in packages if PACMAN.installed(p)]
        cls.cache_changed()
        run_as_root_in_terminal('pacman -R %s' % ' '.join(packages))
    @classmethod
    def pacman_sync(cls):
        print '\x1b[1;36m', _('Run "pacman -Sy". Please wait for a few minutes.'), '\x1b[m'
        run_as_root_in_terminal('pacman -Sy')
        cls.pacman_sync_called = True

def get_response_time(url):
    is_string_not_empty(url)

    import urllib2
    import time
    import sys
    begin = time.time()
    if sys.version_info[:2]>(2,5): # for python 2.6+
        urllib2.urlopen(url, timeout=3)
    else: # for python 2.5
        urllib2.urlopen(url) # FIXME: no timeout!
    end = time.time()
    return (end - begin) * 1000 # in milliseconds

def derive_size(size):
    if not ( isinstance(size, int) or isinstance(size, long) ): raise TypeError
    if not size>=0: raise ValueError
    _1G = 1e9
    _1M = 1e6
    _1K = 1e3
    if size>=_1G:
        return _('%.1f GB') % ( size/_1G )
    if size>=_1M:
        return _('%.1f MB') % ( size/_1M )
    if size>=_1K:
        return _('%.1f KB') % ( size/_1K )
    return _('%s bytes') % int(size)

def derive_time(time):
    if not isinstance(time, int): raise TypeError
    if not time>=0: raise ValueError
    _1h = 3600.
    _1m = 60.
    if time >= _1h:
        return _('%.1f hours') % ( time/_1h )
    if time >= _1m:
        return _('%.1f minutes') % ( time/_1m )
    return _('%d seconds') % time

class KillWhenExit:
    task_list = []
    @classmethod
    def add(cls, task):
        import subprocess
        if not isinstance(task, (str, unicode, subprocess.Popen)): raise TypeError
        if isinstance(task, (str, unicode)):
            assert task!=''
            print '\x1b[1;33m', _('Run command:'), task, '\x1b[m' 
            task=subprocess.Popen(task, shell=True)
        cls.task_list.append(task)
    @classmethod
    def kill_all(cls):
        for task in cls.task_list:
            try:
                import os, signal
                os.kill(task.pid, signal.SIGTERM)
            except:
                print_traceback()
        cls.task_list = []

class CannotDownloadError(Exception):
    pass

class UserCancelInstallation(Exception):
    pass

def download(url, filename):
    import os
    is_string_not_empty(url)
    assert url[0]!='-'
    is_string_not_empty(filename)
    assert filename[0]!='-'
    timeout = Config.wget_get_timeout()
    tries = Config.wget_get_triesnum()
    try:
        run("wget --timeout=%(timeout)s --tries=%(tries)s '%(url)s' -O '%(filename)s'"
            %{'timeout':timeout, 'tries':tries, 'url':url, 'filename':filename} )
    except:
        if os.path.exists(filename): os.unlink(filename)
        raise CannotDownloadError(url)
    
def reset_dir():
    import os, sys
    os.chdir(A)

class APTSource2:
    re_pattern_server = None
    re_pattern_url = None
    @classmethod
    def all_conf_files(cls):
        import glob, os
        ret = glob.glob('/etc/apt/sources.list.d/*.list')
        if os.path.exists('/etc/apt/sources.list'):
            ret.append('/etc/apt/sources.list')
        return ret
    @classmethod
    def iter_all_lines(cls):
        for file in cls.all_conf_files():
            f = open(file)
            for line in f:
                if not line.endswith('\n'): line += '\n'
                yield line
            f.close()
    @classmethod
    def all_lines(cls):
        return [line for line in cls.iter_all_lines()]
    @classmethod
    def all_lines_contain(cls, snip):
        snip = cls.remove_comment(snip)
        for line in cls.iter_all_lines():
            if snip in line: return True
        return False
    @classmethod
    def all_lines_contain_all_of(cls, many_snips):
        for snip in many_snips:
            if not cls.all_lines_contain(snip): return False
        return True
    @classmethod
    def add_lines_to_file(cls, lines, file_path = '/etc/apt/sources.list'):
        assert isinstance(lines, list)
        assert isinstance(file_path, str)
        
        with TempOwn(file_path):
            with open(file_path) as f:
                contents = f.readlines()
            if len(contents) and not contents[-1].endswith('\n'):
                contents.append('\n')
            contents.extend(lines)
            with open(file_path, 'w') as f:
                f.writelines(contents)
    @classmethod
    def remove_snips_from(cls, snips, file_path):
        assert isinstance(snips, list)
        assert isinstance(file_path, str)
        
        with open(file_path) as f:
            contents = f.readlines()
        changed = False
        for i, line in enumerate(contents):
            line = cls.remove_comment(line)
            for snip in snips:
                snip = cls.remove_comment(snip)
                if snip in cls.remove_comment(line):
                    contents[i] = ''
                    changed = True
                    break
        if changed:
            with TempOwn(file_path):
                with open(file_path, 'w') as f:
                    f.writelines(contents)
    @classmethod
    def remove_snips_from_all_files(cls, snips):
        assert isinstance(snips, list)
        for file_path in cls.all_conf_files():
            cls.remove_snips_from(snips, file_path)
    @classmethod
    def remove_comment(cls, line):
        return line.split('#', 1)[0].strip()
    @classmethod
    def is_official_line(cls, line):
        line = cls.remove_comment(line)
        for snip in ['-backports', '-proposed', '-security', '-updates']:
            snip = VERSION + snip
            if snip in line: return True
        return False
    @classmethod
    def get_server_from_line(cls, line):
        line = cls.remove_comment(line)
        import re
        if cls.re_pattern_server is None:
            cls.re_pattern_server = re.compile(r'^deb(-src)? [a-z]+://([^/]+)/.*$')
        match = cls.re_pattern_server.match(line)
        if match: return match.group(2)
        else:     return None
    @classmethod
    def get_url_from_line(cls, line):
        line = cls.remove_comment(line)
        import re
        if cls.re_pattern_url is None:
            cls.re_pattern_url = re.compile(r'^deb(-src)? (\S+) .*$')
        match = cls.re_pattern_url.match(line)
        if match: return match.group(2)
        else:     return None
    @classmethod
    def official_servers(cls):
        ret = set()
        for line in cls.iter_all_lines():
            if cls.is_official_line(line):
                server = cls.get_server_from_line(line)
                ret.add(server)
        return ret
    @classmethod
    def official_urls(cls):
        ret = set()
        for line in cls.iter_all_lines():
            if cls.is_official_line(line):
                url = cls.get_url_from_line(line)
                ret.add(url)
        return ret
    @classmethod
    def third_party_urls(cls):
        offi_urls = cls.official_urls()
        ret = set()
        for line in cls.iter_all_lines():
            url = cls.get_url_from_line(line)
            if url and url not in offi_urls: ret.add(url)
        return ret
    @classmethod
    def all_urls(cls):
        ret = set()
        for line in cls.iter_all_lines():
            url = cls.get_url_from_line(line)
            if url: ret.add(url)
        return ret
    @classmethod
    def this_line_contain(cls, line, snip):
        return snip in cls.remove_comment(line)
    @classmethod
    def this_line_contain_any_of(cls, line, snip_set):
        for snip in snip_set:
            if cls.this_line_contain(line, snip):
                return True
        return False
    @classmethod
    def remove_official_servers(cls):
        offi_servers = cls.official_servers()
        for file in cls.all_conf_files():
            with open(file) as f:
                contents = f.readlines()
            changed = False
            for i, line in enumerate(contents):
                if cls.this_line_contain_any_of(line, offi_servers):
                    contents[i] = ''
                    changed = True
            if changed:
                with TempOwn(file):
                    with open(file, 'w') as f:
                        f.writelines(contents)
    @classmethod
    def add_official_url(cls, url):
        with TempOwn('/etc/apt/sources.list'):
            with open('/etc/apt/sources.list') as f:
                contents = f.readlines()
            if len(contents) and not contents[-1].endswith('\n'):
                contents.append('\n')
            contents.append('deb %(url)s %(version)s main restricted universe multiverse\n'
                            'deb %(url)s %(version)s-backports restricted universe multiverse\n'
                            'deb %(url)s %(version)s-proposed main restricted universe multiverse\n'
                            'deb %(url)s %(version)s-security main restricted universe multiverse\n'
                            'deb %(url)s %(version)s-updates main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s-backports main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s-proposed main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s-security main restricted universe multiverse\n'
                            'deb-src %(url)s %(version)s-updates main restricted universe multiverse\n'
                            % {'url':url, 'version':VERSION})
            with open('/etc/apt/sources.list', 'w') as f:
                f.writelines(contents)

import threading
class PingThread(threading.Thread):
    def __init__(self, url, server, result):
        is_string_not_empty(url)
        is_string_not_empty(server)
        assert isinstance(result, list)
        
        threading.Thread.__init__(self)
        self.url = url
        self.server = server
        self.result = result
        import time
        self.start_time = time.time()
    def elapsed_time(self):
        import time
        return time.time() - self.start_time
    def run(self):
        try:
            time = get_response_time(self.url)
            self.result.append([self.server, time])
        except:
            self.result.append([self.server, 'unreachable'])

def open_web_page(page):
    is_string_not_empty(page)
    notify( _('Opening web page'), page)
    KillWhenExit.add('xdg-open "%s"'%page)

def url_button(url, text=None): # put here because of open_web_page :(
    if text == None: text = url
    import gtk, pango
    def func(w, url): open_web_page(url)
    def enter(w, e): 
        try: w.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        except AttributeError: pass
    def leave(w, e): 
        try: w.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
        except AttributeError: pass
    label = gtk.Label()
    label.set_markup("<span color='blue'><u>%s</u></span>" % text)
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

def report_bug(*w):
    page = 'http://code.google.com/p/ailurus/issues/entry'
    notify( _('Opening web page'), page)
    KillWhenExit.add('xdg-open %s'%page)

import os
class firefox:
    support = False # do not use this class if support is False
    preference_dir = None # form: $HOME/.mozilla/firefox/5y7bqw54.default/
    extensions_dir = None # form: preference_dir + 'extensions/'
    prefs_js_path = None # form: preference_dir + 'prefs.js'
    pattern1 = None # regexp
    pattern2 = None # regexp
    prefs_js_line_pattern = None
    key2value = {} # key is native python constant. value is native python constant.
    key2line = {} # key is native python constant. line is the line in prefs.js
    @classmethod
    def init(cls):
        'may raise exception'
        ini_file = os.path.expanduser('~/.mozilla/firefox/profiles.ini')
        if not os.path.exists(ini_file):
            print '[x] Firefox profiles.ini missing'
            return
        with open(ini_file) as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line == 'Name=default\n': break
        else:
            raise Exception('"Name=default" not found')
        lines = lines[i+1:]
        for line in lines:
            if line.startswith('Path='):
                dir_name = line.split('=', 1)[1].strip()
                break
        else:
            raise Exception('"Path=..." not found')
        cls.preference_dir = os.path.expanduser('~/.mozilla/firefox/') + dir_name + '/'
        assert os.path.exists(cls.preference_dir), cls.preference_dir
        cls.extensions_dir = cls.preference_dir + 'extensions/'
        if not os.path.exists(cls.extensions_dir): os.mkdir(cls.extensions_dir)
        cls.prefs_js_path = cls.preference_dir + 'prefs.js'
        if not os.path.exists(cls.prefs_js_path): # touch file
            with open(cls.prefs_js_path, 'w') as f: pass
        import re
        cls.pattern1 = re.compile('em:name="(.+)"')
        cls.pattern2 = re.compile('<em:name>(.+)</em:name>')
        cls.prefs_js_line_pattern = re.compile(r'''^user_pref\( # begin
            (['"][^'"]+['"]) # key
            ,\s
            (.+) # value
            \); # end ''', re.VERBOSE)
        cls.load_user_prefs()
        cls.support = True
    @classmethod
    def is_extension_archive(cls, file_path):
        assert isinstance(file_path, str) and file_path
        assert file_path.endswith('.xpi') or file_path.endswith('.jar')
    @classmethod
    def install_extension_archive(cls, file_path):
        cls.is_extension_archive(file_path)
        run('cp "%s" "%s"' % (file_path, cls.extensions_dir))
    @classmethod
    def extension_archive_exists(cls, file_path):
        cls.is_extension_archive(file_path)
        return os.path.exists(cls.extensions_dir + file_path)
    @classmethod
    def remove_extension_archive(cls, file_path):
        cls.is_extension_archive(file_path)
        print '\x1b[1;33m', _('Run command:'), 'rm -f %s%s' % (cls.extensions_dir, file_path), '\x1b[m'
        os.unlink(cls.extensions_dir + file_path)
    @classmethod
    def extension_is_installed(cls, extension_name):
        assert isinstance(extension_name, (str, unicode)) and extension_name
        import glob
        dirs = glob.glob(cls.extensions_dir + '*')
        ret = []
        for dir in dirs:
            if extension_name == cls.get_extension_name_in(dir):
                return True
        return False
    @classmethod
    def all_installed_extensions(cls):
        import glob
        dirs = glob.glob(cls.extensions_dir + '*')
        ret = []
        for dir in dirs:
            ret.append(cls.get_extension_name_in(dir))
        return ret
    @classmethod
    def get_extension_name_in(cls, dir):
        assert isinstance(dir, str) and dir
        rdf_file = '%s/install.rdf' % dir
        if not os.path.exists(rdf_file): return None
        with open(rdf_file) as f:
            content = f.read()
        return cls.guess_name_from_content_method1(content) or cls.guess_name_from_content_method2(content)  
    @classmethod
    def guess_name_from_content_method1(cls, content):
        try:    return cls.pattern1.search(content).group(1)
        except: return None
    @classmethod
    def guess_name_from_content_method2(cls, content):
        try:    return cls.pattern2.search(content).group(1)
        except: return None
    @classmethod
    def all_user_pref_lines(cls, content):
        assert isinstance(content, (str, unicode))
        lines = content.splitlines()
        ret = []
        for line in lines:
            if line.startswith('user_pref(') and line.endswith(');'):
                ret.append(line)
        return ret
    @classmethod
    def get_key_value_from(cls, user_pref_line): # may raise exception
        'return (key, value). both of them are native python constant.'
        assert isinstance(user_pref_line, (str, unicode))
        match = cls.prefs_js_line_pattern.match(user_pref_line)
        assert match, user_pref_line
        key = match.group(1)
        key = eval(key)
        value = match.group(2)
        true = True # javascript boolean
        false = False # javascript boolean
        value = eval(value)
        return key, value
    @classmethod
    def load_user_prefs(cls):
        cls.key2value.clear()
        with open(cls.prefs_js_path) as f:
            content = f.read()
        lines = cls.all_user_pref_lines(content)
        for line in lines:
            try:
                key, value = cls.get_key_value_from(line)
                cls.key2value[key] = value
                cls.key2line[key] = line
            except:
                print_traceback()
    @classmethod
    def get_pref(cls, key):
        'key should be native python string. return native python constant'
        assert isinstance(key, (str, unicode))
        return cls.key2value[key]
    @classmethod
    def set_pref(cls, key, value):
        'value should be native python variable'
        cls.key2value[key] = value
        repr_key = '"%s"' % key
        repr_value = repr(value)
        if value == True: repr_value = 'true'
        elif value == False: repr_value = 'false'
        cls.key2line[key] = 'user_pref(%s, %s);' % (repr_key, repr_value)
    @classmethod
    def remove_pref(cls, key):
        try: del cls.key2value[key]
        except KeyError: pass
    @classmethod
    def save_user_prefs(cls):
        keys = cls.key2value.keys()
        keys.sort()
        with open(cls.prefs_js_path, 'w') as f:
            for key in keys:
                line = cls.key2line[key]
                print >>f, line

def delay_notify_firefox_restart(show_notify=False):
    assert isinstance(show_notify, bool)
    if not show_notify:
        delay_notify_firefox_restart.should_show = True
    else:
        if getattr(delay_notify_firefox_restart, 'should_show', False):
            delay_notify_firefox_restart.should_show = False
            try:
                string = get_output('ps -a -u $USER | grep firefox', True)
                if string:
                    notify(_('Please restart Firefox'), _('Please restart Firefox to complete installation.'))
                else:
                    KillWhenExit.add('firefox')
            except:
                print_traceback()

def sha1(path):
    is_string_not_empty(path)
    import os
    assert os.path.exists(path)
    import hashlib
    obj = hashlib.sha1()
    f = open(path)
    while True:
        block = f.read(4096)
        if len(block)==0: break
        obj.update(block)
    f.close()
    return obj.hexdigest()

class R:
    pingtime_cache = {}
    @classmethod
    def get_speed(cls, url):
        assert url and isinstance(url, str)
        import re
        match = re.match('^\w+://([^/]+)/.+$', url)
        assert match, url
        try:
            server = match.group(1)
            if server in cls.pingtime_cache:
                Time = cls.pingtime_cache[server]
            else:
                Time = get_response_time(url)
                print _('Response time of server %(name)s is %(time).1f ms.') % {'name':server, 'time':Time}
        except:
            print _('Server %s does not respond.')%server
            Time = 10000.0
        finally:
            cls.pingtime_cache[server] = Time
            return Time
    @staticmethod
    def compare(u1, u2):
        s1 = R.get_speed(u1)
        s2 = R.get_speed(u2)
        return cmp(s1, s2)
    def sort(self):
        if self.sorted: return
        self.sorted = True
        
        if isinstance(self.url, str): 
            self.sorted_url = [self.url]
        elif isinstance(self.url, list):
            if len(self.url)>1:
                self.url.sort(R.compare)
            self.sorted_url = self.url
        else:
            raise Exception
    def delete_duplicate(self, List):
        ret = []
        servers = set()
        for url in List:
            import re
            match = re.search('://([^/]+)/', url)
            server = match.group(1)
            if not server in servers:
                ret.append(url)
                servers.add(server)
        return ret
    def __init__(self, url_list, size=None, hash=None, filename=None):
        #check url
        assert url_list
        assert isinstance(url_list, (str,list))
        if isinstance(url_list, str): 
            url_list = [ url_list ]
        for e in url_list:
            assert isinstance(e, str), e
            assert e.startswith('http://') or e.startswith('https://') or e.startswith('ftp://')
        self.url = self.delete_duplicate(url_list)

        #check size
        if size!=None:
            assert size>0
            assert isinstance(size, int) or isinstance(size, long), size
        self.size = size
        #check hash
        if hash:
            assert isinstance(hash, str), hash
            assert len(hash)==40, hash
        self.hash = hash

        if filename:
            self.filename = filename
        else:
            if isinstance(url_list, str): u = url_list
            elif isinstance(url_list, list): u = url_list[0]
            import re
            self.filename = re.match('^.+/(.+)$', u).group(1)
            
        self.sorted = False
    def can_download(self):
        import urllib2
        for url in self.url:
            try:
                print url
                f = urllib2.urlopen(url)
                return True
            except:
                pass
        return False
    def check(self, path):
        if self.size:
            import os
            filesize=os.path.getsize(path)
            if filesize!=self.size: 
                raise CommandFailError('File is broken. Expected file length is %s, but real length is %s.'%(self.size, filesize) )
        if self.hash:
            print _('Checking file integrity ...'),
            filehash = sha1(path)
            if filehash!=self.hash: 
                raise CommandFailError('File is broken. Expected hash is %s, but real hash is %s.'%(self.hash, filehash) )
            print _('Good.')
    def download(self):
        self.sort()
        dest = '/tmp/'+self.filename
        import os, sys
        assert isinstance(self.sorted_url, list)
        for i, url in enumerate(self.sorted_url):
            print '\x1b[1;36m', _('Using mirror %(i)s. There are a total of %(total)s mirrors.') % {'i' : i+1, 'total' : len(self.sorted_url)}, '\x1b[m'
            assert isinstance(url, str)
            try:
                download(url, dest)
                self.check(dest)
                return dest
            except:
                print_traceback()
        
        raise CannotDownloadError(self.url)

class ETCEnvironment:
    def __init__(self):
        self.keys = []
        self.values = {}
        f = open('/etc/environment')
        for line in f:
            items = line.split('=',1)
            if len(items)<2: continue
            key = items[0].strip()
            if not key in self.keys:
                self.keys.append(key)
            value = items[1].strip()
            if value[0]==value[-1]=='\'' or value[0]==value[-1]=='\"': value = value[1:-1]
            self.values[key] = value.split(':')
    def add(self, key, *values):
        assert key and isinstance(key, str),    key
        
        values = list(values)
        assert values
        for v in values:
            assert v and isinstance(v, str),    v
            assert not ':' in v,     v
        
        if not key in self.keys:
            self.keys.append(key)
            self.values[key] = values
        else:
            self.values[key] = values+self.values[key]
    def remove(self, key, *values):
        assert key and isinstance(key, str),    key
        for v in values:
            assert v and isinstance(v, str),    v
            assert not ':' in v,     v

        if not key in self.keys: return
        if not values: 
            # delete it directly
            try:    self.keys.remove(key)
            except: pass
            try:    del self.values[key]
            except: pass
        else:
            List = self.values[key]
            self.values[key] = [e for e in List if not e in values]
    def save(self):
        with TempOwn('/etc/environment'):
            f = open('/etc/environment', 'w')
            for key in self.keys:
                if not self.values[key]: continue
                f.write(key)
                f.write('=')
                f.write('\"')
                f.write(':'.join(self.values[key]))
                f.write('\"')
                f.write('\n')

class Chdir:
    def __init__(self,path):
        is_string_not_empty(path)
        if path[0]=='-':
            raise ValueError
        import os
        if not os.path.exists(path):
            raise ValueError
        
        self.oldpath = os.getcwd()
        os.chdir(path)
    def __enter__(self):
        return None
    def __exit__(self, type, value, traceback):
        import os
        os.chdir(self.oldpath)

def create_file(path, content):
    with TempOwn(path):
        with open(path, 'w') as f:
            f.write(content)

def print_traceback():
    import sys, traceback
    traceback.print_exc(file = sys.stderr)

def window_manager_name():
    """Returns window manager name"""
    # Thanks to Whise (Helder Fraga), we have this elegant function!
    # This function is from Screenlets/sensors.py
    # GPLv3
    import gtk
    root = gtk.gdk.get_default_root_window()
    try:
        ident = root.property_get("_NET_SUPPORTING_WM_CHECK", "WINDOW")[2]
        _WM_NAME_WIN = gtk.gdk.window_foreign_new(long(ident[0]))
    except TypeError, exc:
        _WM_NAME_WIN = ""

    name = ""
    win = _WM_NAME_WIN
    if (win != None):
        try:
            name = win.property_get("_NET_WM_NAME")[2]
        except TypeError, exc:
            pass
        except AttributeError: #'str' object has no attribute 'property_get'
            pass
    return name

class FedoraReposSection:
    def _set(self, lines):
        self.name = lines[0][1:-1]

        self.dict = {}
        for l in lines[1:]:
            try:
                k, v = l.split('=', 1)
            except ValueError: # no '='
                self.dict[l] = ''
            else:
                self.dict[k] = v
        
    def __init__(self, lines, parent):
        assert isinstance(parent, FedoraReposFile)
        self.parent = parent # for delete section
        assert isinstance(lines, list) and lines[0].startswith('[')
        for l in lines: assert not l.endswith('\n')
        self._set(lines)
    
    def set_new_content_as(self, new_content):
        assert isinstance(new_content, str)
        lines = new_content.split('\n')
        lines = [l for l in lines if l]
        self._set(lines)
    
    def to_string(self):
        import StringIO
        stream = StringIO.StringIO()
        print >>stream, '[%s]' % self.name
        for k, v in self.dict.items():
            print >>stream, '%s=%s' % (k, v)
        return stream.getvalue()
        
    def write(self, stream):
        stream.write(self.to_string())

    def is_main_repos(self):
        if 'gpgkey' in self.dict:
            v = self.dict['gpgkey']
            return v == 'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$basearch'
        return False

    def enabled(self):
        if 'enabled' in self.dict and self.dict['enabled']:
            v = self.dict['enabled']
            return v == '1' or v == 'True' or v == 'true'
        else:
            return False

    def set_enabled(self, value):
        if value: self.dict['enabled'] = '1'
        else: self.dict['enabled'] = '0'
        
    def delete(self):
        self.parent.delete_section(self)

class FedoraReposFile:
    def __init__(self, path):
        assert isinstance(path, str)
        self.path = path
        self.sections = []
        if os.path.exists(path):
            with open(path) as f:
                contents = f.readlines()
            contents = [l for l in contents if not l.startswith('#') and l.strip()!=''] # skip comments and blank lines at the beginning
            contents = [l.strip() for l in contents] # strip \n
            lines = []
            for line in contents:
                if line.startswith('[') and lines: # a new section starts
                    section = FedoraReposSection(lines, parent=self)
                    self.sections.append(section)
                    lines = []
                lines.append(line)
            section = FedoraReposSection(lines, parent=self)
            self.sections.append(section)

    def filename(self):
        return os.path.basename(self.path)

    @classmethod
    def full_path(cls, filename):
        assert isinstance(filename, str) and filename and not ' ' in filename
        return '/etc/yum.repos.d/%s' % filename

    @classmethod
    def all_repo_objs(cls):
        import glob
        paths = glob.glob('/etc/yum.repos.d/*.repo')
        return [FedoraReposFile(p) for p in paths]
        
    def write(self):
        if self.sections:
            with TempOwn(self.path):
                with open(self.path, 'w') as f:
                    for s in self.sections:
                        s.write(f)
        else: # no section. remove file
            if os.path.exists(self.path):
                run_as_root('rm -f "%s"' % self.path)

    def delete_section(self, section):
        assert section.parent == self
        assert section in self.sections
        self.sections.remove(section)

    def get_section(self, name):
        assert isinstance(name, str)
        for s in self.sections:
            if s.name == name: return s
        return None
    
    def has_section(self, name):
        assert isinstance(name, str)
        for s in self.sections:
            if s.name == name: return True
        return False

    def append_section(self, section):
        assert isinstance(section, FedoraReposSection)
        assert not section in self.sections
        self.sections.append(section)

class TimeStat:
    __open_stat_names = set()
    __begin_time = {}
    result = {}
    def __init__(self, name):
        assert isinstance(name, str) and name
        assert name not in TimeStat.__open_stat_names, name
        TimeStat.__open_stat_names.add(name)
        import time
        TimeStat.__begin_time[name] = time.time()
        self.name = name
    def __enter__(self):
        return None
    def __exit__(self, type, value, traceback):
        name = self.name
        assert isinstance(name, str) and name
        assert name in TimeStat.__open_stat_names
        import time
        length = time.time() - TimeStat.__begin_time[name]
        TimeStat.result[name] = length
        TimeStat.__open_stat_names.remove(name)
    @classmethod
    def clear(cls):
        cls.__open_stat_names.clear()
        cls.__begin_time.clear()
        cls.result.clear()

def add_linuxskill(linux_skill, how_to_contact_the_submitter=None):
    assert isinstance(linux_skill, (str, unicode)) and linux_skill
    assert how_to_contact_the_submitter is None or isinstance(how_to_contact_the_submitter, (str, unicode))

    import httplib, urllib
    params = {'linux_skill': linux_skill}
    if how_to_contact_the_submitter:
        params['how_to_contact_the_submitter'] = how_to_contact_the_submitter
    params = urllib.urlencode(params)
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}
    connection = httplib.HTTPConnection('we-like-ailurus.appspot.com')
    connection.request('POST', '/add_linuxskill', params)
    response = connection.getresponse()
    assert response.status == 200, response.status
    connection.close()

def add_suggestion(suggestion, how_to_contact_the_submitter=None):
    assert isinstance(suggestion, (str, unicode)) and suggestion
    assert how_to_contact_the_submitter is None or isinstance(how_to_contact_the_submitter, (str, unicode))
    
    import httplib, urllib
    params = {'suggestion': suggestion}
    if how_to_contact_the_submitter:
        params['how_to_contact_the_submitter'] = how_to_contact_the_submitter
    params = urllib.urlencode(params)
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}
    connection = httplib.HTTPConnection('we-like-ailurus.appspot.com')
    connection.request('POST', '/add_suggestion', params)
    response = connection.getresponse()
    assert response.status == 200, response.status
    connection.close()

def debian_installation_command(package_names):
    return 'apt-get install ' + package_names

def fedora_installation_command(package_names):
    return 'yum install ' + package_names

def archlinux_installation_command(package_names):
    return 'pacman -S ' + package_names

def useBASH():
    import os
    return os.environ['SHELL'] == '/bin/bash'

def get_ailurus_version():
    import os
    path = A+'/version'
    with open(path) as f:
        return f.read().strip()
    
def get_ailurus_release_date():
    import os, time
    path = A+'/version'
    info = os.stat(path)
    return time.strftime('%Y-%m-%d', time.gmtime(info.st_mtime))

def now(): # return current time in seconds
    import time
    return long(time.time())

def time_string(time):
    import datetime
    return datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M')

class Snapshot:
    def __init__(self, _dict):
        assert isinstance(_dict, dict) and \
               'time' in _dict and \
               'comment' in _dict and \
               'pkgs' in _dict
        self.dict = _dict
    
    def remove(self):
        os.unlink(self.path())
    
    @classmethod
    def new_snapshot(cls):
        dict = {}
        dict['time'] = now()
        dict['comment'] = ''
        BACKEND.cache_changed() # if the system is changed outside ...
        dict['pkgs'] = BACKEND.get_installed_pkgs_set() # set
        s = Snapshot(dict)
        s.write()
        return s
    
    def path(self):
        return Config.config_dir + 'snapshot_%d' % self.time()
    
    def time(self):
        return self.dict['time']

    def comment(self):
        return self.dict['comment']

    def set_comment(self, new_comment):
        assert isinstance(new_comment, str)
        self.dict['comment'] = new_comment.replace('\n', ' ').strip()
        self.write()
    
    def write(self):
        with open(self.path(), 'w') as f:
            for k,v in self.dict.items():
                if k == 'pkgs':
                    v = ','.join(list(v))
                print >>f, '%s=%s' % (k,v)
    
    @classmethod
    def read(cls, path):
        with open(path) as f:
            lines = f.readlines()
        lines = [l.strip() for l in lines]
        lines = [l for l in lines if l]
        dict = {}
        for line in lines:
            k, v = line.split('=', 1)
            if k == 'pkgs':
                if v: v = set(v.split(','))
                else: v = set()
            elif k == 'time': v = long(v)
            dict[k] = v
        return Snapshot(dict)

    def difference(self):
        current = BACKEND.get_installed_pkgs_set()
        self_pkgs = self.dict['pkgs']
        new_installed = current.difference(self_pkgs)
        new_removed = self_pkgs.difference(current)
        return new_installed, new_removed
    
    @classmethod
    def list_snapshots(cls):
        ret = []
        import glob
        paths = glob.glob(Config.config_dir + 'snapshot_*')
        for p in paths:
            filename = os.path.basename(p)
            assert filename.startswith('snapshot_')
            time = long(filename[9:])
            ret.append(time)
        return ret
    
    @classmethod
    def get_snapshot_at(cls, time):
        path = Config.config_dir + 'snapshot_%s' % time
        return cls.read(path)
    
    @classmethod
    def all_snapshots(cls):
        ret = []
        import glob
        paths = glob.glob(Config.config_dir + 'snapshot_*')
        for p in paths:
            ret.append(cls.read(p))
        return ret

try:
    AILURUS_VERSION = get_ailurus_version()
    AILURUS_RELEASE_DATE = get_ailurus_release_date()
except: # raise exception in python console because __file__ is not defined
    print_traceback()

Config.init()

install_locale()

GPL = _('GNU General Public License')
LGPL = _('GNU Lesser General Public License')
EPL = _('Eclipse Public License')
MPL = _('Mozilla Public License')
BSD = _('Berkeley Software Distribution License')
MIT = _('MIT License')
CDDL = _('Common Development and Distribution License')
APL = _('Aptana Public License')
AL = _('Artistic License')

import atexit
atexit.register(ResponseTime.save)
atexit.register(KillWhenExit.kill_all)
atexit.register(drop_priviledge)
try:
    firefox.init()
    if firefox.support:
        atexit.register(firefox.save_user_prefs)
except:
    print_traceback()

try:
    import pynotify
    pynotify.init('Ailurus')
except:
    print 'Cannot init pynotify'

UBUNTU = Config.is_Ubuntu()
UBUNTU_DERIV = False # True value means Ubuntu derivative. For Ubuntu it is False. For Mint it is True.
MINT = Config.is_Mint()
YLMF = Config.is_YLMF()
DEEPIN = Config.is_Deepin()
FEDORA = Config.is_Fedora()
ARCHLINUX = Config.is_ArchLinux()
DEBIAN = Config.is_Debian()
if UBUNTU:
    DISTRIBUTION = 'ubuntu'
    VERSION = Config.get_Ubuntu_version()
    BACKEND = APT
    installation_command_backend = debian_installation_command
elif MINT:
    DISTRIBUTION = 'ubuntu'
    UBUNTU_DERIV = True
    VERSION = Config.get_Mint_version() # VERSION is in ['5', '6', '7', '8', '9', '10']
    VERSION = ['hardy', 'intrepid', 'jaunty', 'karmic', 'lucid', 'maverick'][int(VERSION)-5]
    BACKEND = APT
    installation_command_backend = debian_installation_command
elif YLMF:
    DISTRIBUTION = 'ubuntu'
    UBUNTU_DERIV = True
    VERSION = Config.get_YLMF_version()
    BACKEND = APT
    installation_command_backend = debian_installation_command
elif DEEPIN:
    DISTRIBUTION = 'ubuntu'
    UBUNTU_DERIV = True
    VERSION = Config.get_Deepin_version()
    BACKEND = APT
    installation_command_backend = debian_installation_command
elif FEDORA:
    DISTRIBUTION = 'fedora'
    VERSION = Config.get_Fedora_version()
    BACKEND = RPM
    installation_command_backend = fedora_installation_command
elif ARCHLINUX:
    DISTRIBUTION = 'archlinux'
    VERSION = '' # ArchLinux has no version -_-b
    BACKEND = PACMAN
    installation_command_backend = archlinux_installation_command
elif DEBIAN:
    DISTRIBUTION = 'debian'
    VERSION = Config.get_Debian_version()
    BACKEND = APT
    installation_command_backend = debian_installation_command
else:
    # This Linux distribution is not supported. :(
    DISTRIBUTION = ''
    VERSION = ''
    BACKEND = None
    installation_command_backend = None

GNOME = False
KDE = False
XFCE = False
# Thank you, GShutdown Team!
# This code is from gshutdown/src/values.c
# GPLv2
WINDOW_MANAGER = window_manager_name()
if WINDOW_MANAGER == "Metacity":
    GNOME = True
elif WINDOW_MANAGER == "KWin":
    KDE = True
elif WINDOW_MANAGER == "Xfwm4":
    XFCE = True
else:
    print 'Window Manager is not recognized:', WINDOW_MANAGER
    # These functions are less effective, but they work.
    GNOME = Config.is_GNOME()
    KDE = Config.is_KDE()
    XFCE = Config.is_XFCE()
if GNOME:
    DESKTOP = 'gnome'
elif KDE:
    DESKTOP = 'kde'
elif XFCE:
    DESKTOP = 'xfce'
else:
    DESKTOP = ''