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
import gtk, gobject, pango
import sys, os
from lib import *
from libu import *

# TODO: Shall we display commented line in treeview?

class ReposConfigPane(gtk.VBox):
    icon = D+'sora_icons/m_repository_configure.png'
    text = _('Edit\nRepository')
    
    def __init__(self, main_view):
        gtk.VBox.__init__(self, False, 5)
        
        if os.path.exists('/etc/apt/sources.list')==True:
        
        # the first gobject.TYPE_PYOBJECT is in [True, False, None]
        # True: this is a deb line.
        # False: this is a deb line, commented by "#" mark
        # None: this is not a deb line. For example, a normal comment
        #
        # the second gobject.TYPE_STRING is a line
            self.treestore = treestore = gtk.TreeStore(gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)
            self.treestore_filter = treestore_filter = treestore.filter_new()
            treestore_filter.set_visible_func(self.__treestore_item_visible_function)
            self.treeview = treeview = gtk.TreeView(treestore_filter)
        
            toggle_render = gtk.CellRendererToggle()
            toggle_render.set_property('activatable', True)
            toggle_render.connect('toggled',self.__repo_toggled, treestore_filter)
            toggle_column = gtk.TreeViewColumn()
            toggle_column.set_title(_('Enabled'))
            toggle_column.pack_start(toggle_render, False)
            toggle_column.set_cell_data_func(toggle_render, self.__repo_toggle_cell_function)
        
            text_render = gtk.CellRendererText()
            text_render.connect('edited', self.__repo_text_edited)
            text_render.set_property('ellipsize', pango.ELLIPSIZE_END)
            text_column = gtk.TreeViewColumn()
            text_column.pack_start(text_render)
            text_column.set_cell_data_func(text_render, self.__repo_text_cell_function)
        
            treeview.append_column(toggle_column)
            treeview.append_column(text_column)
            treeview.set_rules_hint(True)
            self.__refresh_treestore()
        
            scrollwindow = gtk.ScrolledWindow()
            scrollwindow.add(treeview)
            scrollwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
            scrollwindow.set_shadow_type(gtk.SHADOW_IN)
        
        # TODO: Put add_debline_button in AddReposArea. Add signal "clicked" to AddReposArea.
            self.add_repos_area = add_repos_area = AddReposArea()
            self.add_debline_button = add_debline_button = image_stock_button(gtk.STOCK_ADD, _('Add'))
            add_debline_button.connect('clicked', self.__add_debline_button_clicked)
            add_debline_button_align = gtk.Alignment(0.5, 0.5)
            add_debline_button_align.add(add_debline_button) # put add_debline_button at right-bottom corner
            bottom_box = gtk.HBox(False, 10)
            bottom_box.set_border_width(5)
            bottom_box.pack_start(add_repos_area, True)
            bottom_box.pack_start(add_debline_button_align, False)
        
            self.treeview.expand_all()
            self.treeview.get_selection().select_path('0')
            
#       Uncomment the following lines when menu is done.        
#        def button_press_event(w, event):
#            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
#                path = w.get_path_at_pos(int(event.x), int(event.y))
#                selection = w.get_selection()
#                if path:
#                    selection.select_path(path[0])
#                    #TODO: display menu
#                    return True
#            return False
#        
#        self.treeview.connect('button_press_event', button_press_event)

            self.pack_start(scrollwindow)
            self.pack_start(bottom_box, False)

        else:
            label = gtk.Label(_('Sorry. Ailurus cannot find your sources.list.\n'
            'Please fix it first using Ubuntu Update Manager.'))
            label.modify_font(pango.FontDescription('Sans 12'))
            warning_box = gtk.VBox(False, 10)
            warning_box.pack_start(label, True)
            self.pack_start(warning_box, False)

    def __treestore_item_visible_function(self, treestore, iter):
        object = treestore.get_value(iter, 0) # instance of gobject.TYPE_PYOBJECT
        return object != None
    
    def __repo_toggle_cell_function(self, column, cell, model, iter):
        object = model.get_value(iter, 0)
        if object != None:
            cell.set_property('active', object)
    
    def __repo_text_cell_function(self, column, cell, model, iter):
        parent = model.iter_parent(iter)
        object = model.get_value(iter, 0)
        text = model.get_value(iter, 1)
        if parent == None:
            # this is file name
            file_path = text
            file_name = os.path.split(file_path)[1]
            cell.set_property('markup', '<b>%s</b> (%s: %s)' %
                                        (file_name, _('File'), file_path))
            cell.set_property('editable', False)
        elif object != None:
            # this is a line in file
            cell.set_property('markup', self.__colorful_debline(text))
            cell.set_property('editable', True)
    
    def __colorful_debline(self, text):
        words = text.split()
        if len(words) < 3:
            return text
        
        def right_start(word):
            return word.startswith('deb') or word.startswith('deb-src')
        
        def right_protocol(word):
            return word.startswith('http://') or word.startswith('https://') or word.startswith('ftp://') or word.startswith('rstp://')
        
        if not right_start(words[0]):
            return text
        
        if not right_protocol(words[1]):
            return text
        
        import StringIO
        string = StringIO.StringIO()
        print >>string, '<span color="#6900B2">%s</span>' % words[0],
        print >>string, '<b><span color="red">%s</span></b>' % words[1],
        print >>string, '<span color="#007243">%s</span>' % words[2],
        
        for i in range(3, len(words)):
            print >>string, '<span color="blue">%s</span>' % words[i],
        return string.getvalue()
    
    def __is_debline_not_commented(self, line):
        # return None, means this is a normal comment
        # return True, means this is a deb line
        # return False, means this is a commented deb line
        # TODO: more accurate
        if line.startswith('#'):
            a = line[1:].lstrip()
            if a.startswith('deb ') or a.startswith('deb-src '):
                return False
        if line.startswith('deb ') or line.startswith('deb-src '):
            return True
        return None
    
    def __refresh_treestore(self):
        import glob
        self.treestore.clear()
        for path in ['/etc/apt/sources.list'] + glob.glob('/etc/apt/sources.list.d/*.list'):
            root_node = self.treestore.append(None, [True, path])
            with open(path) as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
            for line in lines:
                value = self.__is_debline_not_commented(line)
                if value == False:
                    line = line[1:].strip()
                self.treestore.append(root_node, [value, line])
            self.__set_parent_node_toggle(root_node)
        self.treestore_filter.refilter()
    
    def __write_changes_to_all_repo_files(self):
        parent = self.treestore.get_iter_first()
        while parent:
            self.__write_changes_to_one_repo_file(parent)
            parent = self.treestore.iter_next(parent)

    
    def __write_changes_to_all_repo_files(self):
        parent = self.treestore.get_iter_first()
        while parent:
            self.__write_changes_to_one_repo_file(parent)
            parent = self.treestore.iter_next(parent)
    
    def __write_changes_to_one_repo_file(self, parent):
        file_name = self.treestore.get_value(parent, 1)
        lines = []
        child_iter = self.treestore.iter_children(parent)
        while child_iter:
            type = self.treestore.get_value(child_iter, 0)
            text = self.treestore.get_value(child_iter, 1)
            if type == False: line = '#' + text
            else: line = text
            lines.append(line)
            child_iter = self.treestore.iter_next(child_iter)
        with TempOwn(file_name):
            with open(file_name, 'w') as f:
                f.write('\n'.join(lines))
    
    def __repo_toggled(self, renderer, path, treefilter):
        # toggle: uncommented repo line <-> commented repo line
        run_as_root('true') # do not catch AccessDenied in this function
        fiter_iter = treefilter.get_iter_from_string(path)
        treestore_childiter = treefilter.convert_iter_to_child_iter(fiter_iter)
        treestore_parent_iter = self.treestore.iter_parent(treestore_childiter)
        
        type = self.treestore.get_value(treestore_childiter, 0)
        assert type != None # because such kind of lines do not appear in treeview
        type = not type
        
        if treestore_parent_iter: # toggle one line in some file
            self.__enable_repos(type, treestore_childiter)
            self.__set_parent_node_toggle(treestore_parent_iter)
        else: # toggle whole repo file
            self.__enable_repos(type, treestore_childiter)
            self.__set_children_node_toggle(treestore_childiter, type)
        self.__write_changes_to_all_repo_files()
    
    def __repo_text_edited(self, cellrenderertext, path, new_text):
        if self.treestore_filter[path][1] != new_text:
            run_as_root('true') # do not catch AccessDeniedError in this function
            filter_iter = self.treestore_filter.get_iter_from_string(path)
            treestore_iter = self.treestore_filter.convert_iter_to_child_iter(filter_iter)
            type = self.__is_debline_not_commented(new_text)
            if type == False:
                new_text = new_text[1:]
            self.treestore.set_value(treestore_iter, 0, type)
            self.treestore.set_value(treestore_iter, 1, new_text)
            self.__write_changes_to_all_repo_files()
            self.treestore_filter.refilter()
    
    def __add_debline_button_clicked(self, widget):
        text = self.add_repos_area.construct_debline_from_entries()
        text = text.strip()
        if not text: return
        type = self.__is_debline_not_commented(text)
        if type == None:
            dialog = gtk.MessageDialog(buttons=gtk.BUTTONS_YES_NO,
                                    message_format=_('This is not a repository. Add it anyway?'))
            ret = dialog.run()
            dialog.destroy()
            if ret == gtk.RESPONSE_NO: return

        run_as_root('true')
        selection = self.treeview.get_selection()
        model, fiter_iter = selection.get_selected()
        treestore_iter = self.treestore_filter.convert_iter_to_child_iter(fiter_iter)
        treestore_parentiter = self.treestore.iter_parent(treestore_iter)
        if type == False:
            text = text[1:].strip()
        if treestore_parentiter:
            self.treestore.insert_after(treestore_parentiter, treestore_iter, [type, text])
        else:
            self.treestore.append(treestore_iter, [type, text])
        self.add_repos_area.clear_entries()
        self.__write_changes_to_all_repo_files()
        self.treestore_filter.refilter()
    
    def __set_parent_node_toggle(self, parent):
        file_name = self.treestore.get_value(parent, 1)
        child_iter = self.treestore.iter_children(parent)
        parent_node_type = None
        while child_iter:
            type = self.treestore.get_value(child_iter, 0)
            if type == False:
                parent_node_type = False
                break
            elif type == True:
                parent_node_type = True
            child_iter = self.treestore.iter_next(child_iter)
        self.__enable_repos(parent_node_type, parent)
    
    def __set_children_node_toggle(self, parent, type):
        child = self.treestore.iter_children(parent)
        while child:
            if self.treestore.get_value(child, 0) != None:
                self.__enable_repos(type, child)
            child = self.treestore.iter_next(child)
    
    def __enable_repos(self, type, iter):
        self.treestore.set_value(iter, 0, type)

class AddReposArea(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self, False)
        
        self.selected_box = None # self.selected_box is in [self.add_deb_line_box, self.add_PPA_repo_box]
        self.add_deb_line_box = gtk.HBox(False, 10)
        self.add_PPA_repo_box = gtk.HBox(False, 10)
        
        self.add_deb_line_box.entry = entry = gtk.Entry()
        self.add_deb_line_box.pack_start(entry)
        
        ppa_owner_label = gtk.Label(_('PPA owner:'))
        self.add_PPA_repo_box.ppa_owner_entry = ppa_owner_entry = gtk.Entry()
        ppa_name_label = gtk.Label(_('PPA name:'))
        self.add_PPA_repo_box.ppa_name_entry = ppa_name_entry = gtk.Entry()
        ppa_name_entry.set_text('ppa')
        self.add_PPA_repo_box.pack_start(ppa_owner_label, False)
        self.add_PPA_repo_box.pack_start(ppa_owner_entry)
        self.add_PPA_repo_box.pack_start(ppa_name_label, False)
        self.add_PPA_repo_box.pack_start(ppa_name_entry)
        
        self.box1 = gtk.VBox(False, 10)
        self.box1.pack_start(self.add_deb_line_box)
        self.box1.pack_start(self.add_PPA_repo_box)
        
        self.box2 = gtk.VBox(False, 10)
        def toggled(widget, index):
            self.__changed(index)
        radiobutton_deb = gtk.RadioButton(None, _('Add a line'))
        radiobutton_deb.connect('toggled', toggled, 0)
        radiobutton_ppa = gtk.RadioButton(radiobutton_deb, _('Add a PPA line'))
        radiobutton_ppa.connect('toggled', toggled, 1)
        radiobutton_deb.set_active(True)
        self.box2.pack_start(radiobutton_deb)
        self.box2.pack_start(radiobutton_ppa)
        
        self.pack_start(self.box1, True)
        self.pack_start(self.box2, False)
        
        self.__changed(0)
    
    def construct_debline_from_entries(self):
        if self.selected_box == self.add_deb_line_box:
            return self.add_deb_line_box.entry.get_text()
        elif self.selected_box == self.add_PPA_repo_box:
            user = self.add_PPA_repo_box.ppa_owner_entry.get_text()
            if not user:
                return ''
            ppa = self.add_PPA_repo_box.ppa_name_entry.get_text()
            if not ppa:
                return ''
            text = 'deb http://ppa.launchpad.net/%s/%s/ubuntu %s main' % (user, ppa, VERSION)
            return text
        
    def clear_entries(self):
        if self.selected_box == self.add_deb_line_box:
            self.add_deb_line_box.entry.set_text('')
        elif self.selected_box == self.add_PPA_repo_box:
            self.add_PPA_repo_box.ppa_owner_entry.set_text('')
            self.add_PPA_repo_box.ppa_name_entry.set_text('')
    
    def __changed(self, index):
        if index == 0:
            self.selected_box = self.add_deb_line_box
            self.add_deb_line_box.set_sensitive(True)
            self.add_PPA_repo_box.set_sensitive(False)
        elif index == 1:
            self.selected_box = self.add_PPA_repo_box
            self.add_deb_line_box.set_sensitive(False)
            self.add_PPA_repo_box.set_sensitive(True)
