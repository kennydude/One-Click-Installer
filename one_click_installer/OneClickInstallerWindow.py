# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Joe Simpson headangerkenny@googlemail.com
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('one-click-installer')

import gtk, json, urllib, os, sys, glib
import logging, thread
logger = logging.getLogger('one_click_installer')

from one_click_installer_lib import Window
def shellquote(s):
    return s.replace("'", "'\\''")

# See one_click_installer_lib.Window.py for more details about how this class works
class OneClickInstallerWindow(Window):
    __gtype_name__ = "OneClickInstallerWindow"
	def keypress(self, widget, event) :
		if event.keyval == gtk.keysyms.Escape :
            print "ESCAPED"
			gtk.main_quit()
    def load_data(self, to_open):
        try:
            if "http" in to_open:
                contents = urllib.urlopen(to_open)
            else:
                contents = open(to_open, 'r')
            contents = json.load(contents)
            for source in contents['sources']:
                self.liststore.append([_("Add the source %s to your system") % source])
            for package in contents['packages']:
                self.liststore.append([_("Install the pakage %s") % package])
            self.liststore.remove(self.please_wait)
            self.one_click = contents
        except Exception as ex:
            print ex
            self.liststore.remove(self.please_wait)
            self.liststore.append([_("ERROR: Couldn't read that file!")])
            print "Couldn't load file"
            sys.exit()
    
    def set_file(self, to_open):
        thread.start_new_thread(self.load_data, (to_open, ))
    def exit_button(self, widget, data=None):
        print "Install canceled"
        gtk.main_quit()
    def install_app(self):
        '''
        Actually install the app here!!!!
        '''
        command = ""
        for source in self.one_click['sources']:
            command += "add-apt-repository %s;" % shellquote(source)
        command += "apt-get update;"
        for package in self.one_click['packages']:
            command += "apt-get install %s;" % shellquote(package)
        print "About to execute '%s' in a root terminal" % command
        os.system('gksudo -k -m "%s" "sh -c \'%s\'"' % (_("Please enter your password to install the software"), command))
        glib.idle_add(self.done)
    def done(self):
        self.dialog.destroy()
        msg = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO, gtk.BUTTONS_OK, _("Software was installed. Thanks for using One Click Installer"))
        msg.connect('response', gtk.main_quit)
        msg.show()
    def install_button(self, widget, data=None):
        import PleasewaitdialogDialog
        self.dialog = PleasewaitdialogDialog.PleasewaitdialogDialog()
        self.dialog.set_transient_for(self)
        thread.start_new_thread(self.install_app, ())
        self.dialog.show()
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(OneClickInstallerWindow, self).finish_initializing(builder)
        self.connect("key-press-event", self.keypress)
        # Code for other initialization actions should be added here.
        self.liststore = gtk.ListStore(str)
        self.please_wait = self.liststore.append([_("Please wait...")])
        the_list = self.ui["changesBox"]
        the_list.set_model(self.liststore)
        textrenderer = gtk.CellRendererText()
        
        exit_button = self.ui['cancelButton']
        exit_button.connect('clicked', self.exit_button, None)
        install_button = self.ui['installButton']
        install_button.connect('clicked', self.install_button, None)

        # Add the column to the treeview
        column = gtk.TreeViewColumn(_("Item"), textrenderer, text=0)
        column.set_sort_column_id(1)
        the_list.append_column(column)

